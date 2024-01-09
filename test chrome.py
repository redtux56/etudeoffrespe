from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import json
chemin = os.path.abspath('./')

#initie les options chromedriver pour l'impression de pdf
chrome_options = webdriver.ChromeOptions()
settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}], "selectedDestinationId": "Save as PDF", "version": 2,"isHeaderFooterEnabled": True,"isLandscapeEnabled": False}
prefs = { "savefile.default_directory":chemin+"/pdfpar","download.default_directory":chemin+"/pdfpar","download.prompt_for_download": False, "download.directory_upgrade": True, "safebrowsing.enabled": True,'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
#verifie les prefs
#!print(prefs)
#definir le chemin des data chrome (verifier si cross platform) et ajoute au option de chromedriver
chromeuser=chemin+"/chrome-data"
cap = DesiredCapabilities.CHROME
cap = {'binary_location': chemin+"/chrome-win64/chrome-win64/chrome.exe"}

chrome_options.add_argument('--user-data-dir='+chromeuser)
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
#lance le webdriver chromedriver.exe doit etre dans le repertoire
browser = webdriver.Chrome(options=chrome_options,desired_capabilities=cap)
#creer le repartoire pour l'etude et change de repertoire
browser.get('http://www.google.com/');
