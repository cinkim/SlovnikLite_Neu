import sqlite3
from os import path
import os

import datetime


def overeni_sl():
    if path.exists("db_slovnik.sqlite") == False:
        create_sql_db()

    conn, cursor = pripojeni_db()
    conn.close()

def pripojeni_db():
    """
     - vytvori pripojeni a kruzor do databaze sqlite
    VSTUP: db - nepovinny udaj - cesta k db-souboru; kdyz se nezada, tak db = "db_slovnik.sqlite"
    VYSTUP: connection, cursor
    """
    db="db_slovnik.sqlite"
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    return connection, cursor

def create_sql_db():
    """
    - vytvori strukturu databaze, naplni nektere tabulky    
    VSTUP: bez parametru, natvrdo bere z SQL skritpu v akt.adr. - db_schema.sql, db_data.sql
    VYSTUP: pripravena db ve formatu sqlite
    """
    conn, cursor = pripojeni_db()
    # print('Vytvařím databázi..')
    sql_file = open("db_schema.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    # print('Plním databázi...')
    sql_file = open("db_data.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    
def pridat_studenta(novy):
    overeni_sl()
    """
    - vlozi noveho studenta a jeho jazyky
    VSTUP: jmeno_studenta - retezec
           jazyky_ucebnice - ["jazyk1", "jazyk2", ...]
    VYSTUP: odpovidajici zaznamy v db
    """ 
    jmeno_studenta = novy[0]
    conn, cursor = pripojeni_db()
    # vloží nový záznam do tabulky osoby
    cursor.execute(f'''INSERT INTO OSOBY (jmeno) values ('{jmeno_studenta}') ''')
    # zjišťuje ID nově vložené osoby
    cursor.execute(f'''SELECT ID FROM OSOBY WHERE JMENO = '{jmeno_studenta}' ''')
    nova_osoba_id = cursor.fetchone()[0] 
    novy.pop(0)      
    for jazyk in novy:
        # print(jazyk)
        # zjišťuje ID jazyků, které má daný student
        # (jazyk v db musí existovat, uživatel vybírá z nabídky jazyků)
        cursor.execute(f'''SELECT ID FROM JAZYKY WHERE NAZEV = '{jazyk}'  ''')
        jazyk_id = cursor.fetchone()[0]
        cursor.execute(f'''INSERT INTO OSOBY_JAZYKY values ({nova_osoba_id},{jazyk_id}, null) ''')

    conn.commit()


def uloz_ucebnici(jazyk, ucebnice):
    # conn, cursor = pripojeni_db()
    # zjišťuje ID jazyka
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT ID FROM JAZYKY WHERE NAZEV = '{jazyk}' ''')
    jazyk_id = cursor.fetchone()[0] 

    cursor.execute(f'''INSERT INTO UCEBNICE values (null,'{ucebnice}', {jazyk_id}) ''')
    # return cursor.execute(f'''SELECT ID FROM UCEBNICE WHERE NAZEV = '{ucebnice}' ''').fetchone()[0]        
    conn.commit()

def uloz_lekci(jazyk, ucebnice, lekce, cislo):
    # conn, cursor = pripojeni_db()
    # zjišťuje ID jazyka
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT ID FROM JAZYKY WHERE NAZEV = '{jazyk}' ''')
    jazyk_id = cursor.fetchone()[0] 

    cursor.execute(f'''SELECT ID FROM UCEBNICE WHERE NAZEV = '{ucebnice}' AND JAZYK_ID = {jazyk_id} ''')
    #print(cursor.fetchall())
    ucebnice_id = cursor.fetchone()[0] 

    cursor.execute(f'''INSERT INTO LEKCE values (null,{ucebnice_id}, {cislo}, '{lekce}') ''')
    
    conn.commit()
    

# ********************************************************************************
#  pomocné funkce na převod
# ********************************************************************************
def select_to_seznam(data):
    """
    pomocna funkce na prevod select s 1 sloupcem --> seznam
    """
    # [(jmeno1,), (jmeno2,), (jmeno3,)] --> [jmeno1, jemno2, jmeno3]
    seznam = []   
    for polozka in data:
        seznam.append(polozka[0])
    return seznam

def seznam_tuple2senam_seznamu(seznam, hodnota_none):
    """
    pomocna funkce na prevod seznamu s tuplemi --> seznam seznamů
    hodnota_none  ... to, čím nahradím honodtu NONE(NULL) co vrátila db
    """
    seznam_novy=[]
    for i_tuple in seznam:
        s = []
        for ii in i_tuple:
            if ii==None:
                ii=hodnota_none # nahradí hodnoty None, co přišlo výsledek select z db
            s.append(ii)
        seznam_novy.append(s)
    return seznam_novy

def seznam_studentu():    
    """
    - seznam vsech studentu; 
    VSTUP: bez parametru
    VYSTUP: seznam studentu - [student1, student2]
    """  
    conn, cursor = pripojeni_db()
    cursor.execute(f''' SELECT jmeno from osoby''')     
    return select_to_seznam(cursor.fetchall())

def seznam_jazyku():
    """
    - seznam vsech jazyku v db;
    VSTUP: bez parametru
    VYSTUP: seznam jazyku - [jazyk1, jazyk2]
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f''' SELECT nazev from jazyky''')
    return select_to_seznam(cursor.fetchall())

def seznam_ucebnic(jazyk):
    """
     - seznam vsech ucebnic daneho jazyku
    VSTUP: jayzk - retezec
    VYSTUP: seznam ucebnic - [ucebnice1, ucebnice2,...]
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f''' select u.nazev from ucebnice u
	                        join jazyky j on u.jazyk_id = j.id
                        where j.nazev = '{jazyk}' order by j.nazev''')     
    return select_to_seznam(cursor.fetchall())

