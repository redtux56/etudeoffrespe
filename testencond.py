import os, unicodedata
essai = os.getcwd()
print(essai)
listpdf = os.listdir('./pdfpar')
print(listpdf)
nom_simplifie = unicodedata.normalize('NFKD', listpdf[0]).encode('ascii', 'ignore').decode('ascii')
print(nom_simplifie)
