
import tkinter as tk
from tkinter import StringVar, NORMAL, W, E
from tkinter import NORMAL


import prace_s_db

def vytvor_top_okno_novy_student(self):
        self.st = tk.Toplevel()
        self.st.attributes('-topmost', 'true')
        self.st.title("Nový student")

        self.newst = StringVar()
        self.new_st = tk.Entry(self.st, width=30, justify="center", textvariable=self.newst)
        self.new_st.grid(row=3, column=0, sticky=W)
        self.new_st.config(state=NORMAL)
        self.new_st.focus_set()

        self.new_popis = tk.Label(self.st, text="Jméno studenta", width=20, font="Arial 8")
        self.new_popis.grid(row=3, column=1, sticky=W)

        self.jz = tk.Label(self.st, text="Označ studijní jazyky.", font="Arial 11")
        self.jz.grid(row=4, columnspan=2, sticky=W)

        self.var_Aj = tk.IntVar()
        self.radio_Aj = tk.Checkbutton(self.st, text="Aj", variable=self.var_Aj)
        self.radio_Aj.config(state=NORMAL)
        self.radio_Aj.grid(row=5, column=0, sticky=W)

        self.var_Nj = tk.IntVar()
        self.radio_Nj = tk.Checkbutton(self.st, text="Nj", variable=self.var_Nj)
        self.radio_Nj.config(state=NORMAL)
        self.radio_Nj.grid(row=6, column=0, sticky=W)

        self.var_Fr = tk.IntVar()
        self.radio_Fr = tk.Checkbutton(self.st, text="Fr", variable=self.var_Fr)
        self.radio_Fr.config(state=NORMAL)
        self.radio_Fr.grid(row=7, column=0, sticky=W)

        self.var_Es = tk.IntVar()
        self.radio_Es = tk.Checkbutton(self.st, text="Es", variable=self.var_Es)
        self.radio_Es.config(state=NORMAL)
        self.radio_Es.grid(row=8, column=0, sticky=W)

        self.var_It = tk.IntVar()
        self.radio_It = tk.Checkbutton(self.st, text="It", variable=self.var_It)
        self.radio_It.config(state=NORMAL)
        self.radio_It.grid(row=9, column=0, sticky=W)

        self.var_Ru = tk.IntVar()
        self.radio_Ru = tk.Checkbutton(self.st, text="Ru", variable=self.var_Ru)
        self.radio_Ru.config(state=NORMAL)
        self.radio_Ru.grid(row=10, column=0, sticky=W)

        self.button_uloz = tk.Button(self.st, text="Uložit", command=self.novy, fg="blue", font="Arial 8", width=20)
        self.button_uloz.grid(row=11, column=0, sticky=W)

        self.button_Konec = tk.Button(self.st, text="Konec", command=self.st.destroy, fg="red", font="Arial 8", width=20)
        self.button_Konec.grid(row=12, column=0, sticky=W)



def ulozit_noveho_studenta(self):
    if len(self.slovnik.seznam_studentu) == 3:
        tk.messagebox.showwarning("ERROR", "V této verzi již další student nejde uložit\nnutno zakoupit verzi SlovnikPRO")
        return
    else:
        vystup = []
        new = self.new_st.get()
        if new == "":
            tk.messagebox.showwarning("ERROR", "Zadej jméno studenta.")
            return
        if new in self.slovnik.seznam_studentu:
            tk.messagebox.showwarning("ERROR", "Uživatel již existuje\nzvolte jiné jméno.")
            return
        Aj = self.var_Aj.get()
        Nj = self.var_Nj.get()
        Fr = self.var_Fr.get()
        Es = self.var_Es.get()
        It = self.var_It.get()
        Ru = self.var_Ru.get()
        if Aj+Nj+Fr+Es+It+Ru == 0:
            tk.messagebox.showwarning("ERROR", "Zvolte alespoň jeden studijní jazyk.")
            return
        vystup.append(new)
        if Aj == 1:
            vystup.append("Aj")
        if Nj == 1:
            vystup.append("Nj")
        if Fr == 1:
            vystup.append("Fr")
        if Es == 1:
            vystup.append("Es")
        if It == 1:
            vystup.append("It")
        if Ru == 1:
            vystup.append("Ru")

        prace_s_db.pridat_studenta(vystup)

        self.newst.set("")
        self.var_Aj.set(0)
        self.var_Nj.set(0)
        self.var_Fr.set(0)
        self.var_Es.set(0)
        self.var_It.set(0)
        self.var_Ru.set(0)
    

