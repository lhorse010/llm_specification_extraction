import pandas as pd
import os
import glob
import sys

def merge_excel_files(directory_path):
    # Create directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    
    # Get all .xlsx files in specified directory
    excel_files = glob.glob(os.path.join(directory_path, "*.xlsx"))
    
    # Get the result file path in the same directory
    result_path = os.path.join(directory_path, 'result.xlsx')
    
    # List to store all dataframes
    all_dfs = []
    
    # First file flag to get common columns
    is_first_file = True
    common_df = None
    
    # Iterate through all Excel files
    for file in excel_files:
        # Skip the result.xlsx file if it exists
        if os.path.basename(file) == 'result.xlsx':
            continue
            
        try:
            # Read the 'mtl' sheet from the Excel file
            df = pd.read_excel(file, sheet_name='mtl')
            
            if is_first_file:
                # For the first file, keep all columns except the last one as common columns
                common_df = df.iloc[:, :-1]
                is_first_file = False
            
            # Get the last column and rename it to the filename (without extension)
            file_name = os.path.splitext(os.path.basename(file))[0]
            last_col = df.iloc[:, -1]
            last_col.name = file_name
            
            # Create empty column
            empty_col = pd.Series(['' for _ in range(len(df))], name='')
            
            # Append both the last column and empty column
            all_dfs.extend([last_col, empty_col])
            print(f"Successfully processed file: {file}")
            
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
    
    if common_df is not None and all_dfs:
        # Combine all dataframes
        result_df = pd.concat([common_df] + all_dfs, axis=1)
        
        # Save to Excel
        with pd.ExcelWriter(result_path, engine='openpyxl') as writer:
            result_df.to_excel(writer, sheet_name='mtl', index=False)
        
        print(f"Merge completed! Results saved in {result_path}")
    else:
        print("No files were processed successfully.")

if __name__ == "__main__":
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <doc_dir_name> <doc_file_name>")
        sys.exit(1)
    
    # Get command line arguments
    doc_dir_name = sys.argv[1]
    doc_file_name = sys.argv[2]
    
    # Construct the full directory path
    directory_path = os.path.join(".", "DeepSTL_convert", doc_dir_name, doc_file_name)
    
    merge_excel_files(directory_path)