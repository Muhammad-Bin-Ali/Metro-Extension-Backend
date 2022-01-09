import requests
from bs4 import BeautifulSoup

def parse(url):
    try:
        response = requests.get(url)
        content = response.content

        soup = BeautifulSoup(content, "html.parser")
        paras = soup.find_all('p')

        article = " ".join([str(para.text.strip()) for para in paras])

        return article
    except:
        return False
