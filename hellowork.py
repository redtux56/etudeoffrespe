import requests
from bs4 import BeautifulSoup
import weasyprint
import json

print("url")
adresse = input()
print("rang")     
rang = input()
def hellopdf(url, rang):
    # requete sur le site hellowork
    rep = requests.get(url)
    # trouver tous les tags script
    soup = BeautifulSoup(rep.text, "html.parser")
    list_of_scripts = soup.findAll("script")
    #extrait le 7 élément du script
    ana=str(list_of_scripts[7])
    #parse l'element 
    sup = BeautifulSoup(ana,"html.parser")
    #convertir en json
    data = json.loads(sup.find('script', type='application/ld+json').text)
    print(data)
    if data['@type']=='JobPosting':
        print(data['description'])
        #fait une page web avec titre et description
        web="<h1>"+str(data['title'])+"</h1>"+str(data['description'])
        # creer un pdf en utilisant la "soup" restante
        html = weasyprint.HTML(string=web)
        css = []
        css.append(weasyprint.CSS(filename="none.css"))
        html.write_pdf(str(rang) + "-hello.pdf", stylesheets=css)
    else:
        print("probleme")
        rep = requests.get(url)
        soup = BeautifulSoup(rep.content, "html.parser")
        soupe = soup.find(class_="warning")
        print(soupe.get_text())
hellopdf(adresse,rang)
