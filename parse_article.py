import requests
from bs4 import BeautifulSoup
from abstract_ML_extract import get_summary

def parse(url):
    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, "html.parser")
    paras = soup.find_all('p')

    article = " ".join([str(para.text.strip()) for para in paras])

    return article
