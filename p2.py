import requests
import re
from bs4 import BeautifulSoup
import csv

MAIN_URL = "https://books.toscrape.com"

#récupérer infos pour 1 produit
url = "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#extraction du titre de la page
page_title = doc.h1.string
print("title:", page_title)

#extraction url product page
page_url = url
print("url:", page_url)

#extraction upc
upc = doc.find(text="UPC").next.text
print("upc:", upc)

#price including tax
price_with_tax = doc.find(text="Price (incl. tax)").next.text
print("prix TTC:", price_with_tax)

#price excluding tax
price_no_tax = doc.find(text="Price (excl. tax)").next.text
print("prix HT:", price_no_tax)

#number avalaible
available_number = doc.find(class_="table table-striped").find_all('td')[5]
stock = available_number.text.replace("In stock (","").replace(" available)","")
print("number available:", stock)

#extraction product description
product_description_div = doc.find(id="product_description")
product_description = product_description_div.find_next_sibling("p").text
print("description produit:", product_description)

#category
category_list = doc.find(class_="breadcrumb").find_all('li')[-2]
category = category_list.text.strip()
print("category:", category)

#review rating
rating = doc.find(class_="col-sm-6 product_main").find('p', class_="star-rating")['class'][1]
print("review rating:", rating)

#image url
image = doc.img['src'].replace("../../",MAIN_URL+"/")
print("image url:", image)

# créer une liste pour les en têtes
en_tete = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url' ]
#créer un nouveau fichier et instancier un objet writer
with open('data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(en_tete)
    #créer une ligne avec les données
    ligne = [page_url, upc, page_title, price_with_tax, price_no_tax, stock, product_description, category, rating, image]
    writer.writerow(ligne)
    
# voir le code parsé par beautiful soup
#print(doc)