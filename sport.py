# FastAPI Tutorial with Basic PyQuery Project
import os
import json
import random
import shutil
import string
import urllib.request
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from typing import  Union
from pyquery import PyQuery
from pydantic import BaseModel
from uuid import uuid4 # Universally Unique Identifier

# PyDantic BaseModel Class
class Item(BaseModel):
    sport_class: str
    sport_name: Union[str, None] = None # Optional value (See in FastAPI/docs)

# Exception Class
class MyException(Exception):
    def __init__(self, name: str):
        self.name = name

# Dokwiki_link = 'https://zh.m.wikipedia.org/zh-tw/%E7%8A%AC%E7%A8%AE%E5%88%97%E8%A1%A8'
# doc = PyQuery(url=Dokwiki_link)
# doc_tr = doc.find('tr').children()

Dokwiki_link = 'https://zh.m.wikipedia.org/wiki/%E9%AB%94%E8%82%B2%E9%81%8B%E5%8B%95%E5%88%97%E8%A1%A8'
d = PyQuery(url=Dokwiki_link)
Extreme_sport = d('.mf-section-1').find('a').text().split(" ")
sky_sport = d('.mf-section-2').find('a').text().split(" ")
animal_sport = d('.mf-section-3').find('a').text().split(" ")

sport = 'sport.json'
wiki_sport = []
wiki_sport_new = []
if os.path.exists(sport):
    with open(sport, "r") as f:
        wiki_sport = json.load(f)

app = FastAPI() # FastAPI Module

@app.get('/get_Extreme_sport')
def ExtremeSport():
    return {'Extreme_sport:' : Extreme_sport}   

@app.get('/get_sky_sport')
def SkySport():
    return {'sky_sport:' : sky_sport}   

@app.get('/get_animal_sport')
def AnimalSport():
    return {'animal_sport:' : animal_sport}  

@app.exception_handler(MyException)
def call_exception_handler(request:Request, exc: MyException):
    return JSONResponse (
        status_code= 414,
        content= {
            'Message' : f'Oops ! {exc.name} did something. There goes a rainbow ...'
        }
    )
@app.post('/add', response_model=Item)
def create_sport(item: Item):
    item_dict = item.dict()    
    item_id = uuid4().hex
    item_dict.update({"id":item_id})
    wiki_sport.append(item_dict)
    # Save a new item into local database (JSON file)
    with open(sport, "w") as f:
        json.dump(wiki_sport, f, indent=4)
    return item_dict

@app.post('/upload')
def Upload_file(file: Union[UploadFile, None] = None):
    if not file: return {"message" : "No file upload"}
    try:
        file_location = './' + file.filename
        with open(file_location, "wb") as f:            
            shutil.copyfileobj(file.file, f)
            file.close()
        wiki_sport_new.append(file.filename)        
        return {"Result" : wiki_sport_new }
    except:
        raise MyException(name=f'Upload File {file.filename}')