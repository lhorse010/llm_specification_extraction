# llm_specificaiton_extraction

## 1. dataset

### 1.1 raw document dataset

25 flight modes of Ardupilot

12 flight modes of PX4

6 planning module of Autoware



### 1.2 data process

```shell
# markdown
python md_process.py document_dir_name

# markdown
python rst_process.py document_dir_name

```



## 2. env set

poe cookie set: https://github.com/snowby666/poe-api-wrapper

```shell
## poe cookie
export ENV_P_B='...'
export ENV_P_LAT='...'

## proxy
export HTTPS_POE_PROXY='...'
export HTTP_POE_PROXY='...'
```

