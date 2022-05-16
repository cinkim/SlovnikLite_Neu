import tkinter as tk
from tkinter import ttk, StringVar, NORMAL, CENTER, E, W
from tkinter import DISABLED, NORMAL

def zobraz_vysledky_testu(self):
    self.vypis_odpovedi = tk.Toplevel()
    self.vypis_odpovedi.attributes('-topmost', 'true')
    self.vypis_odpovedi.title("Odpovědi testu: " + self.akt_Lekce)


    self.tree_vypis_testu = ttk.Treeview(self.vypis_odpovedi, column=("otazka", "odpoved", "spravna_odpoved", "hodnoceni"), height=20)
    self.tree_vypis_testu['show'] = 'headings' # schová první sloupec s identifikátorem
    self.tree_vypis_testu.grid(row=2, column=0,  columnspan=2)
    
    self.tree_vypis_testu.heading("#0", text="#\n ")
    self.tree_vypis_testu.column("#0", width=0, anchor='center')

    self.tree_vypis_testu.heading("otazka", text="otázka\n ")
    self.tree_vypis_testu.column("otazka", minwidth=0, width=200, anchor='center')

    self.tree_vypis_testu.heading("odpoved", text="odpověď\n ")
    self.tree_vypis_testu.column("odpoved", minwidth=0, width=200, anchor='center')

    self.tree_vypis_testu.heading("spravna_odpoved", text="správná odpověď\n ")
    self.tree_vypis_testu.column("spravna_odpoved", minwidth=0, width=200, anchor='center')

    self.tree_vypis_testu.heading("hodnoceni", text="hodnocení\n ")
    self.tree_vypis_testu.column("hodnoceni", minwidth=0, width=200, anchor='center')


def nacti_vysledky(self, vysledky):
    for ii in self.tree_vypis_testu.get_children():
        self.tree_vypis_testu.delete(ii)

    pozice = 0
    for cislo in vysledky:
        self.tree_vypis_testu.insert("", "end", text=pozice, values=(cislo[0],cislo[1],cislo[2],cislo[3]))
        pozice += 1