from flask import Flask, render_template, request
from pymongo import MongoClient
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import codecs
import re

client = MongoClient()
col = client['flipkart']['data']

app= Flask(__name__)

url = 'https://www.flipkart.com/search?q=mobiles'
result = requests.get(url)
# print(result)

soup = BeautifulSoup(result.content, 'html.parser')
print(soup.text)

titles=soup.find_all('div', class_="_4rR01T")
ratings=soup.find_all('div', class_="_3LWZlK")
price=soup.find_all('div', class_="_25b18c")
mt=[]
mr=[]
mp=[]

for titles,ratings,price in zip(titles,ratings,price):
    mt.append(titles.text)
    mr.append(ratings.text)
    mp.append(price.text)

d = {'mt':mt, 'mr':mr, 'mp':mp}
model=pd.DataFrame(data=d)
model.to_csv("mobiledata.csv")

@app.route("/")
def Home_page():
    data=pd.read_csv("mobiledata.csv")
    rows=data.values.tolist()
    cols=data.values.tolist()
    data_dict = data.to_dict("records")

    col.insert_many(data_dict)

    return render_template("Sample.html", rows=rows, cols=cols)

if __name__=="__main__":
    app.run(debug=True)

