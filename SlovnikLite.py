# hlavni program

import tkinter as tk
from tkinter import ttk, StringVar,  N, E, W
from tkinter import NO, VERTICAL
import tkinter.messagebox
from tkinter import messagebox

import os
import win32com.client as win32

import webbrowser

import requests
import time
import shutil
import zipfile
import ini_nastaveni

import new_student as ns
import prace_s_db
import nastaveni
import testovani as ts
import vysledky as vys
import pridat_sl as sl
import vypsat_sl as v_sl
import pridat_uc as uc
import pridat_lek as lek
import import_slovicek as im
import _ftp

class slovnik:

    def __init__(self):
        
        self.out = ini_nastaveni.out()
        self.internet_on = ini_nastaveni.pripojeni()
        self.cislo_verze = ini_nastaveni.aktual()
        self.uklidit()
        self.seznam_studentu = [] # vrácený seznam studentů z db
        self.nacti_studenty() # načte z db seznam studentů
        self.jazyky_studenta = [] # seznam jazyků aktuálního studenta
        self.akt_jazyk = "" # aktuální jazyk k testování zvoleného studenta
        # self.akt_U = ""
        self.seznam_ucebnic = [] # seznam učebnic studenta/jazyku
        self.nova_sl = [] # nová slovíčka k uložení do db

        self.k_testovani = [] # načtená všechna slovíčka z db zvolené lekce
        self.testuj = [] # vybraná slova k testování 
        self.netestuj = []# vyřazená slova z testování
        self.aktualni_slovo = 0 # aktuálně testované slovo

        self.vysledky_pro_ulozeni_do_db = [] # konečný řetězec pro uložení výsledku do db

        self.pocet_k_testu = None # počet slovíček v rámci jednoho testu
        self.pocet_spravnych = None # počet správných odpovědí pro vyřazení slovíčka
        self.pocet_kol_testu = None # počet kol testování se stejnými slovíčky
        self.typ_prekladu = None # "směr" překladu: 1=cz/cizí, 2=cizí/cz, 3=míchat
        self.testovat_jen_spatne = None  # Testovat jen ze slovíček se špatnou odpovědí>3,   1=ano, 2=ne
        self.rychlost_cteni = 0 # Nastavení rychlosti pro čení Aj slovíček, 0=pomalu/1=rychle
        
        
        self.vysledky_db = [] # vysledky spravnych sloviček pro uložení do db
        self.vysledky = [] # průběžné výsledky do výpisu na obrazovku
        
        self.pocet_sl_pro_procenta = 0 # mezivýpočet pro procentuelní vyhodnocení testu
        self.pocet_spravnych_pro_procenta = 0 # mezivýpočet pro procentuelní vyhodnocení testu
        self.zbyva_k_testovani = 0
        self.aj = ini_nastaveni.vyslovnost_aj()
        self.de = ini_nastaveni.vyslovnost_de()
        self.fr = ini_nastaveni.vyslovnost_fr()
        self.it = ini_nastaveni.vyslovnost_it()
        self.es = ini_nastaveni.vyslovnost_es()
        self.ru = ini_nastaveni.vyslovnost_ru()




    """__________Uklidit______________"""
    def uklidit(self):
        """
        Smaže update soubory po aktualizaci probramu.
        """

        try:
            os.remove("update.exe")     # smaže update soubor pro starou verzi
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

        try:
            os.remove("update_ini.exe")     # smaže update soubor pro .ini verzi
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    """____________________________novinky______________"""
    def novinky(self):
        """
        Vyhledá na WEBU vzdáleně zdělené informace,
        porovná s již uloženou informací v .ini souboru,
        v případě shody informaci ignoruje, v případě rozdílu
        zobrazí informaci a aktualizuje zprávu v .ini souboru.
        Ignoruje prázdný soubor s žádnou zprávou na webu.
        """

        try:
            url = ini_nastaveni.URL() + "novinky.txt"   # načte cestu z ini
            if url == "novinky.txt":
                return
        except:
            tk.messagebox.showwarning("Error_N0001", "Soubor s webovou adresou nenalezen.\nObraťte se na vývojáře.")
            return


        target_url = url
        response = requests.get(target_url, timeout=self.out)   # načtení novinky
        response.encoding = "utf-8"     # nastavení kódování
        data = str(response.text)       # uložení
        novinky_stazene = data.replace("\r", "").strip() # ošetření znaků stažené novinky
        novinky_stazene = novinky_stazene.replace("\ufeff", "") # ošetření znaků stažené novinky
        novinky_ulozene = ini_nastaveni.novinky_ulozene_ini()   # načtení uložené novinky

        if novinky_stazene == "":   # když na webu prázdný soubor s informací - nedělej nic
            return
        elif novinky_stazene == "\ufeff":   # když na webu "\ufeff" - nedělej nic
            return
        elif novinky_stazene == novinky_ulozene:    # když na webu stejné s uloženou - nedělej nic
            return
        else:
            tk.messagebox.showwarning("Oznámení", novinky_stazene)  # zobrazení informace
            ini_nastaveni.ulozit_novinku(novinky_stazene)   # uložení informace do ini



    """___________________Aktualizace___________________"""
    def aktualizace(self):
        try:
            url = ini_nastaveni.URL() + "aktualizace.txt"   # načte cestu z ini
            if url == "aktualizace.txt":
                return
        except:
            tk.messagebox.showwarning("Error_A0001", "Soubor s webovou adresou nenalezen.\nObraťte se na vývojáře.")
            return

        target_url = url
        response = requests.get(target_url, timeout=self.out)   # načtení verze aktualizace
        data = str(response.text)                               # uložení
        data = data.replace("\r", "")                           # ošetření znaků stažené novinky

        if self.cislo_verze == "???":
                return

        if float(data) == float(self.cislo_verze):  # v případě shody verzí - nic
            pass
        else:         
            if float(data) > float(self.cislo_verze):   # v případě vyšší verze - zeptá se na aktualizaci
                if messagebox.askyesno("Nalezena nová verze programu.", "Byla nalezena nová verze programu\nchtete spustit aktualizaci?") == True:
                    self.upgrade()  # stažení aktualizačního souboru
                    time.sleep(1)
                    os.startfile("update_ini.exe")  # spuštění aktualizačního souboru
                    time.sleep(1)
                    os._exit(0)     # ukončení Slovníku
                else:
                    pass     # odmítnutá aktualizace

            elif float(data) < float(self.cislo_verze):
                tk.messagebox.showwarning("???", "Nejde aktualizovat na nižší verzi programu.")

    def upgrade(self):
        """
        Stažení a rozbalení aktualizačního souboru
        """
        DOWN_ZIP = "./.DownloadZip/"
        EXTRAKT_ZIP = "./.ExtraktZip/"

        WORKING_FOLDERS = [DOWN_ZIP, EXTRAKT_ZIP]

        for folder in WORKING_FOLDERS:  # příprava adresářové struktury pro rozbalení aktualizace
            if not os.path.exists(folder):
                os.makedirs(folder)

        url = ini_nastaveni.URL() + "update_ini.zip"

        try:
            r = requests.get(url, allow_redirects=True, timeout=self.out)
            open(DOWN_ZIP + "update_ini.zip", 'wb').write(r.content)
        except:
            tk.messagebox.showwarning("Error_U0001", "Nebylo navázené spojení se serverem.\nNa stránkách vývojářů v sekci 'Kontakt' požádejte o možné řešení.")
            return

        with zipfile.ZipFile(DOWN_ZIP + '/' + "update_ini.zip", 'r') as zip_ref:
            zip_ref.extractall(EXTRAKT_ZIP)

        shutil.copy2(EXTRAKT_ZIP + "update_ini.exe", ".")


    """_____________ načtení všech studentů po startu aplikace ______________"""
    def nacti_studenty(self):
        try:
            prace_s_db.overeni_sl()
        except:
            self.seznam_studentu = []
        else:
            self.seznam_studentu = prace_s_db.seznam_studentu()
            for filename in os.listdir('.'):
                if filename.endswith('.mp3'):
                    os.remove(filename) 



