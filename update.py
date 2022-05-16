import zipfile
import os
import requests
import time
import glob
import shutil
from pathlib import Path

verze = "10.21"
adresa = "http://pyladiesplzen.wz.cz/SlovnikLite/"

print("Začínám aktualizovat.")

DOWN_ZIP = './.DownloadZip/'
EXTRAKT_ZIP = "./.ExtraktZip/"
TEMP = "./.TEMP/"


WORKING_FOLDERS = [DOWN_ZIP, EXTRAKT_ZIP, TEMP]

def vytvor_adresare(folders):
    """
    Ověří existenci adresářů
    pokud neexistují, vytvoří je
    """
    print("Ověřuji adresářovou strukturu.")
    time.sleep(1)

    try:
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
    except:
        input("""ERROR 1000:\n
                Není možné vytvořit adresářovou strukturu.\n
                Stisknutím klávesy 'Enter' aktualizaci ukončíte.""")
        os.startfile("SlovnikLite.exe")
        os._exit(0)


def nacti_adresu(cesta):
    try:
        with open(cesta, mode="r", encoding="utf-8") as cesta:
            cesta = cesta.read()
        cesta = cesta.strip()
        return cesta
    except FileNotFoundError:
        input("""ERROR 1001:\n
                Nebyl nalezen soubor s cestou na server aktualizací.\n
                Na stránkách vývojářů v sekci 'Kontakt' požádejte o možné řešení.\n
                Stisknutím klávesy 'Enter' aktualizaci ukončíte.""")
        os.startfile("SlovnikLite.exe")
        os._exit(0) 
        

def stahni_soubor(cesta_webu, DOWN_ZIP):
    """
    Stahne aktualizační soubor SlovnikLite.zip
    Jako parametr přebírá adresář pro uložení souborů
    """
    print("Stahuji potřebné soubory")
    time.sleep(1)

    url = cesta_webu + "SlovnikLite.zip"
    
    try:
        r = requests.get(url, allow_redirects=True)
        open(DOWN_ZIP + "SlovnikLite.zip", 'wb').write(r.content)
    except:
        input("""ERROR 1002:\n
                Nebylo navázené spojení se serverem.\n
                Na stránkách vývojářů v sekci 'Kontakt' požádejte o možné řešení.\n
                Stisknutím klávesy 'Enter' aktualizaci ukončíte.""")
        os.startfile("SlovnikLite.exe")
        os._exit(0)


def extract_data_file(filename, input_folder, output_folder):
    """
    Rozbalí aktualizační soubor.
    Jako parametr přebírá vstupní a výstupní adresář a název souboru
    """
    print("Rozbaluji nové soubory.")
    time.sleep(1)
    try:
        with zipfile.ZipFile(input_folder + '/' + filename,
                            'r') as zip_ref:
            zip_ref.extractall(output_folder)
    except:
        input("""ERROR 1003:\n
                Nepodařilo se rozbalit aktualizační soubory.\n
                Na stránkách vývojářů v sekci 'Kontakt' požádejte o možné řešení.\n
                Stisknutím klávesy 'Enter' aktualizaci ukončíte.""")
        os.startfile("SlovnikLite.exe")
        os._exit(0)


def vytvor_zalohu(TEMP):
    """
    Vytvoří zálohu starých souborů
    Jako parametr přebírá adresář pro uložení starých dat
    """
    print("Vytvářím zálohu starých souborů.")
    time.sleep(1)
    try:
        zaloha = glob.glob(os.path.join("*.*"))
        for soubor_zalohy in zaloha:
            shutil.copy2(soubor_zalohy, TEMP + soubor_zalohy)
    except:
        input("""ERROR 1004:\n
                Nepodařilo se vytvořit zálohu starých souborů.\n
                Na stránkách vývojářů v sekci 'Kontakt' nás informujte o tomto problému.\n
                Stisknutím klávesy 'Enter' aktualizaci ukončíte.""")
        os.startfile("SlovnikLite.exe")
        os._exit(0)


