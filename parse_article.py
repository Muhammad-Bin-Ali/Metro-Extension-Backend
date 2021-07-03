import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.theguardian.com/sport/2021/jul/02/max-verstappen-formula-one-red-bull-lewis-hamilton-f1")
content = response.content

soup = BeautifulSoup(content, "html.parser")
paras = soup.find_all('p')

article = " ".join([str(para.text.strip()) for para in paras])

print(article)

