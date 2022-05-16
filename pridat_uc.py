import tkinter as tk
from tkinter import StringVar, E, W, NORMAL
from tkinter import messagebox
import prace_s_db as db

def nova_ucebnice(self): 
    self.ucebnice_nova = tk.Toplevel()
    self.ucebnice_nova.attributes('-topmost', 'true')
    self.ucebnice_nova.title("Nová učebnice")

    self.nadpis = tk.Label(self.ucebnice_nova, text="Jazyk: " + self.akt_jazyk.get(), font="Ariel 14", bg="red")
    self.nadpis.grid(row=0, columnspan=4, sticky=W+E)

    self.mezera = tk.Label(self.ucebnice_nova, text="", font="Ariel 10")
    self.mezera.grid(row=1, column=0)

    self.popisek = tk.Label(self.ucebnice_nova, text="Název učebnice:", font="Ariel 10")
    self.popisek.grid(row=2, column=0)

    self.uc = StringVar()
    self.nova_uc = tk.Entry(self.ucebnice_nova, width=25, textvariable=self.uc)
    self.nova_uc.grid(row=2, column=1, columnspan=2 )
    self.nova_uc.config(state=NORMAL)
    self.nova_uc.focus_set()

    self.Ulozit = tk.Button(self.ucebnice_nova, width=20, text="OK", fg="green", command=self.ulozit_ucebnice)
    self.Ulozit.grid(row=2, column=3, sticky=W)

    
    self.mezera = tk.Label(self.ucebnice_nova, text="", font="Ariel 10")
    self.mezera.grid(row=3, column=0)

    self.Konec_prid_uc = tk.Button(self.ucebnice_nova, width=20, text="Konec", fg="red", command=self.ucebnice_nova.destroy)
    self.Konec_prid_uc.grid(row=4, column=0, sticky=W)


def ulozit_novou_ucebnici(self):
    seznam = db.seznam_vsech_ucebnic()
    if self.nova_uc.get() in seznam:
        tk.messagebox.showwarning("???", "Učebnice již existuje\npoužijte jiné pojmenování, postačí přidat za název jakýkoliv znak\nnapř: číslovku, přezdívku....")
        return
    if messagebox.askyesno("Uložit???", "Uložit učebnici?") == True:
        while True:
            if self.nova_uc.get() == "":
                tk.messagebox.showwarning("ERROR", "Zadej název učebnice.")
                return
            else:
                db.uloz_ucebnici(self.akt_j,self.nova_uc.get())
                # self.nova_uc.insert(0,"")
                # self.akt_ucebnice = self.nova_uc # nová učebnice se stává aktuální učebnicí  
                self.nacti_ucebnice()
                # self.ucebnice_ListBox.select_set(self.seznam_ucebnic.index(self.akt_ucebnice)) # označení řádku aktuální učebnice
                self.nacti_lekce()
                self.uc.set("")
                return
    else:
        pass
















