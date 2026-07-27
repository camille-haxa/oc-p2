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
    product_description = product_description_div.find_next_sibling("p").text if product_description_div else "Description non disponible"
    category_list = book_doc.find(class_="breadcrumb").find_all('li')[-2]
    category = category_list.text.strip()
    rating = book_doc.find(class_="col-sm-6 product_main").find('p', class_="star-rating")['class'][1]
    image_path = book_doc.img['src'].replace("../../",MAIN_URL+"/")
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
        'image url': image_path
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

#definir une fonction pour telecharger les images des livres
image_filename =  f"{book_details['upc']}.jpg"
image_file = os.path.join(images_folder, image_filename)
def download_image(image_path, image_file):
    image_doc = requests.get(image_path)
    if image_doc.status_code == 200:
        with open(image_file, 'wb') as file:
            file.write(image_doc.content)

#créer dossier contenant les images de chaque livre
books_images_dir = 'books_images'
os.makedirs(books_images_dir, exist_ok=True)

#récupérer l'url de chaque catégorie
site_url = MAIN_URL
main_doc = requests.get(site_url).text
main_soup = BeautifulSoup(main_doc, "html.parser")
cat_list = main_soup.find('ul', class_="nav nav-list").find('ul').find_all('li')
print(cat_list)

#construire l'url de chaque catégorie
for cat in cat_list:
    cat_url = MAIN_URL+ '/'+ cat.a['href'].removesuffix("index.html")
    #requests get sur l'url de la catégorie
    doc = requests.get(cat_url).text
    soup = BeautifulSoup(doc, "html.parser")

    #trouver le nombre de pages:
    #condition pour différencier si 1 seule page ou plusieurs
    page_urls = []   
    if soup.find(class_='current') == None:
        page_url = f"{cat_url}index.html"
        page_urls.append(page_url)
        print(page_url, page_urls)
    else :
        page_numbers = int(soup.find(class_='current').text.split()[-1])
        print(page_numbers)
        #contruire l'url des pages de la catégorie:
        page = 1
        for i in range (1, page_numbers+1):
            page_url = f"{cat_url}page-{i}.html"
            page_urls.append(page_url)
            print(page_url, page_urls)
        
    #passer sur toutes les pages de toutes les catégorie en bouclant sur la liste page_urls créée précédemment
    for p in page_urls:
        page_doc = requests.get(p).text
        page_soup = BeautifulSoup(page_doc, "html.parser")
        #extraire tous les livres de la catégorie
        all_books = page_soup.find_all('article', class_='product_pod')
        

        #faire une boucle pour récupèrer les infos de chaque livre
        all_books_data = []
        for book in all_books:
            book_url = book.h3.a['href'].replace("../../../",MAIN_URL+ '/catalogue' '/')
            #appeler la fonction pour recuperer le detail de chaque livre sur l'url correspondante:
            book_data = book_details(book_url)
            all_books_data.append(book_data)

            #appeler la fonction image_download sur l'url de chaque livre
            download_image(book_data['image url'])
            

        #appeler la fonction csv sur les données de chaque livre pour créer un fichier contenant les données de chaque livre
        ecriture_csv(all_books_data, "all_data.csv")
