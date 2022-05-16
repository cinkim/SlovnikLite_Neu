import tkinter as tk
from tkinter import ttk, E, W, NO


def vypis_vysledky(self,seznam_vysledku):
        self.vysledky = tk.Toplevel()
        self.vysledky.attributes('-topmost', 'true')
        self.vysledky.title("Výsledky studenta: " + self.akt_student)

        self.nadpis = tk.Label(self.vysledky, text="Jazyk: " + self.akt_j + "\nUčebnice:" + self.akt_ucebnice, font="Ariel 14", bg="red")
        self.nadpis.grid(row=0, columnspan=3, sticky=W+E)
        
        self.tree_vysledky = ttk.Treeview(self.vysledky, column=("datum", "lekce", "hodnoceni", "testovano"), height=20, selectmode='browse')
        self.tree_vysledky['show'] = 'headings' # schová první sloupec s identifikátorem
        self.tree_vysledky.grid(row=13, columnspan=3)
        
        self.tree_vysledky.heading("#0", text="#\n ")
        self.tree_vysledky.column("#0", width=0, stretch=NO, anchor='center')

        self.tree_vysledky.heading("datum", text="Datum\n ")
        self.tree_vysledky.column("datum", minwidth=0, width=150, stretch=NO, anchor='center')

        self.tree_vysledky.heading("lekce", text="Lekce\n")
        self.tree_vysledky.column("lekce", minwidth=0, width=270, stretch=NO, anchor=W)

        self.tree_vysledky.heading("hodnoceni", text="Hodnocení %\n ")
        self.tree_vysledky.column("hodnoceni", minwidth=0, width=100, stretch=NO, anchor='center')

        self.tree_vysledky.heading("testovano", text="Počet slov ")
        self.tree_vysledky.column("testovano", minwidth=0, width=120, stretch=NO, anchor='center')

        self.mez = tk.Label(self.vysledky, text="", height=1)
        self.mez.grid(row=17, column=0)

        self.Konec = tk.Button(self.vysledky, width=20, text="Konec", fg="red", command=self.vysledky.destroy)
        self.Konec.grid(row=19, column=0, sticky=W)

        pozice = 0
        
        for zaznam in seznam_vysledku:
            

            self.tree_vysledky.insert("", "end",  text=pozice, values=(zaznam[0], zaznam[1], zaznam[2], zaznam[3]))
            pozice += 1
        
        """
        print(ttk.Style().theme_names())
        ttk.Style().theme_use('clam')
        ttk.Style().configure("Treeview", background="red",foreground="white")
        self.tree_vysledky.insert('', 'end', text=pozice, values=(1,2,3), tags=('r',))
        self.tree_vysledky.tag_configure('sp', background='red')
        self.tree_vysledky.tag_configure('r',background='yellow')
        """


