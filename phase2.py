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
        'title': book_title,
        'url': book_url,
        'upc': upc,
        'prix TTC': price_with_tax,
        'prix HT': price_no_tax,
        'number available': stock,
        'product description': product_description,
        'category': category,
        'rating': rating,
        'image url': image
    }

#definir une fonction pour inscrire les données dans un fichier csv
def ecriture_csv(data, filename):

#créer un nouveau fichier et instancier un objet writer
    with open('cat_data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url' ])
    #créer une ligne avec les données
        for book in data:
            writer.writerow([book['url'], book['upc'], book['title'], book['prix TTC'], book['prix HT'], book['number available'], book['product description'], book['category'], book['rating'], book['image url']])


#faire une boucle pour récupèrer les infos de chaque livre
all_books_data = []
for book in all_books:
    book_title = book.h3.a['title']
    book_url = book.h3.a['href'].replace("../../../",MAIN_URL+ '/catalogue' '/')
    #appeler la fonction pour recuperer le detail de chaque livre sur l'url correspondante:
    book_data = book_details(book_url)
    
    all_books_data.append(book_data)
#print("books:", all_books_data)

ecriture_csv(all_books_data, "cat_data.csv")


# voir le code parsé par beautiful soup
#print(doc)