import tkinter as tk
from tkinter import StringVar, NORMAL, CENTER, E, W
from tkinter import DISABLED, NORMAL
import random
import prace_s_db
import prace_s_db as db
from random import randrange
import vysledky_testu as vt

import datetime

import os


def tes(self):
    self.akt_Lekce = str(self.tree_Lekce.item(self.tree_Lekce.focus())["values"][1])
    self.top_test = tk.Toplevel()
    self.top_test.attributes('-topmost', 'true')
    self.top_test.title("Testování lekce: "+ self.akt_Lekce)
    self.top_test.grid_columnconfigure(0, weight=4)
    self.top_test.grid_columnconfigure(1, weight=4)
    self.top_test.grid_columnconfigure(2, weight=4)
    self.top_test.grid_columnconfigure(3, weight=4)

    self.top_test.grid_rowconfigure(1, weight=0)
    self.top_test.grid_rowconfigure(2, weight=1)
    self.top_test.grid_rowconfigure(3, weight=0)
    self.top_test.grid_rowconfigure(4, weight=1)
    self.top_test.grid_rowconfigure(5, weight=0)
    self.top_test.grid_rowconfigure(6, weight=1)
    self.top_test.grid_rowconfigure(7, weight=1)
    self.top_test.grid_rowconfigure(8, weight=0)
    self.top_test.grid_rowconfigure(9, weight=0)

    self.testovani = tk.Label(self.top_test, text="Student: " + self.akt_student + "\nJazyk : " + self.akt_j + "\nUčebnice :" + self.akt_ucebnice + "\nLekce:" + self.akt_Lekce, font="Ariel 14", bg="grey")
    self.testovani.grid(row=1, columnspan=4, sticky=W+E)

    self.M_tes = tk.Label(self.top_test, text="")
    self.M_tes.grid(row=2, column=0)

    self.ceskytext = StringVar()
    self.cesky = tk.Label(self.top_test, textvariable=self.ceskytext, width=25, font="Arial 12")
    self.cesky.grid(row=3, column=0)

    self.pr = StringVar()
    self.preklad = tk.Entry(self.top_test, width=25, font="Arial 12", textvariable=self.pr)
    self.archiv = self.preklad.get()
    self.preklad.bind("<Return>", self.vyhodnot)
    self.preklad.grid(row=3, column=1)
    self.preklad.config(state=NORMAL)

    self.uspech = StringVar()
    self.akt_uspech = tk.Label(self.top_test, textvariable=self.uspech, width=25, font="Arial 12")
    self.akt_uspech.grid(row=3, column=2)

    self.zbyva = StringVar()
    self.zbyva_slovicek = tk.Label(self.top_test, textvariable=self.zbyva, width=25, font="Arial 12")
    self.zbyva_slovicek.grid(row=3, column=3)

    self.M_tes = tk.Label(self.top_test, text="")
    self.M_tes.grid(row=4, column=0)

    self.M_tes = tk.Label(self.top_test, text="Otázka")
    self.M_tes.grid(row=5, column=0)

    self.M_tes = tk.Label(self.top_test, text="Tvoje odpověď")
    self.M_tes.grid(row=5, column=1, )

    self.M_tes = tk.Label(self.top_test, text="Správná odpověď")
    self.M_tes.grid(row=5, column=2)

    self.M_tes = tk.Label(self.top_test, text="Hodnocení")
    self.M_tes.grid(row=5, column=3)

    self.text1 = tk.Text(self.top_test, font="Arial 10", width=33, height=2)
    self.text1.grid(row=6, column=0)

    self.text2 = tk.Text(self.top_test, font="Arial 10", width=33, height=2)
    self.text2.grid(row=6, column=1)

    self.text3 = tk.Text(self.top_test, font="Arial 10", width=33, height=2)
    self.text3.grid(row=6, column=2)

    self.text4 = tk.Text(self.top_test, font="Arial 10", width=33, height=2)
    self.text4.grid(row=6, column=3)

    self.mez = tk.Label(self.top_test, text="")
    self.mez.grid(row=7, column=0)

    self.spustit = tk.Button(self.top_test, text="Spustit Test", command=self.Testuj, font="Ariel 8", width=20)
    self.spustit.grid(row=8, column=0, sticky=W)

    self.Konec = tk.Button(self.top_test, text="Konec", command=self.ukonci_top_test, fg="red", font="Arial 8", width=20)
    self.Konec.grid(row=9, column=0, sticky=W)

