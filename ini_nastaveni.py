import configparser
from tkinter import messagebox
from ftplib import FTP


def nacteni_ini():   
    try:
        cesta_ini = "setup.ini"
        return cesta_ini
    except FileNotFoundError:
        
        return ""

def aktual():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()
    if cesta_ini == "":
        return "???"

    try:    
        config.read(cesta_ini)
        cislo_verze = config["DEFAULT"]["aktualizace"]
        if cislo_verze == "" or cislo_verze =="NONE":
            return "???" 
        else:
            return cislo_verze
    except:
        messagebox.showwarning("Error_P0010", "Nebyla nalezena hodnota verze.")
        return "???"

def vyslovnost_aj():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["PREDVOLBY"]["aj"]
    except:
        return "co.uk"

def vyslovnost_de():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["PREDVOLBY"]["de"]
    except:
        return "de"

def vyslovnost_fr():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["PREDVOLBY"]["fr"]
    except:
        return "fr"

def vyslovnost_it():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["PREDVOLBY"]["it"]
    except:
        return "it"

def vyslovnost_es():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["PREDVOLBY"]["es"]
    except:
        return "es"

def vyslovnost_ru():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["PREDVOLBY"]["ru"]
    except:
        return "ru"

def URL():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["DEFAULT"]["web_novinky_aktualizace"]
    except:
        return ""


def WEB():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["DEFAULT"]["web"]
    except:
        return ""


def novinky_ulozene_ini():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        return config["DEFAULT"]["novinky_ulozene"]
    except:
        return "???"


def ulozit_novinku(stazeno):
    config = configparser.ConfigParser() # vytvo??en?? instance
    cesta_ini = nacteni_ini() # ov????en?? existence .ini souboru
    config.read(cesta_ini)  # na??ten?? souboru
    config['DEFAULT']['novinky_ulozene'] = stazeno   # update polo??ky
    with open(cesta_ini, 'w') as configfile:    # save
        config.write(configfile)

def overeni_IP():
    config = configparser.ConfigParser() # vytvo??en?? instance
    cesta_ini = nacteni_ini() # ov????en?? existence .ini souboru
    config.read(cesta_ini)  # na??ten?? souboru
    return config["DEFAULT"]["ip"]

def out():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()

    try:
        config.read(cesta_ini)
        out = float(config["DEFAULT"]["timeout"])
        if out == "":
            return float(2)
        else:
            return out
    except:
        messagebox.showwarning("Error_P0011", """Nebyl nalezen konfigura??n?? soubor.
                                        \nn??kter?? ????sti programu mohou zp??sobit neo??ek??vanou chybu
                                        \ndoporu??ujeme program nepou????vat a kontaktovat v??voj????e na adrese
                                        \npetr.f@pyladiesplzen.wz.cz""")
        return float(2)

def ftpHost():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()
    config.read(cesta_ini)
    return config["DEFAULT"]["ftp_host"]

def ftpName():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()
    config.read(cesta_ini)
    return config["DEFAULT"]["ftp_name"]


def ulozeni_uzivatele_do_ini(uzivatel):
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()
    config.read(cesta_ini)
    if config["DEFAULT"]["mac_"] == uzivatel:
        pass
    else:
        config["DEFAULT"]["mac_"] = uzivatel
        with open(cesta_ini, 'w') as configfile2:
            config.write(configfile2)


def _MAC():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()
    config.read(cesta_ini)
    return config["DEFAULT"]["mac_"]

def pripojeni():
    config = configparser.ConfigParser()
    cesta_ini = nacteni_ini()
    config.read(cesta_ini)
    try:
        ftp = FTP(ftpHost(), timeout=2)  # connect to host, default port
        ftp.login(ftpName(), 'Touskov33033')  # user , passwd
        ftp.close()
        config["DEFAULT"]["pripojeni"] = "ON"
        with open(cesta_ini, 'w') as configfile:  # save
            config.write(configfile)
    except:
        config["DEFAULT"]["pripojeni"] = "OF"
        with open(cesta_ini, 'w') as configfile:  # save
            config.write(configfile)