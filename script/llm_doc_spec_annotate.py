from poe_api_wrapper import PoeApi
import sys
import os

tokens = {
    'p-b': os.getenv('ENV_P_B'), 
    'p-lat': os.getenv('ENV_P_LAT'),
}

# proxy 
proxy_config = [
    {"https://": os.getenv('HTTPS_POE_PROXY'),
     "http://": os.getenv('HTTP_POE_PROXY')}
]

def generate_prompt(doc):
    prompt_file = open("doc_sentences_spec_annotate_prompt.txt", "r")
    prompt = prompt_file.read()
    prompt_file.close()
    prompt += "#@#@#@#@#@\n\n"
    prompt += doc
    prompt += "\n\n#@#@#@#@#@"
    return prompt

def extract(prompt, model_name, result_file):
    # clear context, triple try, merge
    # client = PoeApi(tokens=tokens, proxy=proxy_config)
    client = PoeApi(tokens=tokens)
    bot=model_name
    chatId = None    

    for chunk in client.send_message(bot=bot, message=prompt, chatId=chatId):
        # non stream version
        pass
    print(chunk["text"], file=result_file, end='', flush=True)

def create_directory_if_not_exists(directory_path):
    """
    Check if the directory at the specified path exists, and create it if it doesn't.

    :param directory_path: The path of the directory to check and create
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        except OSError as e:
            print(f"Error creating directory: {e}")
    else:
        print(f"Directory already exists: {directory_path}")

if __name__ == "__main__":
    model_name = sys.argv[1]
    doc_dir_name = sys.argv[2]
    doc_file_name = sys.argv[3]
    
    file = open("../dataset/input/" + doc_dir_name + "/text_only/" + doc_file_name + ".json", "r")
    doc = file.read()
    file.close()
    
    prompt = generate_prompt(doc)

    # result_file: result/doc_dir/mode_name/model.txt
    result_file_dir = "./result/" + doc_dir_name + "/" + doc_file_name
    create_directory_if_not_exists(result_file_dir)
    result_file_name = result_file_dir + "/" + model_name + ".txt"
    result_file = open(result_file_name, "w")
    result_file.write("")
    result_file.close()
    
    result_file = open(result_file_name, "w+")
    extract(prompt, model_name, result_file)
    result_file.close()

    # TODO: metrics

