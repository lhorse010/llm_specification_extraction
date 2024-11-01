# llm_specificaiton_extraction

## 1. dataset

### 1.1 raw document dataset

25 flight modes of Ardupilot

12 flight modes of PX4

6 planning module of Autoware



### 1.2 data process

```shell
####sentence slicing####
# markdown
python md_process.py document_dir_name
# rst
python rst_process.py document_dir_name

####generate input(json)####
python generate_input.py

```



## 2. env set

poe cookie set: https://github.com/snowby666/poe-api-wrapper

```shell
## poe cookie
export ENV_P_B='...'
export ENV_P_LAT='...'
```



## 3. To use

### 3.1 llm end to end

```shell
#### run ####
cd script
# prompt: doc_spc_extraction_end_to_end_prompt.txt
./main_spec_extract_end_to_end.sh

#### check  result ####
# cd ./result_end_to_end
```

### 3.2 llm annotate + transform

#### 3.2.1 llm annotate

```shell
#### run ####
cd script
# prompt: doc_sentences_spec_annotate_prompt.txt
./main_annotate.sh
# to generate input json file of transform process
./generate_second_step_input.sh

#### check result ####
# cd ./result_annotate
# cd ./second_step_input
```

#### 3.2.2 llm spec transform

```shell
#### run ####
cd script
# prompt: doc_spec_transform_prompt.txt
./main_spec_transform.sh

#### check result ####
# cd ./result_llm_tranform
```

#### 3.2.3 deepstl spec transform

```shell
#### run ####
# follow the set up guaidence in https://github.com/JieHE-2020/DeepSTL
# to use input genetrate by our method
# use
# ./script/transformer_run.py

#### check result ####
# cd ./DeepSTL_convert
```

### 
