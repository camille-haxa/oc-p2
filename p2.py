import requests
from bs4 import BeautifulSoup

#récupérer infos pour 1 produit
url = "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#extraction du titre de la page
title = doc.h1.string
print("title:", title)

#extraction url product page
page_url = url
print("url:", page_url)

#extraction upc
upc = doc.find(text="UPC")
print("upc:", upc.next.text)

#price including tax
price_including_tax = doc.find(text="Price (incl. tax)")
print("prix TTC:", price_including_tax.next.text)

#price excluding tax
price_excluding_tax = doc.find(text="Price (excl. tax)")
print("prix HT:", price_excluding_tax.next.text)

#number avalaible
available_number = doc.find(class_="table table-striped").find_all('td')[5]
stock = available_number.text.replace("In stock (","").replace(" available)","")
print("number available:", stock)

#extraction product description
product_description_div = doc.find(id="product_description")
product_description = product_description_div.find_next_sibling("p")
print("description produit:", product_description.text)

#category
category_list = doc.find(class_="breadcrumb").find_all('li')[2]
print("category:", category_list.text.strip())

#review rating
#rating = doc.find(class_="col-sm-6 product_main").find_all('p')[2]
#print("review rating:", rating)

#image url
image = doc.img['src']
print("image url:", image)

# voir le code parsé par beautiful soup
#print(doc)