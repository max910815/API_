from fastapi import FastAPI, Path, Query
import openai
from pydantic import BaseModel
import json
import os
import csv
import time


class Data(BaseModel):
    key: str
    text: str
    

class File(BaseModel):
    Q: str
    A: str
    index: str = None


app = FastAPI()


def em(text):

    # API 基本資訊
    openai.api_key = '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'
    openai.timeout = 0
    # embedding模組設定
    embedding = 'text-embedding-ada-002'
    # 調用 text-embedding-ada-002 模型進行 Embedding
    response = openai.Embedding.create(input=text, engine=embedding)
    embeddings = response['data'][0]['embedding']
    
    return embeddings


@app.get("/")
async def hello():
    return "Hello, World!"


# Data data = new Data();
@app.post("/embedding")
async def embedding(data: Data):

    # API 基本資訊
    openai.api_key = data.key
    text = data.text
    # embedding模組設定
    embedding = 'text-embedding-ada-002'

    # 調用 text-embedding-ada-002 模型進行 Embedding
    response = openai.Embedding.create(input=text, engine=embedding)
    embeddings = response['data'][0]['embedding']

    return embeddings


@app.post("/create")
async def create(file: list[File]):
    
    id = hash(time.time())
    path = './' + str(id) + '.json'
    
    coulum = []
    for row in file:
        row.index = row.Q + row.A
        temp = {'Q': row.Q, 'A': row.A, 'index': row.index, 'embedding': em(row.index)}
        coulum.append(temp)
    #將coulum寫入json檔案
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(coulum))
    re = {'id': id, 'data': coulum }
    return re

@app.post("/asking")
async def asking(asking: str):
    
    return asking