def seznam_vsech_ucebnic():
    """
     - seznam vsech ucebnic daneho jazyku
    VSTUP: jayzk - retezec
    VYSTUP: seznam ucebnic - [ucebnice1, ucebnice2,...]
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f''' select u.nazev from ucebnice u
	                        join jazyky j on u.jazyk_id = j.id
                        order by j.nazev''')     
    return select_to_seznam(cursor.fetchall())

def seznam_lekci(ucebnice):
    """
    - seznam vsech lekci dane ucebnice
    VSTUP: ucebnice - retezec
    VYSTUP: seznam dvojic - [(id1, lekce1),(id2, lekce2)]
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f''' select l.cislo, l.nazev from ucebnice u
	                        join lekce l on l.ucebnice_id = u.id
                    where u.nazev = '{ucebnice}'
                    order by l.cislo
                    ''')     
    return cursor.fetchall()

def jazyky_studenta(jmeno_studenta):
    """
    - seznam vsech jazyku daneho studenta
    VSTUP: jmeno_studenta - retezec
    VYSTUP: [jazyk1, jazyk2, ....]
    """      
    conn, cursor = pripojeni_db()
    try:
        cursor.execute(f''' SELECT id from osoby where jmeno ='{jmeno_studenta}'  ''')
        id_studenta = cursor.fetchone()[0]
    except:
        return f"Student jménem {jmeno_studenta} není v databázi"
    cursor.execute(f''' SELECT j.nazev from jazyky j join osoby_jazyky oj on oj.jazyk_id = j.id where oj.osoba_id={id_studenta}''')
    return select_to_seznam(cursor.fetchall())

def uloz_akt_jazyk(jazyk, jmeno_studenta):
    conn, cursor = pripojeni_db()
    cursor.execute(f''' SELECT id from jazyky where nazev ='{jazyk}'  ''')
    jazyk_id = cursor.fetchone()[0]
    cursor.execute(f'''UPDATE OSOBY SET AKT_JAZYK_ID = {jazyk_id} WHERE JMENO = '{jmeno_studenta}' ''')
    conn.commit()

