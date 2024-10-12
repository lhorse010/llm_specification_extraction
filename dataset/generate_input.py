import json
import os
from pathlib import Path

def convert_to_json(document):
    sections = document.split('\n\n')
    title = sections[0].strip()
    json_sections = []

    for section_id, section in enumerate(sections[1:]):
        lines = section.strip().split('\n')
        section_title = lines[0].strip()
        sentences = lines[1:]

        json_section = {
            'section-id': section_id,
            'title': section_title,
            'sentences': []
        }

        for sentence_id, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if sentence:
                json_section['sentences'].append({
                    'sentence-id': sentence_id,
                    'text': sentence
                })

        json_sections.append(json_section)

    return {
        'title': title,
        'sections': json_sections
    }

def process_directory(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    for txt_file in input_path.glob('*.txt'):
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                document = f.read()
        except IOError:
            print(f"Error: Unable to read input file '{txt_file}'.")
            continue

        result = convert_to_json(document)
        
        output_file = output_path / f"{txt_file.stem}.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"JSON output has been written to '{output_file}'.")
        except IOError:
            print(f"Error: Unable to write to output file '{output_file}'.")

def main():
    directories = [
        ('document_after_manual_check/ardupilot_docs/text_only', 'input/ardupilot_docs/text_only'),
        ('document_after_manual_check/px4_docs/text_only', 'input/px4_docs/text_only'),
        ('document_after_manual_check/autoware_docs/text_only', 'input/autoware_docs/text_only')
    ]

    for input_dir, output_dir in directories:
        print(f"Processing directory: {input_dir}")
        process_directory(input_dir, output_dir)
        print(f"Finished processing {input_dir}\n")

if __name__ == "__main__":
    main()