class slovnikGUI(tk.Frame):

    def __init__(self, parent, slovnik):
        super().__init__(parent)
        self.parent = parent
        self.slovnik = slovnik
        self.parent.title(self.slovnik.cislo_verze)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets_uzivatele()
        if slovnik.internet_on == "OF":
            tk.messagebox.showwarning("Error_P0000", "Nebylo navázané spojení se serverem.")
        else:
            try:
                self.slovnik.aktualizace()
                self.slovnik.novinky()
            except requests.exceptions.ConnectionError:
                tk.messagebox.showwarning("Error", "Nebylo navázané spojení se serverem.")

            self.zobraz()
            self.akt_ucebnice = ""

    

    """__________________ vytvoří pole se seznamem studentů _________________________________________"""
    def create_widgets_uzivatele(self):

        self.uzivatel = tk.Label(root, text="", font="Arial 16", fg="red")
        self.uzivatel.grid(row=0, columnspan=4, sticky=W+E)

        self.studenti = tk.LabelFrame(root, text="Studenti", font="Arial 8")
        self.studenti.grid(row=1, column=0, sticky=N)

        self.scrollbar_studenti = tk.Scrollbar(self.studenti, orient=VERTICAL)
        self.studenti_ListBox = tk.Listbox(self.studenti, width=21, yscrollcommand=self.scrollbar_studenti.set, height=15, font="Arial 8")
        self.studenti_ListBox.bind( "<ButtonRelease-1>", self.nacti_studenta)  # po kliknutí se načtou slovíčka z dané učebnice 
        self.studenti_ListBox.grid(row=2, column=0, sticky=W)

        self.button_new_st = tk.Button(root, text="Nový student", command=self.vytvor_top_okno_novy_student, font="Arial 8", width=20)
        self.button_new_st.grid(row=10, column=0, sticky=W)

        self.button_Konec = tk.Button(root, text="Konec", command=self.on_close, fg="red", font="Arial 8", width=20)
        self.button_Konec.grid(row=11, column=0, sticky=W)

        

    """________________________ vytvoří pole jazyků, podle zvoleného studenta ___________________"""
    def create_widgets_jazyk(self):      
        pozice = 1 # pozice řádky v rámci skupiny RadioButtonu
        self.akt_jazyk = StringVar()

        try:
            self.jazyky.destroy()
            self.ucebnice.destroy()
            self.Lekce.destroy()
        except AttributeError:
            pass

        self.jazyky = tk.LabelFrame(root, text="Testovat jazyk", font="Arial 8")
        self.jazyky.grid(row=1, column=1, sticky=N)

        for jazyk in self.jazyky_studenta:
            self.j_studenta = tk.Radiobutton(self.jazyky, indicatoron=0, text=jazyk, variable=self.akt_jazyk, command=self.nacti_ucebnice, value=jazyk, width = 20)
            self.j_studenta.grid(row=pozice, column=0, sticky=W)
            if jazyk == self.akt_jazyk:
                self.j_studenta.select()
                
            else:
                self.j_studenta.deselect()
            pozice = pozice + 1

    """___________________________ vytvoří pole se seznamem učebnic podle zvoleného studenta a jazyka ________________________"""
    def create_widgets_ucebnice(self):       
        try:
            self.ucebnice.destroy()
            self.Lekce.destroy()
        except AttributeError:
            pass
        self.ucebnice = tk.LabelFrame(root, text="Učebnice", font="Arial 8")
        self.ucebnice.grid(row=1, column=2, rowspan=11, sticky=N)

        self.scrollbar_ucebnice = tk.Scrollbar(self.ucebnice, orient=VERTICAL)

        self.ucebnice_ListBox = tk.Listbox(self.ucebnice, width=21, yscrollcommand=self.scrollbar_ucebnice.set, height=15, font="Arial 8")
        self.ucebnice_ListBox.bind( "<ButtonRelease-1>", self.nacti_lekce, self.export_ucebnice) 
        
        self.ucebnice_ListBox.grid(row=2, column=2, sticky=W)

        self.button_pridat_ucebnici = tk.Button(self.ucebnice, text="Přidat učebnici", command=self.pridat_ucebnici, font="Arial 8", width=20)
        self.button_pridat_ucebnici.grid(row=8, column=2, sticky=W)

        self.button_export_ucebnici = tk.Button(self.ucebnice, text="Export učebnice", command=self.export_ucebnice, font="Arial 8", width=20)
        self.button_export_ucebnici.grid(row=9, column=2, sticky=W)



    """____________________vytvoří pole se seznamem lekcí podle zvoleného studenta/jazyka/učebnice ____________________"""
    def create_widgets_Lekce(self):
        try:
            self.Lekce.destroy()
        except AttributeError:
            pass
        self.Lekce = tk.LabelFrame(root, text="Lekce", font="Arial 8")
        self.Lekce.grid(row=1, column=3, rowspan=11, sticky=N)

        self.tree_Lekce = ttk.Treeview(self.Lekce, column=("c_lekce", "nazev"), height=10, selectmode='browse')
        self.tree_Lekce['show'] = 'headings' # schová první sloupec s identifikátorem
        self.tree_Lekce.grid(row=2, column=0,  columnspan=2)
        
        self.tree_Lekce.heading("#0", text="#\n ")
        self.tree_Lekce.column("#0", width=0, stretch=NO, anchor='center')

        self.tree_Lekce.heading("c_lekce", text="lekce\n ")
        self.tree_Lekce.column("c_lekce", minwidth=0, width=50, stretch=NO, anchor='center')

        self.tree_Lekce.heading("nazev", text="Název lekce\n ")
        self.tree_Lekce.column("nazev", minwidth=0, width=200, stretch=NO, anchor='center')

        self.button_pridat_lekci = tk.Button(self.Lekce, text="Přidat lekci", command=self.pridat_lekci, font="Arial 8", width=20)
        self.button_pridat_lekci.grid(row=4, column=0, sticky=W)

        self.button_pridat_slovicka = tk.Button(self.Lekce, text="Přidat slovíčka", command=self.pridat_slovicka, font="Arial 8", width=20)
        self.button_pridat_slovicka.grid(row=4, column=1, sticky=W)

        self.button_pridat_slovicka = tk.Button(self.Lekce, text="Vypsat slovíčka", command=self.vypsat_slovicka, font="Arial 8", width=20)
        self.button_pridat_slovicka.grid(row=5, column=0, sticky=W)

        self.button_export_lekce = tk.Button(self.Lekce, text="Export lekce", command=self.export_lekce, font="Arial 8", width=20)
        self.button_export_lekce.grid(row=5, column=1, sticky=W)

        self.button_Test = tk.Button(self.Lekce, text="Testovat", command=self.Test, font="Arial 8", width=20, bg="lightgreen")
        self.button_Test.grid(row=6, column=0, columnspan=2, sticky=W+E)


              
    """_________________ vytvoří pravé pole pro další volby - nastavení/testování/historie ____________________________"""
    def create_ovl_sekce(self):
        self.pole_nastaveni = tk.LabelFrame(root, text="Nastavení", font="Arial 8")
        self.pole_nastaveni.grid(row=1, column=4, sticky=N)
        self.nastav = tk.Label(self.pole_nastaveni, text="", font="Arial 8")

        self.button_Nastaveni = tk.Button(self.pole_nastaveni, text="Nastavení studenta", command=self.nastaveni_stud, font="Arial 8", width=20)
        self.button_Nastaveni.grid(row=2, column=2, sticky=W)

        self.mezera1 = tk.Label(self.pole_nastaveni, text="")
        self.mezera1.grid(row=3, column=2, sticky=W)

        self.button_Nastaveni = tk.Button(self.pole_nastaveni, text="Výsledky studenta", command=self.vysledky_stud, font="Arial 8", width=20)
        self.button_Nastaveni.grid(row=4, column=2, sticky=W)

        self.mezera1 = tk.Label(self.pole_nastaveni, text="")
        self.mezera1.grid(row=5, column=2, sticky=W)

        self.email = tk.Button(self.pole_nastaveni, text="Poslat email vývojářům?", command=self.email_vyvojarum, font="Arial 8", width=20)
        self.email.grid(row=6, column=2, sticky=W)

        self.mezera2 = tk.Label(self.pole_nastaveni, text="")
        self.mezera2.grid(row=7, column=2, sticky=W)

        self.web = tk.Button(self.pole_nastaveni, text="Navštívit web", command=self.web, font="Arial 8", width=20)
        self.web.grid(row=8, column=2, sticky=W)

        self.mezera3 = tk.Label(self.pole_nastaveni, text="")
        self.mezera3.grid(row=9, column=2, sticky=W)


        self.aktualizuj = tk.Button(self.pole_nastaveni, text="Aktualizovat", command=self.aktualizuj, font="Arial 8", width=20)
        self.aktualizuj.grid(row=10, column=2, sticky=W)

        self.mezera3 = tk.Label(self.pole_nastaveni, text="")
        self.mezera3.grid(row=11, column=2, sticky=W)

        self.button_tov_nastaveni = tk.Button(self.pole_nastaveni, text="Obnovit\ntovární nastavení", command=self.tovarni_nastaveni, fg="red", font="Arial 8", width=20)
        self.button_tov_nastaveni.grid(row=12, column=2, sticky=W)




    """__________________WEB_______________________"""
    def web(self):
        web = ini_nastaveni.WEB()
        if web == "":
            pass
        else:
            webbrowser.open(web, new=2)



    """_______________Aktualizuj___________________"""
    def aktualizuj(self):
        self.slovnik.upgrade()
        time.sleep(1)
        os.startfile("update_ini.exe")
        time.sleep(1)
        os._exit(0)



    """__________________________email vývojářům________________"""
    def email_vyvojarum(self):
        try:
            outlook = win32.Dispatch("outlook.application")
            mail = outlook.CreateItem(0)
            mail.subject = "Slovník - nahlásit problém/požadavek" # předmět
            mail.To = "petr.f@pyladiesplzen.wz.cz"
            mail.Display(False)
            return
        except:
            tk.messagebox.showwarning("Error_P0001", """Je nutné mít nainstalovanou aplikaci MS Outlook\npokud aplikaci nechcete instalovat, 
                                        kontaktujte nás na adrese\nhttps://pyladiesplzen.wz.cz/Kontakt/""")



    """_______________________ Tovární nastavení______________________________"""
    def tovarni_nastaveni(self):
        if messagebox.askyesno("POZOR", "Program se uvede do prvotního spuštění\nVšechny učebnice budou exportovány do adresáře 'Export'") == True:
            prace_s_db.export_vseho()
            os.remove("db_slovnik.sqlite")
            tk.messagebox.showwarning("???", "Nastaveno prvotní zobrazení\nSPUSŤE PROGRAM ZNOVU")
            self.parent.destroy()

        else:
            pass



    """_______________________ nastaveni.py ___________________________________________________________________"""
    # vše k pravému nastavení + testování
    def nastaveni_stud(self):
        nastaveni.nastaveni_studenta(self)
        return

    def uloz_nastaveni_stud(self):
        nastaveni.uloz_nastaveni_studenta(self)
        return

    def pridej_jazyk(self, student, jazyk):
        nastaveni.pridat_jazyk(self, student, jazyk)
        return
    
    """_______________________ vysledky.py ___________________________________________________________________"""
    def vysledky_stud(self):
        # vypíše výsledky studenta v rámci jedné učebnice
        
        try:
            # self.akt_ucebnice = self.seznam_ucebnic[self.ucebnice_ListBox.curselection()[0]]
            data = prace_s_db.nacti_vysledky(self.akt_student, self.akt_ucebnice)
            vys.vypis_vysledky(self, data)
        except AttributeError:
            tk.messagebox.showwarning("Error_P0002", "Vyber jazyk, učebnici.")
        except IndexError:
            tk.messagebox.showwarning("Error_P0002", "Vyber jazyk, učebnici.")
        except TypeError:
            tk.messagebox.showwarning("Error_P0002", "Vyber jazyk, učebnici.")
        return
    

    """_______________________Testování______________________________________"""
    # vše k oknu testování
    
    def Test(self): # otevře okno pro testování
        try:
            ts.tes(self)
        except IndexError:
            tk.messagebox.showwarning("Error_P003", "Nejdříve vyber lekci.")
            return

   
    def Testuj(self): # spustí se po kliknutí na tlačítko Testuj
        if len(self.slovnik.testuj) > 0:
            pass
        else:
            self.nacti_nastaveni_studenta()
            if self.slovnik.aktualni_slovo == 0:
                self.slovnik.vysledky = []
                self.slovnik.aktualni_slovo = 0
                ts.nacti(self)
                ts.spust_test(self)
            elif self.slovnik.aktualni_slovo == len(self.slovnik.testuj):
                if tk.messagebox.askyesno("Nová volba", "Testovat znovu?") == True:
                    self.slovnik.k_testovani = []
                    self.slovnik.testuj = []
                    self.slovnik.netestuj = []
                    self.slovnik.aktualni_slovo = 0
                    self.slovnik.vysledky_pro_ulozeni_do_db = []
                    self.slovnik.vysledky_db = []
                    self.slovnik.vysledky = []
                    self.slovnik.pocet_sl_pro_procenta = 0
                    self.slovnik.pocet_spravnych_pro_procenta = 0
                    ts.nacti(self)
                    ts.spust_test(self)
                else:
                    self.slovnik.k_testovani = []
                    self.slovnik.testuj = []
                    self.slovnik.netestuj = []
                    self.slovnik.aktualni_slovo = 0
                    self.slovnik.vysledky_pro_ulozeni_do_db = []
                    self.slovnik.vysledky_db = []
                    self.slovnik.vysledky = []
                    self.slovnik.pocet_sl_pro_procenta = 0
                    self.slovnik.pocet_spravnych_pro_procenta = 0
                    self.top_test.destroy()
            else:
                pass
            


    def vyhodnot(self, event):    
        if self.slovnik.aktualni_slovo == len(self.slovnik.testuj):
            return
        else:
            ts.vyhodnoceni(self)


    def ukonci_top_test(self):
        self.slovnik.k_testovani = []
        self.slovnik.testuj = []
        self.slovnik.netestuj = []
        self.slovnik.aktualni_slovo = 0
        self.slovnik.vysledky_pro_ulozeni_do_db = []
        self.slovnik.vysledky_db = []
        self.slovnik.vysledky = []
        self.slovnik.pocet_sl_pro_procenta = 0
        self.slovnik.pocet_spravnych_pro_procenta = 0
        self.top_test.destroy()

    """_______________________ pridat_uc.py _________________________________________________________________________"""
    # vše k učebnici
    def pridat_ucebnici(self):
        uc.nova_ucebnice(self) # otevře nové okno
         
    def ulozit_ucebnice(self):
        uc.ulozit_novou_ucebnici(self) # uloží novou učebnici
        self.Lekce.destroy()


    """_______________________Export učebnice_________________________"""

    def export_ucebnice(self):
        try:
            prace_s_db.export_ucebnice(self.slovnik.akt_U, self.slovnik.akt_jazyk)
        except AttributeError:
            tk.messagebox.showwarning("Error_P0004", "Vyber učebnici k exportu.")
            return

            
    """____________________________ pridat_lek.py ___________________________________________________________________"""

    # vše k lekci
    def pridat_lekci(self): 
        lek.nova_lekce(self) # otevře nové okno

    
    def ulozit_lekci(self): # uloží novou lekci
        lek.ulozit_Lek(self)

    def smazat_lekci(self):
        lek.smazat_Lek(self) # smaže lekci

    """____________________________ pridat_sl.py _______________________________________________________________"""

    # vše k novému oknu přidat slovíčka(otevření, zavření, ukládání)
    def pridat_slovicka(self):
        """
        Otevře okno pro přidání učebnice, lekce, slovíček
        """
        sl.nacti_lekci(self)

    def dalsi_slovo(self, event):
        """
        Postupné ukládání slovíček
        """
        sl.dalsi(self)
        sl.vypsat_manualni_slovicka(self)


    def ulozit(self):
        """
        Uložení nových slovíček
        """
        sl.ulozit(self)

    def nacist(self):
        im.import_sl(self)

    def edit(self):
        sl.opravit(self)

    """____________________________ vypsat_sl.py _______________________________________________________________"""

    # vše k novému oknu vypsat slovíčka(otevření, zavření, ukládání)
    def vypsat_slovicka(self):
        """
        Vypíše seznam slovíček vybrané lekce
        """
        
        try:
            self.akt_Lekce = str(self.tree_Lekce.item(self.tree_Lekce.focus())["values"][1])
            v_sl.vypis_slovicka(self,prace_s_db.slovicka_lekce(self.akt_Lekce, self.akt_student))
            #print(prace_s_db.nastaveni_studenta(self.akt_student))
        except IndexError:
            tk.messagebox.showwarning("Error_P0005", "Vyber lekci.")


    """_________________________Export lekce__________________________________"""

    def export_lekce(self):
        try:
            self.akt_Lekce = str(self.tree_Lekce.item(self.tree_Lekce.focus())["values"][1])
            prace_s_db.export_lekce(self.akt_Lekce, self.akt_jazyk, "Export_Lekce")
        except IndexError:
            tk.messagebox.showwarning("Error_P0006", "Vyber lekci.")


    """_____________________________ new_student.py ______________________________________________________________"""

    # vše k oknu nový student

    def vytvor_top_okno_novy_student(self):
        """
        Otevře okno pro registraci studenta
        """
        ns.vytvor_top_okno_novy_student(self)


    def novy(self):
        ns.ulozit_noveho_studenta(self)
        self.slovnik.seznam_studentu = []
        self.slovnik.nacti_studenty()
        self.studenti.destroy()
        self.create_widgets_uzivatele()
        self.zobraz()
        return



    """___________________________ načtení studenta ____________________________________________________________"""
    # načtení studenta
    def nacti_studenta(self, event=""):
        """
        Nacte jazyky studenta
        """
        try:
            if event !="":  # funkci spouštím z akce ListBoxu - <on click>     
                self.akt_student = self.slovnik.seznam_studentu[self.studenti_ListBox.curselection()[0]]
            self.words.destroy()
            self.ucebnice.destroy()
            # self.Lekce.destroy()
        except IndexError:
            tk.messagebox.showwarning("Error_P0007", "Vyber studenta.")
            return
        except AttributeError:
            pass

        try:
            _ftp.prog(self.akt_student)
        except:
            pass

            
        self.jazyky_studenta = prace_s_db.jazyky_studenta(self.akt_student)
        self.create_widgets_jazyk()
        self.create_ovl_sekce()
        self.uzivatel["text"] = "Aktuální uživatel je "+ str(self.akt_student)
        self.nacti_nastaveni_studenta()
        return
    
    def nacti_nastaveni_studenta(self):
        
        """
        nastavi aktuální hodnoty do promennych:
        self.pocet_k_testu 
        self.pocet_spravnych
        self.pocet_kol_testu
        self.typ_prekladu
        self.testovat_jen_spatne
        self.rychlost_cteni
        """
        
        nastav_studenta = prace_s_db.nastaveni_studenta(self.akt_student)
        self.slovnik.pocet_k_testu = nastav_studenta[0]
        self.slovnik.pocet_spravnych = nastav_studenta[1]
        self.slovnik.pocet_kol_testu = nastav_studenta[2]
        self.slovnik.typ_prekladu = nastav_studenta[3]
        self.slovnik.testovat_jen_spatne = nastav_studenta[4]
        self.slovnik.rychlost_cteni = nastav_studenta[5]
        return
    

    """____________________ načtení učebnice _________________________________________________________"""
    # načte učebnice podle zvoleného jazyka
    def nacti_ucebnice(self):
        # print(self.akt_jazyk.get(), end=": ")
        self.akt_j = self.akt_jazyk.get()
        self.seznam_ucebnic = prace_s_db.seznam_ucebnic(self.akt_jazyk.get())
        #print(self.seznam_ucebnic)
        self.create_widgets_ucebnice()
        for ucebnice in self.seznam_ucebnic:
            #print(ucebnice)
            self.ucebnice_ListBox.insert(tkinter.END, ucebnice)
        return
       
    """___________________________ načtení lekce ______________________________________"""
    # načte lekce podle vybrané učebnice
    def nacti_lekce(self, event=""):
        try:
            if event !="":  # funkci spouštím z akce ListBoxu - <on click>     
                self.akt_ucebnice = self.seznam_ucebnic[self.ucebnice_ListBox.curselection()[0]]
                self.slovnik.akt_U = self.akt_ucebnice
        except IndexError:
            tk.messagebox.showwarning("Error_P0008", "Založ novou učebnici.")
            self.akt_ucebnice = ""
            return
        self.create_widgets_Lekce()
        # print("Učebnice: ", self.akt_ucebnice, end=": ")
        self.seznam_lekci = prace_s_db.seznam_lekci(self.akt_ucebnice)
        for ii in self.tree_Lekce.get_children():
            self.tree_Lekce.delete(ii)

        pozice = 0
        for cislo in self.seznam_lekci:
            self.tree_Lekce.insert("", "end", text=pozice, values=cislo)
            pozice += 1

    """_______________________ zobrazí registrované studenty __________________________"""
    # zobrazí registrované studenty
    def zobraz(self):
        for student in self.slovnik.seznam_studentu:
            self.studenti_ListBox.insert(tkinter.END, student)
        return


    """_______________________ ukončení celé aplikace _____________________________"""
    # zavře celou aplikaci včetně všech oken
    def on_close(self):
       self.parent.destroy()


    
if __name__ == '__main__':
    root = tk.Tk()
    my_menu = tk.Menu(root)
    slovnik = slovnik()
    app = slovnikGUI(root, slovnik)
    app.mainloop()
