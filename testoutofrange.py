import os
import os
import shutil
import re

def clean_filename(filename):
    # Remplace les caractères interdits par un underscore
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

listpdf = os.listdir('./pdfpar')
nom = listpdf[0]
print(nom)
nomclean=clean_filename(nom)
print(nom)

os.rename(f'./pdfpar/{nom}', f'./pdfpar/{nomclean}')
