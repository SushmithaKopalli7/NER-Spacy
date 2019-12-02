import pandas as pd

#return the wordnet object value corresponding to the POS tag
from nltk.corpus import wordnet
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# create doc2vec vector columns
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# add tf-idfs columns
from sklearn.feature_extraction.text import TfidfVectorizer


from flask import Flask,jsonify
from flask import request
from collections import OrderedDict
from gensim.summarization import keywords
from gensim.summarization import summarize
from stemming.porter2 import stem
from flask_cors import CORS, cross_origin
from reviewModel import reviewModel

import spacy
import operator
import re


app = Flask(__name__)
cors = CORS(app, resources={r"/tags": {"origins": "http://localhost:port"}})

nlp = spacy.load('en_core_web_sm')

class my_dictionary(dict):  
  
    # __init__ function  
    def __init__(self):  
        self = dict()  
          
    # Function to add key:value  
    def add(self, key, value):  
        self[key] = value

@app.route("/producttags",methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def entity():
  
   req_data = request.get_json()
   text = req_data['text']
   product_name=req_data['product_name']
   return jsonify(EntityResponse(text,product_name))

@app.route("/hello")
def check():
   return "Hii......"

def EntityResponse(text,product_name):

    #nlp = spacy.load("C:/Users/NLP/Documents/poc/models/footwearModel")
    nlp = spacy.load("C:/Users/NLP/Desktop/NER-Spacy/models/categoryModel")
    doc=nlp(text)
    tags=doc.cats
    dict_cat=my_dictionary()
    categoryDisplay=my_dictionary()
    seoDisplay=my_dictionary()
    entityDisplay=my_dictionary()
    entity = {}
    seo={}
    category=my_dictionary()

    category_name= max(tags.items(), key=operator.itemgetter(1))[0]
    if category_name=="CLTH":
        nlp=spacy.load("C:/Users/NLP/Desktop/NER-Spacy/models/clothModel")
        doc_cloth=nlp(text)
        category.key="Category-1"
        category.value="Clothing"
        category.add(category.key,category.value)
        for key, value in mapStorage(doc_cloth).items():
            entity.setdefault(value, []).append(key)
            if value == "target":
                category.setdefault("Category-2", []).append(key)
            if value == "ItemType":
                category.key="Category-3"
                category.value=key
                category.add(category.key, category.value)
        categoryDisplay.key = "Category"
        categoryDisplay.value = category
        categoryDisplay.add(categoryDisplay.key, categoryDisplay.value)
        entityDisplay.key = "Entities"
        entityDisplay.value = entity
        entityDisplay.add(entityDisplay.key, entityDisplay.value)
        seo.setdefault("KeyWords", []).append(keyWordExtraction(text))
        seo.setdefault("Meta_Description", []).append(summarize(text))
        seo.setdefault("SEO_URL", []).append(re.sub('[^A-Za-z ]+', '', product_name).replace(" ", "_"))
        seoDisplay.key = "SEO"
        seoDisplay.value = seo
        seoDisplay.add(seoDisplay.key, seoDisplay.value)
        dict_cat.update(categoryDisplay)
        dict_cat.update(entityDisplay)
        dict_cat.update(seoDisplay)
        return dict_cat

    elif category_name=="JEWL":
        nlp = spacy.load("C:/Users/NLP/Desktop/NER-Spacy/models/JewlModel")
        doc_jewl=nlp(text)
        category.key="Category-1"
        category.value="Jewellery"
        category.add(category.key,category.value)
        for key, value in mapStorage(doc_jewl).items():
            entity.setdefault(value, []).append(key)
            if value == "TARGET":
                category.setdefault("Category-2",[]).append(key)
            if value == "ITEMTYPE":
                category.key = "Category-3"
                category.value = key
                category.add(category.key, category.value)
        categoryDisplay.key="Category"
        categoryDisplay.value=category
        categoryDisplay.add(categoryDisplay.key,categoryDisplay.value)
        entityDisplay.key = "Entities"
        entityDisplay.value = entity
        entityDisplay.add(entityDisplay.key, entityDisplay.value)
        seo.setdefault("KeyWords", []).append(keyWordExtraction(text))
        seo.setdefault("Meta_Description",[]).append(summarize(text))
        seo.setdefault("SEO_URL",[]).append(re.sub('[^A-Za-z ]+', '',product_name).replace(" ","_"))
        seoDisplay.key="SEO"
        seoDisplay.value=seo
        seoDisplay.add(seoDisplay.key,seoDisplay.value)
        dict_cat.update(categoryDisplay)
        dict_cat.update(entityDisplay)
        dict_cat.update(seoDisplay)
        return dict_cat

    elif category_name=="FOOT":
        nlp = spacy.load("C:/Users/NLP/Desktop/NER-Spacy/models/footwearModel")
        doc_foot=nlp(text)
        category.key="Category-1"
        category.value="Footwear"
        category.add(category.key,category.value)
        print("checking the prurals")
        stem("simpsons")
        for key, value in mapStorage(doc_foot).items():
            entity.setdefault(value, []).append(key)
            if value == "Target":
                category.setdefault("Category-2", []).append(key)
            if value == "ItemType":
                category.key = "Category-3"
                category.value = key
                category.add(category.key,category.value)
        categoryDisplay.key = "Category"
        categoryDisplay.value = category
        categoryDisplay.add(categoryDisplay.key, categoryDisplay.value)
        entityDisplay.key = "Entities"
        entityDisplay.value = entity
        entityDisplay.add(entityDisplay.key, entityDisplay.value)
        seo.setdefault("KeyWords", []).append(keyWordExtraction(text))
        seo.setdefault("Meta_Description", []).append(summarize(text))
        seo.setdefault("SEO_URL", []).append(re.sub('[^A-Za-z ]+', '',product_name).replace(" ","_"))
        seoDisplay.key = "SEO"
        seoDisplay.value = seo
        seoDisplay.add(seoDisplay.key, seoDisplay.value)
        dict_cat.update(categoryDisplay)
        dict_cat.update(entityDisplay)
        dict_cat.update(seoDisplay)
        return dict_cat

    elif category_name=="AUTO":
        nlp = spacy.load("C:/Users/NLP/Desktop/NER-Spacy/models/autoModel")
        doc_auto=nlp(text)
        category.key = "Category-1"
        category.value = "AutoMobiles"
        category.add(category.key, category.value)
        for key, value in mapStorage(doc_auto).items():
            entity.setdefault(value, []).append(key)
            if value == "TARGETVEH":
                category.setdefault("Category-2", []).append(key)
            if value == "ITEMTYPE":
                category.key = "Category-3"
                category.value = key
                category.add(category.key, category.value)
        categoryDisplay.key = "Category"
        categoryDisplay.value = category
        categoryDisplay.add(categoryDisplay.key, categoryDisplay.value)
        entityDisplay.key = "Entities"
        entityDisplay.value = entity
        entityDisplay.add(entityDisplay.key, entityDisplay.value)
        seo.setdefault("KeyWords", []).append(keyWordExtraction(text))
        seo.setdefault("Meta_Description", []).append(summarize(text))
        seo.setdefault("SEO_URL", []).append(re.sub('[^A-Za-z ]+', '',product_name).replace(" ","_"))
        seoDisplay.key = "SEO"
        seoDisplay.value = seo
        seoDisplay.add(seoDisplay.key, seoDisplay.value)
        dict_cat.update(categoryDisplay)
        dict_cat.update(entityDisplay)
        dict_cat.update(seoDisplay)
        return dict_cat

    else:
        return "not in mentioned category------------------------------"

def mapStorage(doc):
    dict_obj = my_dictionary()
    for entity in doc.ents:
        dict_obj.key = entity.text
        dict_obj.value = entity.label_
        dict_obj.add(dict_obj.key, dict_obj.value)
    return dict_obj

def keyWordExtraction(text):
    return (keywords(text, words=10)).replace("\n","  ")

@app.route("/reviews",methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def reviews():
    datafile = request.files.get('datafile', '')
    file = request.files['datafile']
    datafile.save('C:/Users/NLP/Desktop/NER-Spacy/data/' + file.filename)
    path = 'C:/Users/NLP/Desktop/NER-Spacy/data/' + file.filename
    validator = reviewModel()
    return (validator.process(path).to_json())

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
