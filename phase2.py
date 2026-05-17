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
    return {
        'upc': upc,
    }

#faire une boucle pour récupèrer les infos de chaque livre
all_books_data = []
for book in all_books:
    book_title = book.h3.a['title']
    book_url = book.h3.a['href'].replace("../../../",MAIN_URL+ '/catalogue' '/')
    book_detail = book_details(book_url)
    book_data = {
        'Title': book_title,
        'url': book_url,
        'upc': book_detail['upc']
    }
    all_books_data.append(book_data)
print("books:", all_books_data)


# voir le code parsé par beautiful soup
#print(doc)