

import tkinter as tk
from tkinter import ttk, StringVar, NORMAL, CENTER, N, S, E, W, NO
import ini_nastaveni
import os
import configparser


from gtts import gTTS

from urllib.request import urlopen


def vypis_slovicka(self,seznam_slovicek):
        
        self.slovicka = tk.Toplevel()
        self.slovicka.attributes('-topmost', 'true')
        self.slovicka.title("Slovíčka lekce: " + self.akt_Lekce)

        self.nadpis = tk.Label(self.slovicka, text="Jazyk: " + self.akt_j + "\nUčebnice:" + self.akt_ucebnice + "\nLekce:" + self.akt_Lekce, font="Ariel 14", bg="grey")
        self.nadpis.grid(row=0, columnspan=3, sticky=W+E)
         
        self.tree_slovicka = ttk.Treeview(self.slovicka, column=("česky", "nečesky", "správně", "špatně"), height=20, selectmode='browse')
        self.tree_slovicka['show'] = 'headings' # schová první sloupec s identifikátorem
        self.tree_slovicka.grid(row=1, columnspan=3)
        
        self.tree_slovicka.heading("#0", text="#\n ")
        self.tree_slovicka.column("#0", width=0, stretch=NO, anchor='center')

        self.tree_slovicka.heading("česky", text="CZ\n ")
        self.tree_slovicka.column("česky", minwidth=0, width=270, stretch=NO, anchor=W)

        #self.tree_slovicka.heading("nečesky", text="nečesky\n ")
        self.tree_slovicka.heading("nečesky", text=self.akt_j.upper() + "\n")
        self.tree_slovicka.column("nečesky", minwidth=0, width=270, stretch=NO, anchor=W)

        self.tree_slovicka.heading("správně", text="SPRÁVNĚ\n ")
        self.tree_slovicka.column("správně", minwidth=0, width=65, stretch=NO, anchor='center')

        self.tree_slovicka.heading("špatně", text="ŠPATNĚ\n ")
        self.tree_slovicka.column("špatně", minwidth=0, width=65, stretch=NO, anchor='center')
                
        self.tree_slovicka.bind("<ButtonRelease-1>", lambda x:precti(self.tree_slovicka.item(self.tree_slovicka.focus())["values"][1],
                self.akt_jazyk.get(), self.slovnik.rychlost_cteni, self.slovnik.aj, self.slovnik.de, self.slovnik.fr, self.slovnik.it, self.slovnik.es, self.slovnik.ru))
       
        self.mez = tk.Label(self.slovicka, text="", height=1)
        self.mez.grid(row=2, column=0)

        self.Konec = tk.Button(self.slovicka, width=20, text="Konec", fg="red", command=self.slovicka.destroy)
        self.Konec.grid(row=3, column=0, sticky=W)

        pozice = 0
        for zaznam in seznam_slovicek:
            
            self.tree_slovicka.insert("", "end", text=pozice, values=(zaznam[1], zaznam[2], zaznam[3], zaznam[4]))
            pozice += 1

    
def precti(slovicko, jazyk, rychlost, aj, de, fr, it, es, ru):  
    # engine = pyttsx3.init("sapi5")

    if internet_on() == True:
        try:
            if rychlost == 0:
                rych = False
            else:
                rych = True
            if jazyk == "Aj":  # upravit podmínku podle názvu jazykového balíčku
                tts = gTTS(slovicko, lang='en', tld=aj, slow=rych)
                nazev_souboru = zamen_znak(slovicko)
                tts.save(nazev_souboru + '.mp3')
                os.startfile(nazev_souboru + ".mp3")

            elif jazyk == "Nj":  # upravit podmínku podle názvu jazykového balíčku
                tts = gTTS(slovicko, lang='de',tld=de, slow=rych)
                nazev_souboru = zamen_znak(slovicko)
                tts.save(nazev_souboru + '.mp3')
                os.startfile(nazev_souboru + ".mp3")

            elif jazyk == "Ru":    # upravit podmínku podle názvu jazykového balíčku
                tts = gTTS(slovicko, lang='ru', tld=ru, slow=rych)
                nazev_souboru = zamen_znak(slovicko)
                tts.save(nazev_souboru + '.mp3')
                os.startfile(nazev_souboru + ".mp3")

            elif jazyk == "Fr":  # upravit podmínku podle názvu jazykového balíčku
                tts = gTTS(slovicko, lang='fr', tld=fr, slow=rych)
                nazev_souboru = zamen_znak(slovicko)
                tts.save(nazev_souboru + '.mp3')
                os.startfile(nazev_souboru + ".mp3")

            elif jazyk == "Es":    # upravit podmínku podle názvu jazykového balíčku
                tts = gTTS(slovicko, lang='es', tld=es, slow=rych)
                nazev_souboru = zamen_znak(slovicko)
                tts.save(nazev_souboru + '.mp3')
                os.startfile(nazev_souboru + ".mp3")

            elif jazyk == "It":   # upravit podmínku podle názvu jazykového balíčku
                tts = gTTS(slovicko, lang='it', tld=it, slow=rych)
                nazev_souboru = zamen_znak(slovicko)
                tts.save(nazev_souboru + '.mp3')
                os.startfile(nazev_souboru + ".mp3")
        except:
            tk.messagebox.showwarning("Error_P0028", "Blokován přístup na Googl služby.")



def internet_on():
    config = configparser.ConfigParser()
    cesta_ini = ini_nastaveni.nacteni_ini()
    config.read(cesta_ini)

    if config["DEFAULT"]["pripojeni"] == "OF":
        return
    else:
        try:
            ip = ini_nastaveni.overeni_IP()
            urlopen(ip, timeout=2)
            return True
        except FileNotFoundError:
            tk.messagebox.showwarning("Error_P0029", "Nenalezen soubor s ověřovací IP adresou.")
        except:
            return False

def zamen_znak(nazev_souboru):
    nazev_souboru = nazev_souboru.replace("?", "")
    nazev_souboru = nazev_souboru.replace("/", "")
    nazev_souboru = nazev_souboru.replace("%", "")
    nazev_souboru = nazev_souboru.replace("*", "")
    nazev_souboru = nazev_souboru.replace(":", "")
    nazev_souboru = nazev_souboru.replace('"', "")
    nazev_souboru = nazev_souboru.replace("<", "")
    nazev_souboru = nazev_souboru.replace(">", "")
    nazev_souboru = nazev_souboru.replace(".", "")
    nazev_souboru = nazev_souboru.replace(",", "")
    nazev_souboru = nazev_souboru.replace(";", "")
    nazev_souboru = nazev_souboru.replace("=", "")
    return nazev_souboru
              