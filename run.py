#-*- coding: utf-8 -*-
import requests
import json
import configparser
import xlrd
from vendoasg.vendoasg import Vendo
config = configparser.ConfigParser()
config.read('vendo.ini')

# połączenie z bazą vendo
vendoApi = Vendo(config.get('vendo','vendo_API_port'))
vendoApi.logInApi(config.get('vendo','logInApi_user'),config.get('vendo','logInApi_pass'))
vendoApi.loginUser(config.get('vendo','loginUser_user'),config.get('vendo','loginUser_pass'))

###################################################################
def addTag(numerID,nazwa_wd,nowa_lista):
    response_data = vendoApi.getJson ('/json/reply/Magazyn_Towary_Aktualizuj', {"Token":vendoApi.USER_TOKEN,"Model":{
        "ID":numerID,
        "PolaUzytkownika":{
            "NazwaWewnetrzna":nazwa_wd ,
            "Wartosc":nowa_lista
            }
        }})
###################################################################
def checkWD():
    plik = xlrd.open_workbook("tagi.xls")
    strona = plik.sheet_by_index(0)
    total_cols = strona.ncols
    total_rows = strona.nrows    
    jezyki = ['pl','de','fr','en','cz']
    for jezyk in jezyki:
        i = 1
        nazwa_wd = f'tagi_{jezyk}'
        for e in range(total_rows-1):
            kod_towaru = strona.cell(i,0).value
            nowy_tag = str(strona.cell(i,1).value)
            if kod_towaru != "":
                if isinstance(kod_towaru, float):
                    kod_towaru = str(int(kod_towaru))
                if len(kod_towaru) == 4:
                    kod_towaru = "0" + kod_towaru
                print(kod_towaru)
                try:
                    kod_query = vendoApi.getJson ('/Magazyn/Towary/TowarRozszerzony', {"Token":vendoApi.USER_TOKEN,"Model":{
                        "ZwrocWartosciDowolne":True,
                        "Towar":{"Kod":kod_towaru}
                        }})
                    kod_query = kod_query["Wynik"]

                    numerID = kod_query["KartaTowaru"]["Towar"]["ID"]
                    wd = kod_query["WartosciDowolne"]
                    lista_wd = []
                    for w in wd:
                        lista_wd.append(w['Nazwa'])

                        if w['Nazwa'] == nazwa_wd:
                            lista_tagow = w['Wartosci'][0].replace(" ", "").split(",")
                            dodac = True
                            for tag in lista_tagow:
                                if nowy_tag in tag:
                                    dodac = False
                                    break
                            if dodac == True:
                                lista_tagow = (";").join(lista_tagow)

                                lista_tagow = lista_tagow +";"+ nowy_tag

                                addTag(numerID,nazwa_wd,lista_tagow)
                            else:
                                print("TAG już jest")
                    if nazwa_wd not in lista_wd:
                        addTag(numerID,nazwa_wd,nowy_tag)
                        print("BYŁO PUSTE")
                    i +=1
                except:
                    i +=1
                    continue






if __name__ == '__main__':
    checkWD()
# zakończenie pracy z bazą vendo
    vendoApi.logOutApi()
