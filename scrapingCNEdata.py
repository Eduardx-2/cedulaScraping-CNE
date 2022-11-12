import requests
from bs4 import BeautifulSoup
import argparse
verde = '\033[32m'
blanco = '\033[37m'
rojo = '\033[31m'
magenta = '\033[35m'
amarillo = '\033[33m'


parser = argparse.ArgumentParser()
parser.add_argument("--list", type=str, help='Ingresa la ruta del txt con las cedulas', required=True)
args = parser.parse_args()

with open(args.list) as dataN:
   lineData = dataN.readlines()

def scraping():
    for lineCedula in lineData:
        finalCedula = lineCedula.strip()
        url_scraping = "http://www.cne.gob.ve/web/registro_electoral/ce.php?nacionalidad=V&cedula=%s" % (finalCedula)
        headers_scraping = {
           'User-Agent': "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"
        }
        global requests
        r_session = requests.get(url_scraping, headers=headers_scraping)

        htmlToparsing = BeautifulSoup(r_session.content, "html.parser")
        if r_session.status_code == 200:
           if 'Objeción: FALLECIDO (3)' in htmlToparsing.find_all('td')[20].text:
              print(f"{verde}LA PERSONA DE LA CEDULA {magenta}-> {rojo}{finalCedula}{rojo} {verde}FIGURA COMO FALLECIDA")
           elif 'RECOMENDACIONES' in htmlToparsing.find_all('td')[19].text:
              print(f"{verde}LA CEDULA {magenta}-> {amarillo}{finalCedula} {verde}NO PUEDE VOTAR/NO ES VALIDA")
           else:
               listStringhtml = []
               for contentString  in htmlToparsing.find_all('td')[10: 24]:
                   dataString = contentString.text
                   listStringhtml.append(dataString.strip())
               cedulaString = listStringhtml[1] 
               nombreString = listStringhtml[3]
               estadoString = listStringhtml[5] 
               municipioString = listStringhtml[7]
               print(f"{verde}CEDULA {magenta}-> {blanco}{cedulaString}\n{verde}NOMBRE {magenta}-> {blanco}{nombreString}\n{verde}ESTADO {magenta}-> {blanco}{estadoString}\n{verde}MUNICIPIO {magenta}-> {blanco}{municipioString}")
        else:
           print("SERVER CODE => [%d]" % r_session.status_code)



if __name__ == "__main__":
   scraping()
