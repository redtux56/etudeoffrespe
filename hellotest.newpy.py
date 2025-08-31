import requests
from bs4 import BeautifulSoup
import weasyprint
import json
print("url")
url= input()
  
# requete sur le site hellowork
rep = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
# trouver tous les tags script
soup = BeautifulSoup(rep.text, "html.parser")
#print(soup)
list_of_scripts = soup.findAll("script")
print (list_of_scripts)
analy=list_of_scripts[6]
ana=str(list_of_scripts[6])
print(analy)
type_attr = analy.get('type', '').lower()
print(type_attr)
if type_attr == 'application/ld+json':
    print("Trouvé un script LD+JSON")
else:
    print("pas trouvé")

sup = BeautifulSoup(ana,"html.parser")
print (sup)
#convertir en json
data = json.loads(sup.find('script', type='application/ld+json').text)

print(data)
if data['@type']=='JobPosting':
    print(data['description'])
        #fait une page web avec titre et description
    web="<h1>"+str(data['title'])+"</h1>"+str(data['description'])
else:
    
    
html = weasyprint.HTML(string=web)
css = []
css.append(weasyprint.CSS(filename="none.css"))
html.write_pdf("test.pdf", stylesheets=css)
