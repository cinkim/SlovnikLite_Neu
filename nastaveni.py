import tkinter as tk
from tkinter import ttk, StringVar, N,E, W
from tkinter import messagebox
import prace_s_db

def nastaveni_studenta(self):
    # načte z db nastavení daného studenta
    self.nacti_nastaveni_studenta()
    try:
        self.top_student.destroy()
    except AttributeError:
        pass
    self.top_student = tk.Toplevel()
    self.top_student.attributes('-topmost', 'true')
    self.top_student.title("Nastavení studenta")  
    
    self.nastaveni = tk.LabelFrame(self.top_student, text="Nastavení studenta: "  + self.akt_student, font="Arial 14")
    self.nastaveni.grid(row=0, column=0, rowspan=5, sticky=N)
    
    self.mezera0 = tk.Label(self.nastaveni, text="")
    self.mezera0.grid(row=1, column=0, columnspan=3, sticky=W)
   
    self.pocet_slovicek_popis = tk.Label(self.nastaveni, text="Počet slovíček v jednom testu     (10-50):")
    self.pocet_slovicek_popis.grid(row=2, column=0, columnspan=2,sticky=W)
    self.pocet_slovicek_Entry = tk.Entry(self.nastaveni, width=10, justify="center")
    self.pocet_slovicek_Entry.grid(row=2, column=2, sticky=W)
    self.pocet_slovicek_Entry.insert(0,self.slovnik.pocet_k_testu)

    self.pocet_opakovani_popis = tk.Label(self.nastaveni, text="Počet opakování v rámci testu     (1-5): ")
    self.pocet_opakovani_popis.grid(row=3, column=0, columnspan=2,sticky=W)
    self.pocet_opakovani_Entry = tk.Entry(self.nastaveni, width=10, justify="center")
    self.pocet_opakovani_Entry.grid(row=3, column=2, sticky=W)
    self.pocet_opakovani_Entry.insert(0,self.slovnik.pocet_kol_testu)

    self.pocet_spravne_popis = tk.Label(self.nastaveni, text="Počet správných odpovědí pro vyřazení slovíčka z testu     (1-10): ")
    self.pocet_spravne_popis.grid(row=4, column=0, columnspan=3, sticky=W)
    self.pocet_spravne_Entry = tk.Entry(self.nastaveni, width=10, justify="center")
    self.pocet_spravne_Entry.grid(row=4, column=3, sticky=W)
    self.pocet_spravne_Entry.insert(0,self.slovnik.pocet_spravnych)

    self.mezera = tk.Label(self.nastaveni, text="")
    self.mezera.grid(row=5, column=0, columnspan=3, sticky=W)


    """________________________ výběr typu překladu ___________________"""
    
    self.nastaveni_preklad = tk.LabelFrame(self.nastaveni, text="Typ překladu: ", font="Arial 8")
    self.nastaveni_preklad.grid(row=6, column=0, rowspan=5, sticky=N)
    
    pozice = 1 # pozice řádky v rámci skupiny RadioButtonu
    typy = [("cz -> cizí jazyk","1"),
            ("cizí jazyk -> cz","2"),
            ("míchat: cz <-> cizí jazyk","3")
            ]
    
    self.var_preklad = StringVar()   
    for text, hodnota in typy:      # indicatoron=0, 
        preklad_Radio = tk.Radiobutton(self.nastaveni_preklad, text=text, variable=self.var_preklad, value=hodnota)            
        if hodnota == str(self.slovnik.typ_prekladu):
            preklad_Radio.select()        
        preklad_Radio.grid(row=pozice, sticky=W) 
        pozice = pozice + 1
      
    """________________________ výběr testu se slovíčky s více špatnými odpověďmi___________________"""
    
    self.nastaveni_test_spatna = tk.LabelFrame(self.nastaveni, text="Test pouze ze slovíček\n s více jak 3 špatnými odpověďmi: ", font="Arial 8")
    self.nastaveni_test_spatna.grid(row=6, column=2, columnspan=2,rowspan=5, sticky=W)
    
    pozice = 1 # pozice řádky v rámci skupiny RadioButtonu
    a_n = [("Ano","1"),
            ("Ne","2"),
            ]
    self.var_spatne = StringVar()
    for text, hodnota in a_n:      # indicatoron=0, 
        self.test_spatna_Radio = tk.Radiobutton(self.nastaveni_test_spatna, text=text, variable=self.var_spatne, value=hodnota)      
        if hodnota == str(self.slovnik.testovat_jen_spatne): # označí jako nastavenou hodnotu z db
            self.test_spatna_Radio.select()       
        self.test_spatna_Radio.grid(row=pozice, sticky=W) 
        pozice = pozice + 1
    

    """________________________ nastavení jazyků ___________________"""
    
    self.mezera2 = tk.Label(self.nastaveni, text="")
    self.mezera2.grid(row=15, column=0, columnspan=3, sticky=W)

    self.nastaveni_jazyky = tk.LabelFrame(self.nastaveni, text="Jazyky: ", font="Arial 8", width=600)
    self.nastaveni_jazyky.grid(row=16, column=0, columnspan=5,rowspan=5, sticky=W)

    
    self.studovane_jazyky  = "Aktuálně studované:   "
    for jazyk in self.jazyky_studenta:
        self.studovane_jazyky = self.studovane_jazyky + jazyk + "    " 
    
    self.stud_jazyky_label = tk.Label(self.nastaveni_jazyky, text=self.studovane_jazyky)
    self.stud_jazyky_label.grid(row=0, column=0, columnspan=3,sticky=W)

    if len(nestudovane(self.akt_student))>0: #pokud nemá všechny jazyky už vybrané --> možnost přidat další jazyk
        self.nove_jazyky_label = tk.Label(self.nastaveni_jazyky, text="Přidat další jazyk:")
        self.nove_jazyky_label.grid(row=1, column=0, sticky=W)
        dalsi_jazyk = StringVar()
        self.dalsi_jazyk_Combo=ttk.Combobox(self.nastaveni_jazyky, textvariable=dalsi_jazyk,  width=10)
        self.dalsi_jazyk_Combo['values'] = nestudovane(self.akt_student)
        self.dalsi_jazyk_Combo.grid(row=1, column=1)
        self.pridat_jazyk_Button = tk.Button(self.nastaveni_jazyky, text="Přidat jazyk", 
        command=lambda: self.pridej_jazyk(self.akt_student,nestudovane(self.akt_student)[self.dalsi_jazyk_Combo.current()]), font="Arial 8", width=20)
        self.pridat_jazyk_Button.grid(row=1, column=2, sticky=W)

    """________________________ resetování slovíček - počtů odpovědí ___________________"""
    
    self.mezera3 = tk.Label(self.nastaveni, text="")
    self.mezera3.grid(row=1 , column=0, columnspan=3, sticky=W)
    
    global reset_nastaveni
    reset_nastaveni = tk.LabelFrame(self.nastaveni, text="Vynulovat odpovědi u slovíček\nSmazat slovíčka lekce:            ", font="Arial 8", width=600)
    self.t1 = tk.Label(reset_nastaveni, text="Jazyk:", width=10)
    self.t1.grid(row=0 , column=1, sticky=W)
    self.t2 = tk.Label(reset_nastaveni, text="Učebnice:", width=20)
    self.t2.grid(row=0 , column=2,sticky=W)
    self.t3 = tk.Label(reset_nastaveni, text="Lekce:", width=25)
    self.t3.grid(row=0 , column=3, sticky=W)

    reset_nastaveni.grid(row=23, column=0, columnspan=5,rowspan=5, sticky=W)
    reset_jazyk = StringVar()
    reset_jazyk_Combo=ttk.Combobox(reset_nastaveni, textvariable=reset_jazyk,  width=10)
    reset_jazyk_Combo['values'] = self.jazyky_studenta
    reset_jazyk_Combo.grid(row=1, column=1)
    reset_jazyk_Combo.bind("<<ComboboxSelected>>",lambda x:reset_nacti_ucebnice(reset_jazyk.get(),self.akt_student))
    
    """________________________ nastavení rychlosti čtení___________________"""
   
    self.nastaveni_cteni = tk.LabelFrame(self.nastaveni, text="Rychlost čtení: ", font="Arial 8")
    self.nastaveni_cteni.grid(row=17, column=3, columnspan=2,rowspan=5, sticky=W)
    
    pozice = 1 # pozice řádky v rámci skupiny RadioButtonu
    rychlost = [("Pomalu","0"),
            ("Rychle","1")]
    self.var_rychlost = tk.IntVar()
    for text, hodnota in rychlost:      # indicatoron=0, 
        self.rychlost_Radio = tk.Radiobutton(self.nastaveni_cteni, text=text, variable=self.var_rychlost, value=hodnota)      
        if hodnota == str(self.slovnik.rychlost_cteni): # označí jako nastavenou hodnotu z db
            self.rychlost_Radio.select()       
        self.rychlost_Radio.grid(row=pozice, sticky=W) 
        pozice = pozice + 1
    
    """______________________________________________________ tlačítka _________________________________________________________"""

    self.ulozit_nastaveni = tk.Button(self.top_student, text="Uložit nastavení", command=self.uloz_nastaveni_stud, fg="blue", font="Arial 8", width=20)
    self.ulozit_nastaveni.grid(row=0, column=5, sticky=W)

    self.ulozit_Konec = tk.Button(self.top_student, text="Konec", command=self.top_student.destroy, fg="red", font="Arial 8", width=20)
    self.ulozit_Konec.grid(row=1, column=5, sticky=W+E)
    """_________________________________________________________________________________________________________________________"""