def nacti(self):
    try:
        self.akt_Lekce = str(self.tree_Lekce.item(self.tree_Lekce.focus())["values"][1])
        
    except IndexError:
        tk.messagebox.showwarning("ERROR", "Nejdříve vyber lekci.")
        return

    if self.slovnik.typ_prekladu == 1:
        v1(self)
    elif self.slovnik.typ_prekladu == 2:
        v2(self)
    elif self.slovnik.typ_prekladu == 3:
        v3(self)
    else:
        tk.messagebox.showwarning("ERROR", "Chyba v nastavení.")
        return

    
def v1(self): # cz/cizí
    self.slovnik.k_testovani = prace_s_db.slovicka_lekce(self.akt_Lekce, self.akt_student) # načte všechny slovíčka lekce
    random.shuffle(self.slovnik.k_testovani)
    random.shuffle(self.slovnik.k_testovani) # 2x zamíchá seznam
    prvek = 0
    for poradi in self.slovnik.k_testovani: # projíždí seznam slovíček
        if self.slovnik.testovat_jen_spatne == 1 and poradi[4] > 3 and prvek < self.slovnik.pocet_k_testu:
            self.slovnik.testuj.append(poradi)
            prvek +=1
        elif (prvek < self.slovnik.pocet_k_testu) and (poradi[3] < self.slovnik.pocet_spravnych) and self.slovnik.testovat_jen_spatne == 2: 
            self.slovnik.testuj.append(poradi)
            prvek +=1
        else:
            pass
    self.slovnik.k_testovani = self.slovnik.netestuj
    self.slovnik.netestuj = []
    self.slovnik.testuj = self.slovnik.testuj
    if self.slovnik.testuj == []:
        tk.messagebox.showwarning("ERROR", "S tímto nastavením již není co testovat\nzměňte nastavení studenta, nebo zvolte jinou lekci.")
        return
    else:
        self.slovnik.testuj = self.slovnik.testuj * self.slovnik.pocet_kol_testu
        random.shuffle(self.slovnik.testuj)
        self.slovnik.zbyva_k_testovani = len(self.slovnik.testuj)


def v2(self): # cizí/cz
    self.slovnik.k_testovani = prace_s_db.slovicka_lekce(self.akt_Lekce, self.akt_student)
    random.shuffle(self.slovnik.k_testovani)
    random.shuffle(self.slovnik.k_testovani)

    prvek = 0
    poradi1 = ""
    poradi2 = ""
    for poradi in self.slovnik.k_testovani: # projíždí seznam slovíček
        if self.slovnik.testovat_jen_spatne == 1 and poradi[4] > 3 and prvek < self.slovnik.pocet_k_testu:
            poradi1 = poradi[1]
            poradi2 = poradi[2]
            poradi[1] = poradi2
            poradi[2] = poradi1
            poradi1 = ""
            poradi2 = ""
            self.slovnik.testuj.append(poradi)
            prvek +=1
        elif (prvek < self.slovnik.pocet_k_testu) and (poradi[3] < self.slovnik.pocet_spravnych) and self.slovnik.testovat_jen_spatne == 2:
            poradi1 = poradi[1]
            poradi2 = poradi[2]
            poradi[1] = poradi2
            poradi[2] = poradi1
            poradi1 = ""
            poradi2 = ""
            self.slovnik.testuj.append(poradi)
            prvek +=1
        else:
            pass
    self.slovnik.k_testovani = self.slovnik.netestuj
    self.slovnik.netestuj = []
    self.slovnik.testuj = self.slovnik.testuj
    if self.slovnik.testuj == []:
        tk.messagebox.showwarning("ERROR", "S tímto nastavením již není co testovat\nzměňte nastavení studenta, nebo zvolte jinou lekci.")
        return
    else:
        self.slovnik.testuj = self.slovnik.testuj * self.slovnik.pocet_kol_testu
        random.shuffle(self.slovnik.testuj)
        self.slovnik.zbyva_k_testovani = len(self.slovnik.testuj)



def nahoda(self):
    cislo = randrange(2)
    return cislo

