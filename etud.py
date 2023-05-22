import requests
from bs4 import BeautifulSoup
import weasyprint
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from Screenshot import Screenshot
from hellowork import hellopdf
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
from xlrd import open_workbook

from xlutils.copy import copy

import xlwt
import json
import shutil
import time
import pandas as pd
from PyPDF2 import PdfWriter
from io import BytesIO
start = time.time()

# requete sur le site police emploi
print('Veuillez entrez le domaine professionnel de la recherche')
domaine = input()
print('Veuillez entrez la date d emission de l offre')
emission = input()
print('Veuillez entrez le code INSEE de la commune')
lieux = input()
print('Veuillez entrez le rayon de la recherche')
rayon= input()
print("entre le rang de début")
rangdeb= input()
rangdeb=int(rangdeb)
print("entre le rang de fin")
rangfin= input()
rangfin=int(rangfin)
#defini l'url de requete et permet de rechercher tous les domaines et tous les dates en rajoutant l'operateur tout
adressepe = "https://candidat.pole-emploi.fr/offres/recherche?"
if domaine=="tout" and emission=="tout":
    adressereq=adressepe+ "&lieux="+ lieux+"&rayon="+rayon+"&offresPartenaires=true"
elif domaine=="tout" and emission!="tout":
    adressereq=adressepe+ "&emission="+emission+"&lieux="+ lieux+"&rayon="+rayon+"&offresPartenaires=true"
elif emission=="tout" and domaine!="tout":
    adressereq=adressepe+ "&domaine="+domaine+"&lieux="+ lieux+"&rayon="+rayon+"&offresPartenaires=true"
else :
    adressereq=adressepe+"&domaine="+domaine+"&emission="+emission+"&lieux="+ lieux+"&rayon="+rayon+"&offresPartenaires=true"

# requete sur le site police emploi
if rangdeb == 0:
    response = requests.get(adressereq+"&range=0-19&tri=0")
    soup = BeautifulSoup(response.content, "html.parser")
    # trouver le nombre de résultat de la requête
    # trouver la classe qui contient le nombre de résultats
    soupe = soup.find(class_="zone-resultats")
    # trouver le texte entre les balises
    result = soupe.h1.get_text()
    # rechercher les nombres dans la réponse sous forme de listes
    nb_result_list = [int(temp) for temp in result.split() if temp.isdigit()]
    # enregistre le nombre de résultats sous forme de int
    nb_result = int(nb_result_list[0])
    print("il y a "+str(nb_result)+" offres")

# extraire les référence des offres (chercher tous les attributs li de la classe result
# defini la liste de reference de l'offre et la liste de reference clé
references = []
nb_result_reel = 1+rangdeb
index_offres = []
if rangdeb == 0:
    # cherche les <li class=result> rapporte le paramètre data-id-offre ajoute les résultats aux listes references et index_offres
    for li in soup.find_all("li", class_="result"):
        li.get("data-id-offre")
        references.append(li.get("data-id-offre"))
        index_offres.append(nb_result_reel)
        nb_result_reel = nb_result_reel + 1
    # faire un modulo du nombre de résultats
    nb_range = nb_result // 20
    # requête sur le site police emploi si les resultats sont > 20
    if nb_result > 20:
        nb_result_etat = 1
        # effectue une requete sur les range > 1
        while nb_result_etat <= nb_range:
            response = requests.get(adressereq+"&range="+ str(nb_result_etat * 20)
                + "-"
                + str(nb_result_etat * 20 + 19)
                +"&tri=0"
            )
            soup = BeautifulSoup(response.content, "html.parser")
            for li in soup.find_all("li", class_="result"):
                li.get("data-id-offre")
                references.append(li.get("data-id-offre"))
                index_offres.append(nb_result_reel)
                nb_result_reel = nb_result_reel + 1
            nb_result_etat = nb_result_etat + 1