def akt_jazyk_studenta(jmeno_studenta):
    """
    - vrati aktualni jazyk studenta
    VSTUP: jmeno_studenta - retezec
    VYSTUP: aktualni jazyk studenta
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f''' SELECT count(j.nazev) from jazyky j join osoby o on o.akt_jazyk_id = j.id where o.jmeno='{jmeno_studenta}'  ''')
    if cursor.fetchone()[0] == 0:
        return "" # student nemá nastavený akt_jazyk
    else:
        cursor.execute(f''' SELECT j.nazev from jazyky j join osoby o on o.akt_jazyk_id = j.id where o.jmeno='{jmeno_studenta}'  ''')
        return cursor.fetchone()[0]


def pridej_slovicka(seznam_slovicek):
    # 0. parametr-lekce
    # 1. parametr-seznam seznamů slovíček
    
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT id from lekce where nazev = "{seznam_slovicek[0]}"''')     
    id_lekce = cursor.fetchone()[0]
    seznam_slovicek.pop(0) # zbyde seznam slovíček
    for slovo in seznam_slovicek:     
        cursor.execute(f'''INSERT INTO SLOVICKA values (null,"{slovo[0]}", "{slovo[1]}", {id_lekce}) ''')
    conn.commit()
    cursor.execute(f'''SELECT count(*) from slovicka where lekce_id = {id_lekce}''')
    return cursor.fetchone()[0]

def slovicka_lekce(lekce, student):
    """
    - vrati seznam slovicek lekce vcetne poctu spravnych/spatnych odpovedi od daneho studenta
    VSTUP: lekce - retezec
            student - retezec
    VYSTUP: seznam slovicek [(id,cesky,preklad, spravne, spatne),(id,cesky,preklad, spravne, spatne),.... ]
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT id from lekce where nazev = "{lekce}"''')     
    id_lekce = cursor.fetchone()[0]

    cursor.execute(f'''SELECT id from osoby where jmeno = "{student}"''')     
    id_studenta = cursor.fetchone()[0]
    
    cursor.execute(f''' SELECT s.id,s.cz, s.preklad,pocet_spravne, pocet_spatne from slovicka s
                            LEFT JOIN (select ts.pocet_spravne, ts.pocet_spatne, ts.slovicko_id 
                                        from testovana_slovicka ts where ts.osoba_id={id_studenta})                         
                            ON slovicko_id = s.id 
                        where s.lekce_id = {id_lekce} ''')
                    
    return seznam_tuple2senam_seznamu(cursor.fetchall(),0)


def nacti_vysledky(student, ucebnice):
    """
    - vrati seznam výsledků studenta pro vybranou učebnici
    VSTUP: student - retezec
            ucebnice - retezec
    VYSTUP: seznam vysledku [[datum,lekce,hodnoceni,testovano_slov],[datum,lekce,hodnoceni],.... ]
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT id from osoby where jmeno = "{student}"''')     
    id_student = cursor.fetchone()[0]
    cursor.execute(f'''SELECT id from ucebnice where nazev = "{ucebnice}"''')     
    id_ucebnice = cursor.fetchone()[0]
    
    seznam_vysledku = []
    cursor.execute(f'''SELECT v.datum,l.nazev,v.uspesnost,v.testovano_slov from vysledky v
                        join lekce l on l.id=v.lekce_id
                        where osoba_id = {id_student} 
                        and lekce_id in (select id from lekce where ucebnice_id ={id_ucebnice})
                        order by v.datum
                        ''')
    
    return cursor.fetchall()

    


