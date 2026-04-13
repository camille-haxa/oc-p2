import requests

url = "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html"
page = requests.get(url)

# voir le code html source
print(page.content)