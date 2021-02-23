import json
from vendoasg.vendoasg import Vendo
import configparser

config = configparser.ConfigParser()
config.read('vendo.ini')
# połączenie z bazą vendo
vendoApi = Vendo(config.get('vendo','vendo_API_port'))
vendoApi.logInApi(config.get('vendo','logInApi_user'),config.get('vendo','logInApi_pass'))
vendoApi.loginUser(config.get('vendo','loginUser_user'),config.get('vendo','loginUser_pass'))
produkty = [
'19661',
'19672',
'19654',
'19633',
'19634'
]

with open(f"kolory.txt", 'a') as plik_kolory:
    for produkt in produkty:
        plikjson = r'V:/indesign_baza/jsonFiles/'+str(produkt)+'.json'
        with open(plikjson) as f:
            data = list(json.load(f).items())
        lista_kolorow = (data[0][1]['lista_kolorow'])
        for kolor in lista_kolorow:
            kod = f'{produkt}-{kolor}'
            kod_query = vendoApi.getJson ('/Magazyn/Towary/Towar', {"Token":vendoApi.USER_TOKEN,"Model":{"Towar":{"Kod":kod}}})
            #print(f"kod - {kod_query}")
            try:
                numerID = kod_query["Wynik"]["Towar"]["ID"]
                print(f'{kod}-->{numerID}')
                plik_kolory.write(str(numerID) + "\n")
            except:
                print(kod_query)
