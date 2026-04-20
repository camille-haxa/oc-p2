import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#extraction du titre de la page
title = doc.title.string
print("title:", title)


# voir le code parsé par beautiful soup
print(doc)