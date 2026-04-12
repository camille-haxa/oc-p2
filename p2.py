import requests

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page = requests.get(url)

# voir le code html source
print(page.content)