import requests
import re
from bs4 import BeautifulSoup
import csv

MAIN_URL = "https://books.toscrape.com"

#definir une fonction pour recuperer les details de chaque livre sur l'url de chaque livre
def book_details(book_url):
    response = requests.get(book_url).text
    book_doc = BeautifulSoup(response, "html.parser")

    book_title = book.h3.a['title']
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
header = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url' ]
def ecriture_csv(data, filename):
    # créer un nouveau fichier et instancier un objet writer avec l'option append
    with open('all_data.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        # vérifier si fichier csv existe déjà et si non écrire le header
        if csv_file.tell() == 0:
            writer.writerow(header)
    #créer une ligne avec les données
        for book in data:
            writer.writerow([book['url'], book['upc'], book['title'], book['prix TTC'], book['prix HT'], book['number available'], book['product description'], book['category'], book['rating'], book['image url']])
            

#récupérer l'url de chaque catégorie
site_url = MAIN_URL
main_doc = requests.get(site_url).text
main_soup = BeautifulSoup(main_doc, "html.parser")
cat_list = main_soup.find('ul', class_="nav nav-list").find('ul').find_all('li')
print(cat_list)





#trouver la liste des catégories

for cat in cat_list:
    cat_url = MAIN_URL+ cat.a['href']
print(cat_url)

