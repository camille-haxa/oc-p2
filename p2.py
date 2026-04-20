import requests
from bs4 import BeautifulSoup

#récupérer infos pour 1 produit
url = "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#extraction du titre de la page
title = doc.title.string
print("title:", title)

#extraction url product page
page_url = url
print("url:", page_url)

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

#category

#review rating

#image url
image = doc.img['src']
print("image url:", image)

# voir le code parsé par beautiful soup
#print(doc)