import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#extraction du titre de la page
title = doc.title.string
print("title:", title)

#extraction url product page

#extraction upc
upc = doc.find("td")
print("upc:", upc.text)

#price including tax

#price excluding tax

#number avalaible

#extraction product description
product_description_div = doc.find(id="product_description")
product_description = product_description_div.find_next_sibling("p")
print("description produit:", product_description.text)

# voir le code parsé par beautiful soup
#print(doc)