def reset_nacti_ucebnice(jazyk, student):
    try:
            reset_lekce_Combo.destroy()
    except NameError:
        pass
    reset_ucebnice = StringVar()
    reset_ucebnice_Combo=ttk.Combobox(reset_nastaveni, textvariable=reset_ucebnice,  width=20)
    reset_ucebnice_Combo['values'] = prace_s_db.seznam_ucebnic(jazyk)
    reset_ucebnice_Combo.grid(row=1, column=2)
    reset_ucebnice_Combo.bind("<<ComboboxSelected>>",lambda x:reset_nacti_lekce(reset_ucebnice.get(),student))

def reset_nacti_lekce(ucebnice,student):
    reset_lekce = StringVar()
    global reset_lekce_Combo
    reset_lekce_Combo=ttk.Combobox(reset_nastaveni, textvariable=reset_lekce,  width=30)
    nazvy_lekci=[]
    for lekce in prace_s_db.seznam_lekci(ucebnice):
        nazvy_lekci.append(lekce[1])
    reset_lekce_Combo['values'] = nazvy_lekci
    reset_lekce_Combo.grid(row=1, column=3)
    reset_lekce_Combo.bind("<<ComboboxSelected>>",lambda x:reset_poctu_odpovedi(reset_lekce.get(),student))

