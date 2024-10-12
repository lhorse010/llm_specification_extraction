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
    # client = PoeApi(tokens=tokens, proxy=proxy_config)
    client = PoeApi(tokens=tokens)
    bot=model_name
    chatId = None    

    for chunk in client.send_message(bot=bot, message=prompt, chatId=chatId):
        # non stream version
        pass
    print(chunk["text"], file=result_file, end='', flush=True)

if __name__ == "__main__":
    model_name = sys.argv[1]
    doc_file_name = sys.argv[2]
    result_file_name = sys.argv[3]
    

    file = open(doc_file_name, "r")
    doc = file.read()
    file.close()
    
    prompt = generate_prompt(doc)

    # TODO: Store the old result
    # Clear the result file
    result_file = open(result_file_name, "w")
    result_file.write("")
    result_file.close()
    
    result_file = open(result_file_name, "w+")
    extract(prompt, model_name, result_file)
    result_file.close()