rang_offre = 1+rangdeb
#fonction imprimer offre pdf
typecontrat=[]
def pepdf(idoffre, rang):
    # requete sur le site police emploi
    response = requests.get(
        'https://candidat.pole-emploi.fr/offres/recherche/detail/' + idoffre
    )
    # supprimer une partie de la réponse
    soup = BeautifulSoup(response.content, "html.parser")
    global contrat
    try:
        contrat= soup.find_all("dd")
        contrat=(contrat[0].contents)
        contrat=contrat[0].strip('\n')
    except:
        contrat="-"
        pass
    try:
        soupe = soup.find(class_="modal-details-offre")
        supprimer = soupe.find(class_="other-offers-container")
        
        if supprimer is not None:
            supprimer.clear()
        supprimer = soupe.find(class_="media-body media-middle")
        print(contrat)
        if supprimer is not None:
            supprimer.clear()
    except:
        pass
    # creer un pdf en utilisant la "soup" restante
    html = weasyprint.HTML(string=str(soupe))
    css = []
    #ajoute au css le nombre de page
    css.append(
        weasyprint.CSS(
            string="""
    @page {
    @top-center {
     content: "offre n°"""
            + str(rang)
            + """";
    }
    }"""
        )
    )
    css.append(weasyprint.CSS(filename="../none.css"))
    html.write_pdf(str(rang) + "-" + idoffre + ".pdf", stylesheets=css)


#recupere le chemin absolu du respertoire courant
chemin = os.path.abspath('./')

