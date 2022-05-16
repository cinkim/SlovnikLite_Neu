import tkinter as tk
from tkinter import StringVar, E, W, NORMAL
from tkinter import messagebox
import prace_s_db as db

def nova_lekce(self):
        
    self.lekce_nova = tk.Toplevel()
    self.lekce_nova.attributes('-topmost', 'true')
    self.lekce_nova.title("Nová lekce")

    self.nadpis = tk.Label(self.lekce_nova, text="Jazyk: " + self.akt_j + "\nUčebnice:" + self.akt_ucebnice, font="Ariel 14", bg="red")
    self.nadpis.grid(row=0, columnspan=6, sticky=W+E)

    self.mezera = tk.Label(self.lekce_nova, text="", font="Ariel 10")
    self.mezera.grid(row=1, column=0)

    self.popisek = tk.Label(self.lekce_nova, text="Číslo lekce:", font="Ariel 10")
    self.popisek.grid(row=2, column=0)

    self.cl = StringVar()
    self.nova_lek_cislo = tk.Entry(self.lekce_nova, width=10, textvariable=self.cl)
    self.nova_lek_cislo.grid(row=2, column=1 )
    self.nova_lek_cislo.config(state=NORMAL)
    self.nova_lek_cislo.focus_set()

    self.popisek = tk.Label(self.lekce_nova, text="Název lekce:", font="Ariel 10")
    self.popisek.grid(row=2, column=2)

    self.nl = StringVar()
    self.nova_lek = tk.Entry(self.lekce_nova, width=25, textvariable=self.nl)
    self.nova_lek.grid(row=2, column=3, columnspan=2 )

    self.Ulozit = tk.Button(self.lekce_nova, width=20, text="Uložit", fg="green", command=self.ulozit_lekci)
    self.Ulozit.grid(row=2, column=5, sticky=W)
    
    self.mezera = tk.Label(self.lekce_nova, text="", font="Ariel 10")
    self.mezera.grid(row=3, column=0)

    self.Konec = tk.Button(self.lekce_nova, width=20, text="Konec", fg="green", command=self.lekce_nova.destroy)
    self.Konec.grid(row=4, column=0,  sticky=W)



def ulozit_Lek(self):
    id_l = self.nova_lek_cislo.get()
    nazev = self.nova_lek.get()
    seznam_l = db.seznam_lekci(self.akt_ucebnice)
    for qq in seznam_l:
        if (id_l in str(qq[0])) or (nazev == qq[1]):
            tk.messagebox.showwarning("ERROR", "Číslo lekce, nebo název již existuje.")
            return
    if messagebox.askyesno("Uložit???", "Přidat lekci?") == True:
        while True:
            if (self.nova_lek.get() or self.nova_lek_cislo.get()) == "":
                tk.messagebox.showwarning("ERROR", "Vyplňte číslo a název lekce")
                return
            try:
                # print(self.akt_j, self.akt_ucebnice, self.nova_lek.get(), int(self.nova_lek_cislo.get()))
                nova = nazev + " - " + self.akt_ucebnice
                db.uloz_lekci(self.akt_j, self.akt_ucebnice, nova, int(self.nova_lek_cislo.get()))
                self.nacti_lekce()
                self.cl.set("")
                self.nl.set("") 
                return       
            except ValueError:
                tk.messagebox.showwarning("ERROR", "Zadej správně číslo lekce.")
                return

            except TypeError:
                tk.messagebox.showwarning("ERROR", "Klikni na učebnici, kam se budou ukládat lekce.")
                return
    else:
        pass
    

    # nastavení vybraného řádku právě vložené lekce child_id ... ITEM ID vložené lekce
    # child_id = self.tree_Lekce.get_children()[-1] # poslední řádek
    # child_id = self.tree_Lekce.get_children()[self.seznam_lekci.index((int(cislo),nazev))] # máme řazené tak hledá ID pro danou hodnotu
    # self.tree_Lekce.selection_set(child_id)
