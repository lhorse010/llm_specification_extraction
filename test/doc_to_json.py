import json
import sys

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

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            document = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except IOError:
        print(f"Error: Unable to read input file '{input_file}'.")
        sys.exit(1)

    result = convert_to_json(document)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"JSON output has been written to '{output_file}'.")
    except IOError:
        print(f"Error: Unable to write to output file '{output_file}'.")
        sys.exit(1)

if __name__ == "__main__":
    main()