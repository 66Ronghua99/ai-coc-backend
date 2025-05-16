# ai-coc-backend
AI COC

## Requirement
### Docker
Current version relies pgvector (a vector database in PostgreSQL) to run. Therefore, please make sure that you have docker installed.
[Docker Install](https://docs.docker.com/desktop/)
### Pgvector
Pull docker image
```sh
docker pull pgvector/pgvector:pg17
```
Start the database. Move to the root directory of this repo
```sh
docker compose up -d
```
use `docker stats` to see whether a 'coc' contaier is running

## Python Env
Use any python environment manager you prefer. An example with anaconda is as follows:
```
conda create -n coc python=3.10
...creating env...
conda activate coc
pip install -r requirements.txt
```

## Embed COC rules
```sh
python split_rules/pgvector_storage.py
```

## Setting up OpenAI key
We use dotenv to load env variables. Create a .env file in the root directory
```.env
# .env
OPENAI_API_KEY="sk-xxxxxxxxx"
```

## Start game
```python
python main.py -m scary_fall.docx
```

By default, `main.py` load `docx` modules from `/docs` folder. If you prefer to switch the module, download one and put it inside the module folder. Currently, we only supports `docx` files.

