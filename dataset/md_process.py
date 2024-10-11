import os
import re
import nltk
import argparse
from tqdm import tqdm

nltk.download('punkt', quiet=True)  # Download sentence tokenizer

def extract_tables(text):
    """Extract Markdown tables"""
    table_pattern = r'(\|[^\n]+\|\n)((?:\|[-:| ]+\|\n))((?:\|[^\n]+\|\n)+)'
    tables = re.findall(table_pattern, text, re.MULTILINE)
    return tables

def remove_md_formatting(text):
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove images
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
    # Remove bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text = re.sub(r'`(.+?)`', r'\1', text)
    # Remove heading markers
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove list markers
    text = re.sub(r'^\s*[-*+]\s', '', text, flags=re.MULTILINE)
    # Remove numbered list markers
    text = re.sub(r'^\s*\d+\.\s', '', text, flags=re.MULTILINE)
    # Remove tables
    text = re.sub(r'(\|[^\n]+\|\n)((?:\|[-:| ]+\|\n))((?:\|[^\n]+\|\n)+)', '', text)
    return text.strip()

def split_paragraphs(text):
    """Split text into paragraphs"""
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]

def split_sentences_md(md_text):
    # Remove Markdown formatting
    clean_text = remove_md_formatting(md_text)
    
    # Split into paragraphs
    paragraphs = split_paragraphs(clean_text)
    
    # Split each paragraph into sentences
    sentence_paragraphs = []
    for paragraph in paragraphs:
        sentences = nltk.sent_tokenize(paragraph)
        sentence_paragraphs.append(sentences)
    
    return sentence_paragraphs

def process_md_files(input_dir, output_dir, table_dir):
    # Ensure output and table directories exist
    for directory in [output_dir, table_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Get all .md files
    md_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))

    # Process each .md file
    for md_file in tqdm(md_files, desc="Processing Markdown files"):
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Extract tables
        tables = extract_tables(md_content)
        
        # Process tables
        if tables:
            table_file = os.path.join(table_dir, f"{os.path.basename(md_file)[:-3]}_table.txt")
            with open(table_file, 'w', encoding='utf-8') as f:
                for table in tables:
                    f.write(''.join(table) + '\n\n')

        sentence_paragraphs = split_sentences_md(md_content)

        # Create output filename
        relative_path = os.path.relpath(md_file, input_dir)
        output_file = os.path.join(output_dir, relative_path[:-3] + '.txt')

        # Ensure output file directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write sentences to output file, preserving paragraph structure
        with open(output_file, 'w', encoding='utf-8') as f:
            for paragraph in sentence_paragraphs:
                for sentence in paragraph:
                    if sentence.strip():  # Only write non-empty sentences
                        f.write(sentence.strip() + '\n')
                f.write('\n')  # Add empty line between paragraphs

    print(f"Processed {len(md_files)} Markdown files.")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process Markdown files and split into sentences.")
    parser.add_argument("subdirectory", help="Subdirectory name to be appended to input and output directories")
    
    # Parse arguments
    args = parser.parse_args()

    # Set input and output directories
    input_directory = os.path.join('raw_document', args.subdirectory)
    output_directory = os.path.join('document_after_sentence_slicing', args.subdirectory)
    table_directory = os.path.join(output_directory, 'table')

    # Execute processing
    process_md_files(input_directory, output_directory, table_directory)

if __name__ == "__main__":
    main()