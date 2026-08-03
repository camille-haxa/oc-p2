Ce projet permet de télécharger automatiquement ([*scraper*](https://fr.wikipedia.org/wiki/Web_scraping)) des donnés depuis le site [Books to Scrape](https://books.toscrape.com/)  
Il contient les scripts pour 4 étapes différentes, le script final a exécuter est **phase4.py**  
Ce script final permet de télécharger en local sur votre ordinateur un ensemble de données au format csv ainsi qu'un dossier contenant les images de couverture de chaque livre (identifiable a leur numéro unique upc) au format jpg  

### Pour utiliser le script 

- **cloner le projet**  
``git clone https://github.com/camille-haxa/oc-p2.git``

- **installer les outils de gestion d'environnement virtuel python**   
``python -m venv env``  

- **créer l'envirronnement python et installer les paquets requis**   
``pip install -r requirements.txt``   
- **activer l'environnement virtuel**  
``source env/bin/activate``

- **exécuter le script**   
``python3 phase4.py``  