def v3(self): # mix
    self.slovnik.k_testovani = prace_s_db.slovicka_lekce(self.akt_Lekce, self.akt_student)
    random.shuffle(self.slovnik.k_testovani)
    random.shuffle(self.slovnik.k_testovani)
    
    prvek = 0
    poradi1 = ""
    poradi2 = ""
    for poradi in self.slovnik.k_testovani: # projíždí seznam slovíček
        typ = nahoda(self)
        if typ == 0:
            if self.slovnik.testovat_jen_spatne == 1 and poradi[4] > 3 and prvek < self.slovnik.pocet_k_testu:
                poradi1 = poradi[1]
                poradi2 = poradi[2]
                poradi[1] = poradi2
                poradi[2] = poradi1
                poradi1 = ""
                poradi2 = ""
                self.slovnik.testuj.append(poradi)
                prvek +=1
            elif (prvek < self.slovnik.pocet_k_testu) and (poradi[3] < self.slovnik.pocet_spravnych) and self.slovnik.testovat_jen_spatne == 2:
                poradi1 = poradi[1]
                poradi2 = poradi[2]
                poradi[1] = poradi2
                poradi[2] = poradi1
                poradi1 = ""
                poradi2 = ""
                self.slovnik.testuj.append(poradi)
                prvek +=1
            else:
                pass
        else:
            if self.slovnik.testovat_jen_spatne == 1 and poradi[4] > 3 and prvek < self.slovnik.pocet_k_testu:
                self.slovnik.testuj.append(poradi)
                prvek +=1
            elif (prvek < self.slovnik.pocet_k_testu) and (poradi[3] < self.slovnik.pocet_spravnych) and self.slovnik.testovat_jen_spatne == 2: 
                self.slovnik.testuj.append(poradi)
                prvek +=1
            else:
                pass
    self.slovnik.k_testovani = self.slovnik.netestuj
    self.slovnik.netestuj = []
    self.slovnik.testuj = self.slovnik.testuj
    if self.slovnik.testuj == []:
        tk.messagebox.showwarning("ERROR", "S tímto nastavením již není co testovat\nzměňte nastavení studenta, nebo zvolte jinou lekci.")
        return
    else:
        self.slovnik.testuj = self.slovnik.testuj * self.slovnik.pocet_kol_testu
        random.shuffle(self.slovnik.testuj)
        self.slovnik.zbyva_k_testovani = len(self.slovnik.testuj)


    


def spust_test(self): 
    try:     
        self.slovicko = self.slovnik.testuj[self.slovnik.aktualni_slovo]
        self.cz = self.slovicko[1]
        self.ceskytext.set(self.cz)
        
        self.preklad.focus_set()
        self.preklad.config(state=NORMAL)
    except IndexError:
        return



def ukaz(self):
    smaz(self)

    mezivypocet = self.slovnik.pocet_sl_pro_procenta/100
    proc = self.slovnik.pocet_spravnych_pro_procenta/mezivypocet
    self.proc = str(round(proc, 2))

    self.text1.config(state=NORMAL)
    self.text2.config(state=NORMAL)
    self.text3.config(state=NORMAL)
    self.text4.config(state=NORMAL)
    mezi = self.slovnik.vysledky.reverse()
    if mezi == None:
        mezi = self.slovnik.vysledky

    for vysledek in mezi:
        if vysledek[3] == "Dobře":
            self.uspech.set("Aktuální úspěšnost: " + self.proc + " %")
            self.zbyva.set("Do konce testu zbývá: " + str(self.slovnik.zbyva_k_testovani) + " slovíček.")

            self.text1.tag_config("cerna", foreground="black", justify=CENTER)
            self.text1.insert(tk.END,vysledek[0], "cerna")
            self.text1.insert(tk.END, "\n")

            self.text2.tag_config("cerna", foreground="black", justify=CENTER)
            self.text2.insert(tk.END,vysledek[1], "cerna")
            self.text2.insert(tk.END, "\n")

            self.text3.tag_config("cerna", foreground="black", justify=CENTER)
            self.text3.insert(tk.END,vysledek[2], "cerna")
            self.text3.insert(tk.END, "\n")

            self.text4.tag_config("modre", foreground="blue", justify=CENTER)
            self.text4.insert(tk.END,vysledek[3], "modre")
            self.text4.insert(tk.END, "\n")
            mezi = []


        else:
            self.uspech.set("Aktuální úspěšnost: " + self.proc + " %")
            self.zbyva.set("Do konce testu zbývá: " + str(self.slovnik.zbyva_k_testovani) + " slovíček.")

            self.text1.tag_config("cerna", foreground="black",justify=CENTER)
            self.text1.insert(tk.END,vysledek[0], "cerna")
            self.text1.insert(tk.END, "\n")

            self.text2.tag_config("cerna", foreground="black",justify=CENTER)
            self.text2.insert(tk.END,vysledek[1], "cerna")
            self.text2.insert(tk.END, "\n")

            self.text3.tag_config("cerna", foreground="black",justify=CENTER)
            self.text3.insert(tk.END,vysledek[2], "cerna")
            self.text3.insert(tk.END, "\n")

            self.text4.tag_config("cervena", foreground="red", justify=CENTER)
            self.text4.insert(tk.END,vysledek[3], "cervena")
            self.text4.insert(tk.END, "\n")
            mezi = []
    self.slovnik.vysledky.reverse()
    self.text1.config(state=DISABLED)
    self.text2.config(state=DISABLED)
    self.text3.config(state=DISABLED)
    self.text4.config(state=DISABLED)


