import os
import json
from fuzzywuzzy import fuzz
import glob

def process_files(ground_truth_dir, input_dir, output_dir):
    txt_files = glob.glob(os.path.join(ground_truth_dir, '**', '*.txt'), recursive=True)
    
    for txt_file in txt_files:
        relative_path = os.path.relpath(txt_file, ground_truth_dir)
        json_file = os.path.join(input_dir, os.path.splitext(relative_path)[0] + '.json')
        
        if not os.path.exists(json_file):
            print(f"Warning: Corresponding JSON file not found for {txt_file}")
            continue
        
        with open(txt_file, 'r', encoding='utf-8') as f:
            txt_lines = f.readlines()
        
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        all_sentences = []
        for section in json_data['sections']:
            for sentence in section['sentences']:
                all_sentences.append({
                    'text': sentence['text'],
                    'section-id': section['section-id'],
                    'sentence-id': sentence['sentence-id']
                })
        
        specifications = []
        for txt_line in txt_lines:
            best_match = max(all_sentences, key=lambda x: fuzz.ratio(txt_line.strip(), x['text']))
            match_ratio = fuzz.ratio(txt_line.strip(), best_match['text'])
            if match_ratio > 60:
                specifications.append({
                    'section-id': best_match['section-id'],
                    'sentence-id': best_match['sentence-id'],
                    'sentence' : txt_line
                })
            else:
                specifications.append({
                    'section-id': -1,
                    'sentence-id': -1,
                    'sentence' : txt_line
                })
        
        output_file = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({'specifications': specifications}, f, ensure_ascii=False, indent=2)

folders = ['ardupilot_docs', 'px4_docs', 'autoware_docs']

for folder in folders:
    ground_truth_dir = os.path.join('ground_truth', folder, 'text_only')
    input_dir = os.path.join('input', folder, 'text_only')
    output_dir = os.path.join('ground_truth', folder, 'location')
    
    process_files(ground_truth_dir, input_dir, output_dir)

print("Processing completed.")