import os
import re
import nltk
import argparse
from tqdm import tqdm
from docutils.core import publish_parts
from docutils.parsers.rst import roles
from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst import Directive
import html

nltk.download('punkt', quiet=True)  # Download sentence tokenizer

# Define dummy roles and directives to handle custom RST elements
def dummy_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    return [], []

class DummyDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {}
    def run(self):
        return []

# Register dummy roles and directives
roles.register_local_role('ref', dummy_role)
register_directive('youtube', DummyDirective)
register_directive('toctree', DummyDirective)

def extract_tables(text):
    grid_table_pattern = r'\+[-+]+\+\n((?:\|[^\n]+\|\n)+)\+[-+]+\+'
    simple_table_pattern = r'(===\s+=+\n(?:(?!===).+\n)+===\s+=+\n)'
    
    grid_tables = re.findall(grid_table_pattern, text, re.MULTILINE)
    simple_tables = re.findall(simple_table_pattern, text, re.MULTILINE)
    
    return grid_tables + simple_tables

def remove_rst_formatting(text):
    # Remove links
    text = re.sub(r'`([^`]+)`_', r'\1', text)
    # Remove images
    text = re.sub(r'.. image:: [^\n]+', '', text)
    # Remove inline literals
    text = re.sub(r'``(.+?)``', r'\1', text)
    # Remove directives
    text = re.sub(r'.. [^:]+::', '', text)
    # Remove directive content
    text = re.sub(r'   :.*?(\n\n|\Z)', r'\1', text, flags=re.DOTALL)
    # Remove section titles
    text = re.sub(r'^[=\-`:\'"~^_*+#]+\n', '', text, flags=re.MULTILINE)
    # Remove list markers
    text = re.sub(r'^\s*[-*+]\s', '', text, flags=re.MULTILINE)
    # Remove numbered list markers
    text = re.sub(r'^\s*\d+\.\s', '', text, flags=re.MULTILINE)
    # Remove tables
    text = re.sub(r'\+[-+]+\+\n((?:\|[^\n]+\|\n)+)\+[-+]+\+', '', text)
    # Remove custom roles (like :ref:)
    text = re.sub(r':[a-z]+:`([^`]+)`', r'\1', text)
    return text.strip()

def split_paragraphs(text):
    """Split text into paragraphs"""
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]

def split_sentences_rst(rst_text):
    # Convert RST to HTML
    try:
        html = publish_parts(rst_text, writer_name='html', settings_overrides={'report_level': 5})['html_body']
    except Exception as e:
        print(f"Warning: RST to HTML conversion failed. Error: {str(e)}")
        # If conversion fails, use the original text
        html = rst_text
    
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', html)
    
    # Remove RST formatting
    clean_text = remove_rst_formatting(text)
    
    # Split into paragraphs
    paragraphs = split_paragraphs(clean_text)
    
    # Split each paragraph into sentences
    sentence_paragraphs = []
    for paragraph in paragraphs:
        sentences = nltk.sent_tokenize(paragraph)
        sentence_paragraphs.append(sentences)
    
    return sentence_paragraphs


def simplify_refs(text):
    return re.sub(r':ref:`([^`]+)`', r'\1', text)

def process_rst_files(input_dir, output_dir, table_dir):
    # Ensure output and table directories exist
    for directory in [output_dir, table_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Get all .rst files
    rst_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.rst'):
                rst_files.append(os.path.join(root, file))

    # Process each .rst file
    for rst_file in tqdm(rst_files, desc="Processing RST files"):
        with open(rst_file, 'r', encoding='utf-8') as f:
            rst_content = f.read()

        rst_content = simplify_refs(rst_content)
        # Extract tables
        tables = extract_tables(rst_content)
        
        # Process tables
        if tables:
            table_file = os.path.join(table_dir, f"{os.path.basename(rst_file)[:-4]}_table.txt")
            with open(table_file, 'w', encoding='utf-8') as f:
                for table in tables:
                    f.write(table + '\n\n')

        sentence_paragraphs = split_sentences_rst(rst_content)

        # Create output filename
        relative_path = os.path.relpath(rst_file, input_dir)
        output_file = os.path.join(output_dir, "text_only", relative_path[:-4] + '.txt')

        # Ensure output file directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write sentences to output file, preserving paragraph structure
        with open(output_file, 'w', encoding='utf-8') as f:
            for paragraph in sentence_paragraphs:
                for sentence in paragraph:
                    if sentence.strip():  # Only write non-empty sentences
                        f.write(html.unescape(sentence.strip()) + '\n')
                f.write('\n')  # Add empty line between paragraphs

    print(f"Processed {len(rst_files)} RST files.")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process RST files and split into sentences.")
    parser.add_argument("subdirectory", help="Subdirectory name to be appended to input and output directories")
    
    # Parse arguments
    args = parser.parse_args()

    # Set input and output directories
    input_directory = os.path.join('raw_document', args.subdirectory)
    output_directory = os.path.join('document_after_sentence_slicing', args.subdirectory)
    table_directory = os.path.join(output_directory, 'table')

    # Execute processing
    process_rst_files(input_directory, output_directory, table_directory)

if __name__ == "__main__":
    main()