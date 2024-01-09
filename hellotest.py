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
#print (list_of_scripts)
ana=str(list_of_scripts[8])
#print(ana)
sup = BeautifulSoup(ana,"html.parser")
#convertir en json
data = json.loads(sup.find('script', type='application/ld+json').text)
#print(data)
if data['@type']=='JobPosting':
    print(data['description'])
        #fait une page web avec titre et description
    web="<h1>"+str(data['title'])+"</h1>"+str(data['description'])
    
html = weasyprint.HTML(string=web)
css = []
css.append(weasyprint.CSS(filename="none.css"))
html.write_pdf("test.pdf", stylesheets=css)