#initie les options chromedriver pour l'impression de pdf
chrome_options = webdriver.ChromeOptions()
settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}], "selectedDestinationId": "Save as PDF", "version": 2,"isHeaderFooterEnabled": False,"isLandscapeEnabled": False}
prefs = { "savefile.default_directory":chemin+"/pdfpar","download.default_directory":chemin+"/pdfpar","download.prompt_for_download": False, "download.directory_upgrade": True, "safebrowsing.enabled": True,'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
#verifie les prefs
#!print(prefs)
#definir le chemin des data chrome (verifier si cross platform) et ajoute au option de chromedriver
chromeuser=chemin+"/chrome-data"
chrome_options.add_argument('--user-data-dir='+chromeuser)
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
#lance le webdriver chromedriver.exe doit etre dans le repertoire
browser = webdriver.Chrome(options=chrome_options)
#creer le repartoire pour l'etude et change de repertoire
try:
    os.makedirs('./pdf'+"-"+lieux+"-"+emission+"jours"+"-"+domaine+"-rayon"+rayon+"km")
except FileExistsError:
    pass
os.chdir('./pdf'+"-"+lieux+"-"+emission+"jours"+"-"+domaine+"-rayon"+rayon+"km")

#defini les listes
urlpartenaire=[]
nompartenaire = []
#boucle sur la liste réferences verifie si offre police emploi et recupere le nom et l'url partenaire
if rangdeb==0:
    for x in references:
        print(x)
        print(rang_offre)
        #identifie les offres pe par les trois premier chiffre ( a changer) par si les trois dernier caracteres sont des lettres
        if x[:3] != '128' and x[:3] !='127' and x[:3] !='129' and x[:3] !='139' and x[:3] !='153' and x[:3] !='152' and x[:3] !='151' and x[:3] !='154':
            print("ce n'est pas une offre police emploi")
            # lance la page dans le webdriver
            browser.get("https://candidat.pole-emploi.fr/offres/recherche/detail/"+x)
            #time.sleep(1)
            browser.implicitly_wait(60)
            try:
                browser.find_element(By.ID, "detail-apply").click()
            except:
                print("soucis")
                browser.refresh()
                time.sleep(1)
                browser.find_element(By.ID, "detail-apply").click()
                pass
            nompar = browser.find_element(By.CSS_SELECTOR, "div.item div.media-body.media-middle h4")
            print(nompar.text)
            nompart=nompar.text
            
            lien = browser.find_element(By.ID, "idLienPartenaire").get_attribute('href')

    #si offre pole emploi ajoute pe sur la liste de nom
        else:
            lien="pe"
            nompart="pe"
        #ajoute le lien et le nom du partenaires aux listes
        urlpartenaire.append(lien)
        nompartenaire.append(nompart)
        #pepdf(x, rang_offre)
        #typecontrat.append(contrat)
        rang_offre = rang_offre + 1
    df = pd.DataFrame({'index_etud':index_offres,'reference de l offre':references,'nom du partenaire':nompartenaire,'url partenaire':urlpartenaire})
    df.to_csv("etud"+"-"+lieux+"-"+emission+"jours"+"-"+domaine+"-rayon"+rayon+"km"+".csv")
    for q in df.itertuples():
        print(q[1])
        print(q[2])
        pepdf(q[2], q[1])
        typecontrat.append(contrat)
    df = df.assign(typedecontrat=typecontrat)
    df.to_csv("etud"+"-"+lieux+"-"+emission+"jours"+"-"+domaine+"-rayon"+rayon+"km"+".csv")
if rangdeb != 0:
    df = pd.read_csv ("etud"+"-"+lieux+"-"+emission+"jours"+"-"+domaine+"-rayon"+rayon+"km"+".csv",index_col=0)

df= df.iloc[rangdeb:rangfin]
'''
for q in df.itertuples():
        print(q[1])
        print(q[2])
        pepdf(q[2], q[1])
        typecontrat.append(contrat)
'''
partpb=[]
partinter=[]
partsc=[]
partpourri=[]
print("fin de la génération des pdf Police emploi")
print("debut de la verification des cookies partenaire")



#defini le dictionnaire df2 sans les valeurs 'pe'
df2= df[(df['nom du partenaire'] != 'pe')]
#supprime les doublons de la colonn nom du partenaire
df2=df2.drop_duplicates(subset=['nom du partenaire'])
with open("../partco.txt", 'r') as file:
    partco = json.load(file)
with open("../partproblem.txt", 'r') as file:
    partpb = json.load(file)
with open("../partinter.txt", 'r') as file:
    partinter = json.load(file)
with open("../partsc.txt", 'r') as file:
    partsc = json.load(file)
#│affiche la valeur de la colonne 4 et 5 pour toutes les valaurs su dataframe
for v in df2.itertuples():
    #si la valeur de la colonne 4 n'est pas dans la liste partco
    if v[3] not in partco:
        partco.append(v[3])
        browser.get(v[4])
        print(v[1])
        print(v[2])
        print(v[3])
        print("Veuillez cliquer sur accepter les cookies dans le navigateur et validez en appuyant sur une touche")
        pb=input()
        
        if pb == "pb":
            partpb.append(v[3])
            partpourri.append(v[3])
            print("ajout de"+v[3]+"dans les partenaires manuels")
            
        elif pb == "sc":
            partsc.append(v[3])
            partpourri.append(v[3])
            print("ajout de"+v[3]+"dans les partenaires à capture ecran")
        elif pb =="inter":
            partinter.append(v[3])
            partpourri.append(v[3])
            print("ajout de"+v[3]+"dans les partenaires à interdire")
with open("../partproblem.txt", 'w') as file:
    json.dump(partpb,file)
with open("../partco.txt", 'w') as file:
    json.dump(partco, file)
with open("../partinter.txt", 'w') as file:
    json.dump(partinter, file)
with open("../partsc.txt", 'w') as file:
    json.dump(partsc, file)


#fin du test partenaire
#lance l'enregistrement manuel pour les partenaire problématiques
print("fin du test des partenaires")
print("debut des partenaires problématique")
#defini le dictionnaire df2 sans les valeurs 'pe'
df2= df[(df['nom du partenaire'] != 'pe')]
for w in df2.itertuples():
#verifie si string ou pas
    if isinstance(w[2], int):
        idoffr=str(w[2])
    else:
        idoffr=w[2]
#verifie si le pdf nexiste pas
    if os.path.exists(str(w[1])+'-offrepar-'+idoffr+'.pdf'):
        print ("fichier existe")
    else:
        if w[3] in partpb:
            print(w[1])
            print(w[2])
            print(w[3])
            browser.get(w[4])
            print("Veuillez appuyer sur une touche lors de la présentation correcte")
            input()
            browser.execute_script('window.print();')
            time.sleep(5)
            essai = os.getcwd()
            print(essai)
            listpdf = os.listdir('../pdfpar')
            print(listpdf)
            nom = listpdf[0]
            if isinstance(w[2], int):
                idoffr=str(w[2])
            else:
                idoffr=w[2]
            #renomme le fichier pdf et le met dans le bon repertoire nommage par valeur de chaque coionne dans le dataframe
            os.rename('../pdfpar/' + nom, '../pdfpar/' + str(w[1])+'-offrepar-'+idoffr+'.pdf')
            shutil.move('../pdfpar/' + str(w[1])+'-offrepar-'+idoffr+'.pdf', './')

        elif w[3] in partinter:
            print(w[3]+"pas de pdf")
        elif w[5] == "-":
            print(w[3]+"pas de pdf")
print("pdf des partenaire capture écran")
for w in df2.itertuples():
  if w[3] in partsc:
        print(w[1])
        print(w[2])
        print(w[3])
        ss = Screenshot.Screenshot()
        browser.get(w[4])
        if isinstance(w[2], int):
            idoffr=str(w[2])
        else:
            idoffr=w[2]
        image = ss.full_screenshot(browser, save_path=r'.' , image_name=str(w[1])+'-offrepar-'+idoffr+'.pdf', is_load_at_runtime=True,load_wait_time=3)
#save_path=r'.' 

print("pdf des autres partenaires")
#boucle sur la dataframe df2 - ca chercher chaque offre partenaire et imprime un pdf
print("pdf hellowork")
for w in df2.itertuples():
    if isinstance(w[2], int):
        idoffr=str(w[2])
    else:
        idoffr=w[2]
    #verifie si le pdf nexiste pas
    if os.path.exists(str(w[1])+'-offrepar-'+idoffr+'.pdf'):
        print ("fichier existe")
    else: 
        if w[3] not in partpb and w[3] not in partinter and w[3] not in partsc and w[3]=="HELLOWORK":
            if isinstance(w[2], int):
                idoffr=str(w[2])
            else:
                idoffr=w[2]
            hellopdf(w[4],w[1],idoffr)
        print("fin pdf hellowork")
        print("debut autres partenaires")
        if w[3] not in partpb and w[3] not in partinter and w[3] not in partsc and w[3]!="HELLOWORK":
    #va chercher la valeur de la colone 4
            print(w[1])
            print(w[2])
            print(w[3])
            browser.get(w[4])
            time.sleep(3)
            browser.execute_script('window.print();')
            time.sleep(1)
            #liste les fichier dans le repertoire pdfpar le renomme avec l'index
            
            listpdf = os.listdir('../pdfpar')
            nom = listpdf[0]
            if isinstance(w[2], int):
                idoffr=str(w[2])
            else:
                idoffr=w[2]
            #renomme le fichier pdf et le met dans le bon repertoire nommage par valeur de chaque coionne dans le dataframe
            os.rename('../pdfpar/' + nom, '../pdfpar/' + str(w[1])+'-offrepar-'+idoffr+'.pdf')
            shutil.move('../pdfpar/' + str(w[1])+'-offrepar-'+idoffr+'.pdf', './')
#boucle sur la dataframe df1 - fusionne tous les pdf
mergepdf = []
for z in df.itertuples():
    if isinstance(z[2], int):
        idoffr=str(z[2])
    else:
        idoffr=z[2]
    mergepdf.append(str(z[1])+"-"+idoffr+".pdf")
    if z[3] != 'pe' and z[3] not in partinter:
        mergepdf.append(str(z[1])+"-offrepar-"+idoffr+".pdf")
browser.close()
def ecrirexl():
    rb = open_workbook("../grilledebase.xls", formatting_info=True)
    
    wb = copy(rb)
    s = wb.get_sheet(0)
    s.portrait = 0
    s.paper_size_code = 9
    style = xlwt.easyxf('font: height 160;alignment: horizontal center, vertical center; borders: left thin, right thin, top thin, bottom thin')
    for z in df.itertuples():
        rangcell=z[0]+1
        s.write(rangcell,0,z[1], style)
        s.write(rangcell,1,z[2], style)
        if z[5].startswith('Contrat à durée déterminée'):
            cont="cdd"
                
        elif z[5].startswith('Contrat à durée indéterminée'):
            cont="cdi"
                
        elif z[5].startswith('Mission intérimaire'):
            cont='interim'
                
        else:
            cont=z[5]
        s.write(rangcell,  2, z[3], style)
        s.write(rangcell,3,cont, style)
        lign=4
        while lign < 18:
                s.write(rangcell,lign,"", style)
                lign=lign+1
        rangcellf =rangcell+1
        s.write(rangcell, 18, xlwt.Formula("OR((F"+str(rangcellf)+")=1;(G"+str(rangcellf)+")=1;(H"+str(rangcellf)+")=1;(I"+str(rangcellf)+")=1;(J"+str(rangcellf)+")=1;(K"+str(rangcellf)+")=1;(L"+str(rangcellf)+")=1;(M"+str(rangcellf)+")=1;(N"+str(rangcellf)+")=1;(O"+str(rangcellf)+")=1;(P"+str(rangcellf)+")=1;(Q"+str(rangcellf)+")=1;(R"+str(rangcellf)+")=1)"), style)
    wb.save("grilletud"+"-"+lieux+"-"+emission+"jours"+"-"+domaine+"-rayon"+rayon+"km-"+str(rangdeb)+"-"+str(rangfin)+".xls")


ecrirexl()
merger = PdfWriter()

for pdf in mergepdf:
    merger.append(pdf)


merger.write("resultcomp"+str(rangdeb)+"-"+str(rangfin)+".pdf")
merger.close()
if rangdeb==0:
    print("Police emploi affiche "+str(nb_result)+" mais on trouve "+str(nb_result_reel-1))
stop = time.time()
print('Elapsed time for the entire processing: {:.2f} s'.format(stop - start))