def reset_poctu_odpovedi(lekce,student):
    resetovat_Button = tk.Button(reset_nastaveni, text="Vynuluj počty odpovědí", 
        command=lambda: resetovat(lekce, student), fg="blue", font="Arial 8", width=70)
    resetovat_Button.grid(row=2, column=0, columnspan=4, sticky=W)

    smaz_slovicka = tk.Button(reset_nastaveni, text="Smaž slovíčka!", 
        command=lambda: smaz_slovicka_lek(lekce), fg="red", font="Arial 8", width=70)
    smaz_slovicka.grid(row=3, column=0, columnspan=4, sticky=W)


def resetovat(lekce, student):
    if messagebox.askyesno("Reset???", "Opravdu vynulovat počty u lekce - " + lekce+"?") == True:
        prace_s_db.reset_slovicek(student,lekce)
    else:
        pass

def smaz_slovicka_lek(lekce):
    if messagebox.askyesno("Smazat???", "Opravdu smazat slovíčka " + lekce+"?") == True:
        prace_s_db.smaz_slovicka_lekce(lekce)
    else:
        pass

def studovane(student):
    return prace_s_db.jazyky_studenta(student)

def nestudovane(student):
    nestudovane_jazyky = []
    for jazyk in prace_s_db.seznam_jazyku():
        if jazyk not in studovane(student):
            nestudovane_jazyky.append(jazyk)
    return nestudovane_jazyky


def pridat_jazyk(self,student, jazyk):      
    prace_s_db.uloz_dalsi_jazyk_studentovi(student, jazyk)
    self.dalsi_jazyk_Combo.set('')
    self.studovane_jazyky  = "Aktuálně studované: "
    for jazyk in prace_s_db.jazyky_studenta(self.akt_student):
        self.studovane_jazyky = self.studovane_jazyky + jazyk + "    " 

    self.stud_jazyky_label['text'] = self.studovane_jazyky
    if len(nestudovane(student)) > 0:
        self.dalsi_jazyk_Combo['values'] = nestudovane(student)
    else:
        self.dalsi_jazyk_Combo.destroy()
        self.pridat_jazyk_Button.destroy()
        self.nove_jazyky_label.destroy()
    self.nacti_studenta()
    self.jazyky_studenta=prace_s_db.jazyky_studenta(self.akt_student)
    
def uloz_nastaveni_studenta(self):
    # kontrola zadaných hodnot
    chyba = False
    text_chyby = "CHYBNĚ ZADÁNO:"
    if self.pocet_slovicek_Entry.get().isdigit() and int(self.pocet_slovicek_Entry.get()) <= 50 and int(self.pocet_slovicek_Entry.get()) >= 10 :
        pass
    else:
        chyba = True
        text_chyby = text_chyby + "\n" + "Počet slovíček v jednom testu"

    if self.pocet_spravne_Entry.get().isdigit() and int(self.pocet_spravne_Entry.get()) <= 10 and int(self.pocet_spravne_Entry.get()) > 0 :
        pass
    else:
        chyba = True
        text_chyby = text_chyby + "\n" + "Hodnota musí být v uvedeném rozsahu."
    
    if self.pocet_opakovani_Entry.get().isdigit() and int(self.pocet_opakovani_Entry.get()) <= 5 and int(self.pocet_opakovani_Entry.get()) >= 1 :
        pass
    else:
        chyba = True
        text_chyby = text_chyby + "\n" + "Počet opakování v rámci jednoho testu"


    if chyba:
        tk.messagebox.showwarning("Špatné nastavení:", text_chyby )
    else: #nastavení se uloží do db
        prace_s_db.uloz_nastaveni_studenta([
        self.akt_student, 
        self.pocet_slovicek_Entry.get(),
        self.pocet_spravne_Entry.get(),
        self.pocet_opakovani_Entry.get(),
        self.var_preklad.get(),  
        self.var_spatne.get(),
        self.var_rychlost.get() 
        ])
    self.nacti_nastaveni_studenta()
    