def nastaveni_studenta(student):
    """
    - vrací nastavení studenta
    VSTUP: student - retezec
    VYSTUP: (pocet_testovanych_slovicek, pocet_spravne_kdy_uz_netestovat,pocet_opakovani_testu,typ_prekladu, testovat_jen_spatne, rychlost_reci)
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT pocet_test_slovicek, pocet_spravne_netestovat, pocet_opakovani_testu,
    typ_prekladu, testovat_jen_spatne, rychlost_reci
        from osoby where jmeno = "{student}"''')  
    return list(cursor.fetchone())

def uloz_nastaveni_studenta(data_studenta):
    """
    - ulozi nastaveni studenta
    VSTUP: ["student", pocet_testovanych_slovicek, pocet_spravne_kdy_uz_netestovat,pocet_opakovani_testu,typ_prekladu, testovat_jen_spatne, rychlost_cteni]
    """
    conn, cursor = pripojeni_db()

    cursor.execute(f'''update osoby set pocet_test_slovicek = {data_studenta[1]},
    pocet_spravne_netestovat = {data_studenta[2]},
    pocet_opakovani_testu = {data_studenta[3]},
    typ_prekladu = {data_studenta[4]}, 
    testovat_jen_spatne = {data_studenta[5]},
    rychlost_reci = {data_studenta[6]}
    where jmeno = "{data_studenta[0]}" ''') 
    conn.commit()
    return

def uloz_dalsi_jazyk_studentovi(student,jazyk):
    """
    - seznam vsech jazyku v db;
    VSTUP: "student"
    VYSTUP: uloženo v db
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT id from osoby where jmeno = "{student}"''')     
    id_studenta = cursor.fetchone()[0]  
    cursor.execute(f'''SELECT id from jazyky where nazev = "{jazyk}"''')     
    id_jazyk = cursor.fetchone()[0]    
    cursor.execute(f'''SELECT count(*) from osoby_jazyky where osoba_id = {id_studenta} and jazyk_id = {id_jazyk}''')     
    pocet = cursor.fetchone()[0]  
    if pocet == 0: # v db student ještě nemá zvolený jazyk
        cursor.execute(f'''INSERT INTO osoby_jazyky VALUES({id_studenta},{id_jazyk},NULL)''')     
    conn.commit()
    return


def  uloz_test_studenta(data):
    """
    - uloží výsledek testu
    VSTUP: seznam dat ["student","lekce",hodnoceni,[id_slovicka,pocet_spravne,pocet_spatne],[id_slovicka,pocet_spravne,pocet_spatne],... ]
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT id from osoby where jmeno = "{data[0]}"''')     
    id_studenta = cursor.fetchone()[0]
    cursor.execute(f'''SELECT id from lekce where nazev = "{data[1]}"''')     
    lekce_id = cursor.fetchone()[0]
    hodnoceni = data[2]
    # ze seznamu odstraní první hodnoty, aby zbyl čistý seznam se slovíčky a údaji
    data.pop(2)
    data.pop(1)
    data.pop(0)
    pocet_slov = str(len(data))
    # ukládání informací ke slovíčkám - správné/špatné odpovědi
    for slovo in data: 
        if slovo[1] == 0 and slovo[2] == 0: #slovo nebylo testováno(přišlo s nulovými počty)
            pass
        else: 
            cursor.execute(f'''SELECT count(*) from testovana_slovicka 
                        where slovicko_id = {slovo[0]} and osoba_id={id_studenta}''')
            if  cursor.fetchone()[0] > 0: #slovíčko už je v tabulce testovana_slovicka --> UPDATE pocet_spravne, pocet_spatne
                cursor.execute(f'''UPDATE testovana_slovicka 
                                    SET pocet_spravne = pocet_spravne + {slovo[1]} 
                                    where slovicko_id = {slovo[0]} and osoba_id={id_studenta}
                                ''')
                cursor.execute(f'''UPDATE testovana_slovicka 
                                    SET pocet_spatne = pocet_spatne + {slovo[2]} 
                                    where slovicko_id = {slovo[0]} and osoba_id={id_studenta}
                                ''')
            else: # slovíčko ještě není v tabulce testovana_slovicka
                cursor.execute(f'''INSERT INTO testovana_slovicka 
                                VALUES({id_studenta},{slovo[0]},{slovo[1]}, {slovo[2]})''')
    now = datetime.datetime.now()
    akt_datum = str(now.year)+ "_" + str(now.month) + "_" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute)
    cursor.execute(f'''INSERT INTO vysledky  
                                VALUES(null,{id_studenta},{lekce_id},{hodnoceni},datetime("{now}"), '{pocet_slov}'
                                )''')
    conn.commit()  