def smaz(self):
    self.text1.config(state=NORMAL)
    self.text2.config(state=NORMAL)
    self.text3.config(state=NORMAL)
    self.text4.config(state=NORMAL)

    self.text1.delete(1.0, tk.END)
    self.text2.delete(1.0, tk.END)
    self.text3.delete(1.0, tk.END)
    self.text4.delete(1.0, tk.END)

    self.text1.config(state=DISABLED)
    self.text2.config(state=DISABLED)
    self.text3.config(state=DISABLED)
    self.text4.config(state=DISABLED)
    return


def uloz_do_db(self):
    self.slovnik.vysledky_pro_ulozeni_do_db.append(self.akt_student)
    self.slovnik.vysledky_pro_ulozeni_do_db.append(self.akt_Lekce)
    self.slovnik.vysledky_pro_ulozeni_do_db.append(self.proc)
    sl = []
    for qq in self.slovnik.vysledky_db:
        sl.append(qq[0])
        sl.append(qq[3])
        sl.append(qq[4])
        self.slovnik.vysledky_pro_ulozeni_do_db.append(sl)
        sl = []
    db.uloz_test_studenta(self.slovnik.vysledky_pro_ulozeni_do_db)
    self.slovnik.vysledky_pro_ulozeni_do_db = []

def vyhodnoceni(self):
    self.slovnik.zbyva_k_testovani -=1
    otazka = self.slovicko[2].lower()
    odpoved = self.preklad.get().lower()
    otazka_bez_mezer = otazka.replace(" ", "")
    odpoved_bez_mezer = odpoved.replace(" ", "")

    rozsekana_otazka = otazka.split(";")
    
    orezana_otazka = []
    for slovo in rozsekana_otazka:
        slovo = slovo.strip()
        orezana_otazka.append(slovo)
    
    try:
        self.slovnik.pocet_sl_pro_procenta +=1
        spravne = self.slovicko[3]
        spatne = self.slovicko[4]
        vys = []
        vys_do_vypisu = []
        if (odpoved in orezana_otazka) or (otazka == odpoved) or (otazka_bez_mezer == odpoved_bez_mezer):
            self.ok = True       
            spravne = 1
            spatne = 0
            self.slovnik.pocet_spravnych_pro_procenta+=1
            vys.append(self.slovicko[0])
            vys.append(self.slovicko[1])
            vys.append(self.slovicko[2])
            vys.append(spravne)
            vys.append(spatne)

            vys_do_vypisu.append(self.slovicko[1])
            vys_do_vypisu.append(self.preklad.get())
            vys_do_vypisu.append(self.slovicko[2])
            vys_do_vypisu.append("Dobře")

            self.slovnik.vysledky_db.append(vys)
            self.slovnik.vysledky.append(vys_do_vypisu)
            self.pr.set("")
            ukaz(self)
            self.slovnik.aktualni_slovo+=1
            if self.slovnik.aktualni_slovo == len(self.slovnik.testuj):
                self.ceskytext.set("")
                uloz_do_db(self)
                ulozit_test(self, self.slovnik.vysledky)
                tk.messagebox.showwarning("HOTOVO", "Právě si došel na konec testu.")
                vt.zobraz_vysledky_testu(self)
                vt.nacti_vysledky(self, self.slovnik.vysledky)
                return
            spust_test(self)
        else:
            self.ok = False
            spatne = 1
            spravne = 0
            vys.append(self.slovicko[0])
            vys.append(self.slovicko[1])
            vys.append(self.slovicko[2])
            vys.append(spravne)
            vys.append(spatne)

            vys_do_vypisu.append(self.slovicko[1])
            vys_do_vypisu.append(self.preklad.get())
            vys_do_vypisu.append(self.slovicko[2])
            vys_do_vypisu.append("Špatně")

            self.slovnik.vysledky_db.append(vys)
  
            self.slovnik.vysledky.append(vys_do_vypisu)

            self.pr.set("")
            ukaz(self)
            self.slovnik.aktualni_slovo+=1
            if self.slovnik.aktualni_slovo == len(self.slovnik.testuj):
                self.ceskytext.set("")
                uloz_do_db(self)
                ulozit_test(self, self.slovnik.vysledky)
                tk.messagebox.showwarning("HOTOVO", "Právě si došel na konec testu.")
                vt.zobraz_vysledky_testu(self)
                vt.nacti_vysledky(self, self.slovnik.vysledky)
                return
            spust_test(self)
    except TypeError:
        self.slovnik.pocet_sl_pro_procenta +=1
        spravne = self.slovicko[3]
        spatne = self.slovicko[4]
        vys = []
        vys_do_vypisu = []
        if (odpoved in orezana_otazka) or (otazka == odpoved) or (otazka_bez_mezer == odpoved_bez_mezer):
            self.ok = True       
            spravne = 1
            spatne = 0
            self.slovnik.pocet_spravnych_pro_procenta+=1
            vys.append(self.slovicko[0])
            vys.append(self.slovicko[1])
            vys.append(self.slovicko[2])
            vys.append(spravne)
            vys.append(spatne)

            vys_do_vypisu.append(self.slovicko[1])
            vys_do_vypisu.append(self.preklad.get())
            vys_do_vypisu.append(self.slovicko[2])
            vys_do_vypisu.append("Dobře")

            self.slovnik.vysledky_db.append(vys)
            self.slovnik.vysledky.append(vys_do_vypisu)
            self.pr.set("")
            ukaz(self)
            self.slovnik.aktualni_slovo+=1
            if self.slovnik.aktualni_slovo == len(self.slovnik.testuj):
                self.ceskytext.set("")
                uloz_do_db(self)
                ulozit_test(self, self.slovnik.vysledky)
                tk.messagebox.showwarning("HOTOVO", "Právě si došel na konec testu.")
                vt.zobraz_vysledky_testu(self)
                vt.nacti_vysledky(self, self.slovnik.vysledky)
                return
            spust_test(self)
        else:
            self.ok = False
            spatne = 1
            spravne = 0
            vys.append(self.slovicko[0])
            vys.append(self.slovicko[1])
            vys.append(self.slovicko[2])
            vys.append(spravne)
            vys.append(spatne)

            vys_do_vypisu.append(self.slovicko[1])
            vys_do_vypisu.append(self.preklad.get())
            vys_do_vypisu.append(self.slovicko[2])
            vys_do_vypisu.append("Špatně")

            self.slovnik.vysledky_db.append(vys)
            self.slovnik.vysledky.append(vys_do_vypisu)
            self.pr.set("")
            ukaz(self)
            self.slovnik.aktualni_slovo+=1
            if self.slovnik.aktualni_slovo == len(self.slovnik.testuj):
                self.ceskytext.set("")
                uloz_do_db(self)
                ulozit_test(self, self.slovnik.vysledky)
                tk.messagebox.showwarning("HOTOVO", "Právě si došel na konec testu.")
                vt.zobraz_vysledky_testu(self)
                vt.nacti_vysledky(self, self.slovnik.vysledky)
                return
            
            spust_test(self)

def ulozit_test(self, vysledky):
    while True:
        now = datetime.datetime.now()
        akt_datum = str(now.year)+ "_" + str(now.month) + "_" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute)
        cesta = "Vysledky/" + akt_datum + "_" + self.akt_student + "_" + self.akt_Lekce + ".txt"
        cesta = cesta.replace(":", "_")
        try:
            with open(cesta, mode="w", encoding="utf-8") as soubor:
                for ii in self.slovnik.vysledky:
                    ii = str(ii)
                    ii = ii.replace("[", "")
                    ii = ii.replace("]", "")
                    print(ii, file=soubor)
                return
        except FileNotFoundError:
            os.mkdir("Vysledky")