def smaz():   
    """
    Smaže staré, nepotřebné soubory
    """
    print("Mažu staré soubory.")
    time.sleep(1)
    try:       
        overeni_dat = glob.glob(os.path.join(".ExtraktZip/" + "SlovnikLite/", "*.*"))
        if overeni_dat == []:
            input("""ERROR 1006:\n
                    Nepodařilo se stáhnout nová data.\n
                    Stisknutím klávesy 'Enter' aktualizaci ukončíte.""")
            os.startfile("SlovnikLite.exe")
            os._exit(0)

        soubory_py = glob.glob(os.path.join("*.py"))
        soubory = glob.glob(os.path.join("*.*"))
        for soubor in soubory:
            time.sleep(2)
            if soubor in soubory_py:
                pass
            elif soubor.endswith("db_slovnik.sqlite"):
                pass
            elif soubor.endswith("update.exe"):
                pass
            elif soubor.endswith("vyslovnost.txt"):
                pass
            elif soubor.endswith("novinky.txt"):
                pass
            elif soubor.endswith("aktualizace.txt"):
                if soubor.endswith("web_novinky_aktualizace.txt"):
                    print("Mažu soubor:   ", soubor)
                    os.remove(soubor)
                else:
                    pass
            else:
                print("Mažu soubor:   ", soubor)
                os.remove(soubor)

    except:
        input("""ERROR 1005:\n
                Nepodařilo se smazat některé staré soubory, pravděpodobně Slovník používá zároveň jiný uživatel.\n
                Požádejte všechny uživatele o uzavření SlovníkuLite a ručně spusťte soubor 'update.exe' v adresáři SlovnikLite.\n
                Pokud se ani pak nepodaří tento problém odstranit, nemá cenu již Slovník spouštět,\n
                pravděpodobně budou scházet důležité soubory, kontaktujte nás na našich stránkách.\n
                Poradíme Vám, jak vrátit již smazané soubory.\n
                Stisknutím klávesy 'Enter' aktualizaci ukončíte.""")
        os._exit(0)


def nakopiruj_nove():
    """
    Nakopíruje nové rozbalené soubory.
    """
    print("Nahrávám nové soubory.")
    time.sleep(1)
    try:
        soubory = glob.glob(os.path.join(EXTRAKT_ZIP + "SlovnikLite/", "*.*"))
        for novy_soubor in soubory:          
            if novy_soubor.endswith("db_slovnik.sqlite"):
                pass
            elif novy_soubor.endswith("vyslovnost.txt"):
                pass
            elif novy_soubor.endswith("novinky.txt"):
                pass
            elif novy_soubor.endswith("aktualizace.txt") or novy_soubor.endswith("web_novinky_aktualizace.txt"):
                if novy_soubor.endswith("web_novinky_aktualizace.txt"):
                    print("Kopíruji nový soubor:  ", novy_soubor)
                    shutil.copy2(novy_soubor, "." )
                    time.sleep(1)
                else:
                    pass
            else:
                print("Kopíruji nový soubor:  ", novy_soubor)
                shutil.copy2(novy_soubor, "." )
                time.sleep(1)
                          
    except:
        input("""ERROR 1007:\n
                Nepodařilo se nakopírovat některé nové soubory.\n
                Požádejte všechny uživatele o uzavření SlovníkuLite a ručně spusťte soubor 'update.exe' v adresáři SlovnikLite.\n
                Pokud se ani pak nepodaří tento problém odstranit, nemá cenu již Slovník spouštět,\n
                pravděpodobně budou scházet důležité soubory, kontaktujte nás na našich stránkách.\n
                Poradíme Vám, jak vrátit již smazané soubory.\n
                Stisknutím klávesy 'Enter' aktualizaci ukončíte.""")
        os._exit(0)


def zapis(cesta_webu):
    """
    Zapíše do souboru 'akualizace.txt' aktuální číslo verze
    """
    print("Zapisuji číslo verze.")
    coding = "UTF-8"
    try:
        url = cesta_webu + "aktualizace.txt"
        target_url = url
        response = requests.get(target_url)
        data = str(response.text)
        data = data.replace("\r", "")
    except:
        print("ERROR 1002_Z", "Nebylo navázané spojení se serverem.")
        return

    try:
        with open("aktualizace.txt", mode="r", encoding=coding) as now:
            now = str(now.read())
        now = now.rstrip()      
    except FileNotFoundError:
        with open("aktualizace.txt", mode="w", encoding=coding) as prepsat:
            print(verze, file=prepsat)
    else:
        time.sleep(3)
        with open("aktualizace.txt", mode="r", encoding=coding) as now:
            now = str(now.read())
        now = now.rstrip()
        if data == now:
            pass
        else:
            with open("aktualizace.txt", mode="w", encoding=coding) as prepsat:
                print(data, file=prepsat)
                return


vytvor_adresare(WORKING_FOLDERS) # zkontroluje a vytvoří potřebnou adresářovou strukturu
adresa_serveru = nacti_adresu("web_novinky_aktualizace.txt")
stahni_soubor(adresa_serveru, DOWN_ZIP) # stahne aktualizační soubor SlovnikLite.zip
extract_data_file("SlovnikLite.zip", DOWN_ZIP, EXTRAKT_ZIP) # rozbalí aktualizační soubor SlovnikLite.zip
vytvor_zalohu(TEMP) # vytvoří zálohu starých souborů
smaz() # smaže staré soubory
nakopiruj_nove() # Nakopíruje nové rozbalené soubory
zapis(adresa_serveru) # Zapíše do souboru aktuální číslo verze
print("Aktualizace byla provedena. Spouštím program SlovnikLite.")
os.startfile("SlovnikLite.exe") # spustí SlovnikLite
time.sleep(2) # čeká 2 sekundy
os._exit(0) # ukončuje svůj proces
