import re
import json
import sys

def extract_json(text):
    json_match = re.search(r'```json\n(.*?\n)```', text, re.DOTALL)
    
    if json_match:
        json_string = json_match.group(1)
        
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No JSON block found in the text.")
        return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'r') as file:
            response_text = file.read()

        extracted_json = extract_json(response_text)

        if extracted_json:
            with open(output_file, 'w') as file:
                json.dump(extracted_json, file, indent=2)
            print(f"JSON successfully extracted and written to {output_file}")
        else:
            print("Failed to extract JSON. No output file written.")

    except FileNotFoundError:
        print(f"Error: The input file '{input_file}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{input_file}' or write to '{output_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()