def reset_slovicek(student,lekce):
    """
    - resetuje hodnoty pocet_spravne, pocet_spatne pro danou lekci a studenta
    VSTUP: student,lekce - retezce
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT id from osoby where jmeno = "{student}"''')     
    id_studenta = cursor.fetchone()[0]
    cursor.execute(f'''SELECT id from lekce where nazev = "{lekce}"''')     
    id_lekce = cursor.fetchone()[0]
    cursor.execute(f'''DELETE from testovana_slovicka 
                    where osoba_id={id_studenta} 
                    and slovicko_id in(select id from slovicka where lekce_id={id_lekce}) ''')
    conn.commit()  


def nazev_lekce_bez_ucebnice(lekce):
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT ucebnice_id from lekce where nazev = "{lekce}"''')     
    id_ucebnice = cursor.fetchone()[0]
    cursor.execute(f'''SELECT nazev from ucebnice where id = "{id_ucebnice}"''') 
    nazev_ucebnice = cursor.fetchone()[0]
    return lekce.replace(' - '+ nazev_ucebnice,"")

def export_lekce(lekce,jazyk, adr=''): 
    """
    - exportuje slovicka zvolene lekce do adresare Export 
                            (pro lekci může být bez zadání 3.partametru)
                            (pro učebnici se zadáním 3.parametru = název učebnice)
    VSTUP: lekce,jazyk, adr
    """    
    
    if not os.path.exists('Export'):
        os.makedirs('Export')

    if adr !='':
        adresar = 'Export/' + adr + '/'  # při exportu celé učebnice budou lekce v adresáři s názvem lekce        
    else:
        adresar = 'Export/'
    if not os.path.exists(adresar):
        os.makedirs(adresar)

    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT id, cislo from lekce where nazev = "{lekce}"''')     
    id_lekce, cislo_lekce = cursor.fetchone()    
    cursor.execute(f'''SELECT cz,preklad from slovicka where lekce_id = {id_lekce}                         
                        ''')
    slovicka = cursor.fetchall()    
    nazev_souboru = str(cislo_lekce) + '_' + nazev_lekce_bez_ucebnice(lekce) + '.txt'

    with open(adresar + nazev_souboru, mode='w', encoding='utf-8') as soubor:
        print('cz/preklad', file = soubor)
        for slovo in slovicka:
            print(slovo[0] + '/' + slovo[1], file = soubor)   
    
def export_ucebnice(ucebnice,jazyk): 
    """
    - exportuje slovíčka celé učebnice do adresáře Export, podadresářem název učebnice                            
    VSTUP: učebnice, jazyk
    """       
    conn, cursor = pripojeni_db()
    seznam = seznam_lekci(ucebnice)
    for l in seznam:
        export_lekce(l[1],jazyk,ucebnice)


def smaz_slovicka_lekce(lekce):
    """
    - vymaže slovíčka zvolené lekce
    """
    conn, cursor = pripojeni_db()
    cursor.execute(f'''SELECT id from lekce where nazev = "{lekce}"''')     
    id_lekce = cursor.fetchone()[0]   
    cursor.execute(f''' DELETE from SLOVICKA where lekce_id = {id_lekce} ''')
    conn.commit()
    return

def export_vseho():
    seznam_ucebnic = seznam_vsech_ucebnic()
    jazyk = ""
    for l in seznam_ucebnic:
        export_ucebnice(l, jazyk)

        
#reset_slovicek("Lenka","Greeting colors numbers")

#print(nastaveni_studenta("Lenka"))
# vypíše nápovědu ke konkrétní funkci
# help(jazyky_studenta)
# help(seznam_studentu)

#zkušební kód       
 
#conn, cursor = pripojeni_db()
"""
uloz_nastaveni_studenta(["Lenka",2,3,2,3,2])

print(nastaveni_studenta("Lenka"))

cursor.execute(f'''SELECT count(*) from slovicka where lekce_id =100''')
print(cursor.fetchone()[0])
"""

"""
d = ["Lenka","Greeting colors numbers",8,[1,1,3],[12,3,2], [11,3,0]]
uloz_test_studenta(d)
"""

"""
uloz_dalsi_jazyk_studentovi("Lenka", "Fr")
print(jazyky_studenta("Lenka"))
"""