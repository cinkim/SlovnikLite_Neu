

from getmac import get_mac_address as gma
from ftplib import FTP
import ini_nastaveni
import os
import requests

url_uzivatelu = "http://pyladiesplzen.wz.cz/SlovnikLite/uzivatele.txt"

def uzivatel_Slovniku(uziv):
    try:
        mac = gma()
        user_name = os.getlogin()
        pc_name = os.getenv("COMPUTERNAME")
        uziv = mac + ";___" + pc_name + ";___" + user_name + ";___" + uziv
        return uziv     
    except:
        pass

def overeni_na_netu(target_url, uzivatel, out):
    response = requests.get(target_url, timeout=out)
    data = str(response.text)
    data = data.replace("\r", "")
    if uzivatel in data:
        return
    else:
        pripojeni_ftp_a_stazeni_zaznamu(uzivatel, out)


def pripojeni_ftp_a_stazeni_zaznamu(uzivatel, out):   
    with open("docasny.txt", mode="w", encoding="utf-8") as docas:
        print(uzivatel, file=docas)

    with open("docasny.txt", "rb") as pridat:
        ftp = FTP(ini_nastaveni.ftpHost(), timeout=out)     # connect to host, default port
        ftp.login(ini_nastaveni.ftpName(),'Touskov33033')  # user , passwd 
        ftp.encoding = "utf-8"
        ftp.cwd('SlovnikLite')          # change into "SlovnikLite" directory
        ftp.storbinary('APPE uzivatele.txt', pridat, 1)
        ftp.close()


    try:
        os.remove("docasny.txt") 
    except FileNotFoundError:
        pass






def prog(uziv):
    out = ini_nastaveni.out()
    uzivatel = uzivatel_Slovniku(uziv)
    ini_nastaveni.ulozeni_uzivatele_do_ini(uzivatel)
    overeni_na_netu(url_uzivatelu, uzivatel, out)
