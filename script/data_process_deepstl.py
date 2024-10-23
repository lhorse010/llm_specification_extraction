import sys
import pandas as pd
import json
from difflib import SequenceMatcher
import os

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_best_match(text, json_items):
    if pd.isna(text):  # Handle empty value
        return None
    
    max_similarity = 0
    best_match_item = None
    
    for item in json_items:
        similarity = similar(text, item['sentence'])
        if similarity > max_similarity and similarity >= SIMILARITY_THRESHOLD:
            max_similarity = similarity
            best_match_item = item
    
    return best_match_item

def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def main(model_name, doc_dir_name, doc_file_name):
    try:
        # Construct file paths
        groundtruth_file_name = os.path.join("ground_truth", doc_dir_name, doc_file_name, "raw_data.xlsx")
        json_file_name = os.path.join("DeepSTL_convert", doc_dir_name, doc_file_name, f"{model_name}.json")
        res_file_name = os.path.join("DeepSTL_convert", doc_dir_name, doc_file_name, f"{model_name}.xlsx")

        # Check if input files exist
        if not os.path.exists(groundtruth_file_name):
            raise FileNotFoundError(f"Excel file not found: {groundtruth_file_name}")
        if not os.path.exists(json_file_name):
            raise FileNotFoundError(f"JSON file not found: {json_file_name}")

        # Read Excel file
        print(f"Reading Excel file: {groundtruth_file_name}")
        df = pd.read_excel(groundtruth_file_name, sheet_name='mtl')

        # Read JSON file
        print(f"Reading JSON file: {json_file_name}")
        with open(json_file_name, 'r') as f:
            data = json.load(f)

        # Get all items from json
        json_items = data['temporal_logic_formulars']
        
        # Define similarity threshold
        global SIMILARITY_THRESHOLD
        SIMILARITY_THRESHOLD = 0.8

        # Add new column 'json_data' containing the entire matched item
        print("Processing matches...")
        df['json_data'] = df['text'].apply(lambda x: find_best_match(x, json_items))

        # Find unmatched json items
        matched_items = set()
        for item in df['json_data'].dropna():
            matched_items.add(json.dumps(item))  # Convert dict to string for comparison

        unmatched_items = []
        for item in json_items:
            if json.dumps(item) not in matched_items:
                unmatched_items.append(item)

        # Add three empty rows
        if unmatched_items:
            empty_rows = pd.DataFrame({'text': [''] * 3, 'json_data': [None] * 3})
            df = pd.concat([df, empty_rows], ignore_index=True)

        # Add unmatched items
        for item in unmatched_items:
            new_row = pd.DataFrame({'text': [''], 'json_data': [item]})
            df = pd.concat([df, new_row], ignore_index=True)

        # Ensure output directory exists
        ensure_directory_exists(res_file_name)

        # Save the updated Excel file
        print(f"Saving results to: {res_file_name}")
        df.to_excel(res_file_name, sheet_name='mtl', index=False)
        print("Processing completed successfully")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if correct number of arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <model_name> <doc_dir_name> <doc_file_name>")
        sys.exit(1)
    
    # Get command line arguments
    model_name = sys.argv[1]
    doc_dir_name = sys.argv[2]
    doc_file_name = sys.argv[3]
    
    # Call main function
    main(model_name, doc_dir_name, doc_file_name)