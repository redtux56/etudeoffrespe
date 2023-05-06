import requests
from bs4 import BeautifulSoup
import weasyprint
import json
"""
print("url")
url= input()
print("rang")     
rang = input()
print("idoffre")     
idoffre = input()
"""

def hellopdf(url, rang, idoffre):
    # requete sur le site hellowork
    rep = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    # trouver tous les tags script
    soup = BeautifulSoup(rep.text, "html.parser")
    list_of_scripts = soup.findAll("script")
    #extrait le 9 élément du script
    ana=str(list_of_scripts[9])
    #parse l'element 
    sup = BeautifulSoup(ana,"html.parser")
    #convertir en json
    data = json.loads(sup.find('script', type='application/ld+json').text)
    if data['@type']=='JobPosting':
        print(data['description'])
        #fait une page web avec titre et description
        web="<h1>"+str(data['title'])+"</h1>"+str(data['description'])
       
    else:
        print("probleme")
        rep = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(rep.content, "html.parser")
        soupe = soup.find(class_="warning")
        web=soupe.get_text()
     # creer un pdf en utilisant la "soup" restante
    html = weasyprint.HTML(string=web)
    css = []
    css.append(weasyprint.CSS(filename="../none.css"))
    html.write_pdf(str(rang)+"-offrepar-"+idoffre+".pdf", stylesheets=css)

