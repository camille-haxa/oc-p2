import requests
import re
from bs4 import BeautifulSoup
import csv

MAIN_URL = "https://books.toscrape.com"

#récupérer l'url et les infos d'une catégorie
url = "https://books.toscrape.com/catalogue/category/books/mystery_3/"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#extraire tous les livres de la catégorie
all_books = doc.find_all('article', class_='product_pod')
#print("all books:", all_books)
#TODO:extraire toutes les pages de la catégorie

#definir une fonction pour recuperer les details de chaque livre sur l'url de chaque livre
def book_details(book_url):
    response = requests.get(book_url).text
    book_doc = BeautifulSoup(response, "html.parser")

    upc = book_doc.find(text="UPC").next.text
    price_with_tax = book_doc.find(text="Price (incl. tax)").next.text
    price_no_tax = book_doc.find(text="Price (excl. tax)").next.text
    available_number = book_doc.find(class_="table table-striped").find_all('td')[5]
    stock = available_number.text.replace("In stock (","").replace(" available)","")
    product_description_div = book_doc.find(id="product_description")
    product_description = product_description_div.find_next_sibling("p").text
    category_list = book_doc.find(class_="breadcrumb").find_all('li')[-2]
    category = category_list.text.strip()
    rating = book_doc.find(class_="col-sm-6 product_main").find('p', class_="star-rating")['class'][1]
    image = book_doc.img['src'].replace("../../",MAIN_URL+"/")
    return {
        'upc': upc,
        'prix TTC': price_with_tax,
        'prix HT': price_no_tax,
        'number available': stock,
        'product description': product_description,
        'category': category,
        'rating': rating,
        'image url': image
    }

#faire une boucle pour récupèrer les infos de chaque livre
all_books_data = []
for book in all_books:
    book_title = book.h3.a['title']
    book_url = book.h3.a['href'].replace("../../../",MAIN_URL+ '/catalogue' '/')
    #appeler la fonction pour recuperer le detail de chaque livre sur l'url correspondante:
    book_detail = book_details(book_url)
    book_data = {
        'Title': book_title,
        'url': book_url,
        'upc': book_detail['upc'],
        'prix TTC': book_detail['prix TTC'],
        'prix HT': book_detail['prix HT'],
        'nombre en stock': book_detail['number available'],
        'description': book_detail['product description'],
        'catégorie': book_detail['category'],
        'rating': book_detail['rating'],
        'url image': book_detail['image url']
    }
    all_books_data.append(book_data)
print("books:", all_books_data)


# voir le code parsé par beautiful soup
#print(doc)