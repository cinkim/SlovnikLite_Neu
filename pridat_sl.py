import tkinter as tk
from tkinter import ttk, StringVar, NORMAL, E, W, NO
import tkinter.messagebox
from tkinter import messagebox
import prace_s_db

def new_words(self):
        self.words = tk.Toplevel()
        self.words.attributes('-topmost', 'true')
        self.words.title("Nová slovíčka")
        try:
                pozor = "POZOR: Ukládáš data do"
                jaz = self.akt_j + ":  " + self.akt_ucebnice
                lek = "Lekce: " + self.akt_Lekce
        except AttributeError:
                tk.messagebox.showwarning("ERROR", "Nejsou vybrané všechny parametry.")
                return
        self.nadpis = tk.Label(self.words, text=pozor, font="Ariel 14", bg="grey")
        self.nadpis.grid(row=1, columnspan=3, sticky=W+E)

        self.struktura = tk.Label(self.words, text=jaz, font="Ariel 14", bg="grey")
        self.struktura.grid(row=2, columnspan=3, sticky=W+E)

        self.struktura = tk.Label(self.words, text=lek, font="Ariel 14", bg="grey")
        self.struktura.grid(row=3, columnspan=3, sticky=W+E)

        self.mez1 = tk.Label(self.words, text="")
        self.mez1.grid(row=4, column=0)

        self.mez = tk.Label(self.words, text="X", width=5)
        self.mez.grid(row=12, column=1)
        """
        self.jinak = tk.Label(self.words, text="", font="Ariel 10")
        self.jinak.grid(row=11, column=2)
        """
        self.w1 = StringVar()
        self.wc = tk.Entry(self.words, width=40, justify="center", textvariable=self.w1)
        self.wc.grid(row=12, column=0, sticky=W)
        self.wc.focus_set()
        self.wc.config(state=NORMAL)

        self.w2 = StringVar()
        self.wnc = tk.Entry(self.words, width=40, justify="center", textvariable=self.w2)
        self.wnc.bind("<Return>", self.dalsi_slovo)
        self.wnc.grid(row=12, column=2, sticky=W)
        self.wnc.config(state=NORMAL)

        self.tree_slovicka_new = ttk.Treeview(self.words, column=("česky", "překlad"), height=20, selectmode='browse')
        self.tree_slovicka_new['show'] = 'headings' # schová první sloupec s identifikátorem
        self.tree_slovicka_new.grid(row=13, columnspan=3)
        
        self.tree_slovicka_new.heading("#0", text="#\n ")
        self.tree_slovicka_new.column("#0", width=0, stretch=NO, anchor='center')

        self.tree_slovicka_new.heading("česky", text="Česky\n ")
        self.tree_slovicka_new.column("česky", minwidth=0, width=320, stretch=NO, anchor='center')

        self.tree_slovicka_new.heading("překlad", text="Překlad\n ")
        self.tree_slovicka_new.column("překlad", minwidth=0, width=320, stretch=NO, anchor='center')

        self.mez = tk.Label(self.words, text="", height=1)
        self.mez.grid(row=17, column=0)

        self.Ulozit = tk.Button(self.words, width=20, text="Uložit", command=self.ulozit)
        self.Ulozit.grid(row=17, column=0, sticky=W)

        self.zmena = tk.Button(self.words, width=20, text="Editovat", command=self.edit)
        self.zmena.grid(row=17, column=1, sticky=W)

        self.nacist_ze_souboru = tk.Button(self.words, width=20, text="Načíst ze souboru", command=self.nacist)
        self.nacist_ze_souboru.grid(row=17, column=2, sticky=E)

        self.mez = tk.Label(self.words, text="", height=1)
        self.mez.grid(row=18, column=0)

        self.Konec = tk.Button(self.words, width=20, text="Konec", fg="red", command=self.words.destroy)
        self.Konec.grid(row=19, column=0, sticky=W)


def nacti_lekci(self):
        try:
                self.akt_Lekce = str(self.tree_Lekce.item(self.tree_Lekce.focus())["values"][1])
                new_words(self)
        except IndexError:
                tk.messagebox.showwarning("ERROR", "Nejdříve vyber jazyk/učebnici/lekci.")
                return
        except tkinter.TclError:
                tk.messagebox.showwarning("ERROR", "Nejdříve vyber jazyk/učebnici/lekci.")
                return
        except AttributeError:
                tk.messagebox.showwarning("ERROR", "Nejdříve vyber jazyk/učebnici/lekci.")
                return


def dalsi(self):
        self.slovnik.nova_sl.reverse()
        self.s = []
        if self.w2.get() == "":
            tk.messagebox.showwarning("ERROR", "Vyplň slovíčka pro uložení.")
            return
        elif self.w1.get() == "":
            tk.messagebox.showwarning("ERROR", "Vyplň slovíčka pro uložení.")
            return
        else:
            self.s.append(self.w1.get())
            self.s.append(self.w2.get())
            self.slovnik.nova_sl.append(self.s)
            self.s = []
            self.w1.set("")
            self.w2.set("") 
            self.wc.focus_set()
            self.slovnik.nova_sl.reverse()


def vypsat_manualni_slovicka(self):
        for ii in self.tree_slovicka_new.get_children():
            self.tree_slovicka_new.delete(ii)

        pozice = 0
        for zaznam in self.slovnik.nova_sl:
            self.tree_slovicka_new.insert("", "end", text=pozice, values=(zaznam[0], zaznam[1]))
            pozice += 1


def ulozit(self):
        if messagebox.askyesno("???", "Uložit slovíčka?") == True:
                self.pro_ulozeni = []
                self.pro_ulozeni.append(self.akt_Lekce)
                for qq in self.slovnik.nova_sl:
                        self.pro_ulozeni.append(qq)
                pocet = prace_s_db.pridej_slovicka(self.pro_ulozeni)
                self.slovnik.nova_sl = []
                tk.messagebox.showwarning("ULOŽENO", "V databázi je uloženo " + str(pocet) + "\nslovíček pro tuto lekci.")
                for ii in self.tree_slovicka_new.get_children():
                        self.tree_slovicka_new.delete(ii)
        else:
                pass
                return

def opravit(self):
        try:
                self.oprav_sl = self.tree_slovicka_new.item(self.tree_slovicka_new.focus())["values"]
                self.w1.set(self.oprav_sl[0])
                self.w2.set(self.oprav_sl[1])
                self.slovnik.nova_sl.remove(self.oprav_sl)
        except IndexError:
                tk.messagebox.showwarning("ERROR", "Vyber slovíčko pro editaci.")
                return

        vypsat_manualni_slovicka(self)

