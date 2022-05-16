CREATE TABLE OSOBY (
	ID integer PRIMARY KEY AUTOINCREMENT,
	jmeno text,
	akt_jazyk_id integer,
	pocet_test_slovicek integer DEFAULT 20,
	pocet_spravne_netestovat integer DEFAULT 3,
	pocet_opakovani_testu integer DEFAULT 2,
	typ_prekladu integer DEFAULT 3,
	testovat_jen_spatne integer DEFAULT 2,
	rychlost_reci integer DEFAULT 0		
	
);

CREATE TABLE UCEBNICE (
	ID integer PRIMARY KEY AUTOINCREMENT,
	nazev varchar,
	jazyk_id integer
);

CREATE TABLE LEKCE (
	ID integer PRIMARY KEY AUTOINCREMENT,
	ucebnice_id integer,
	cislo integer,
	nazev varchar
);

CREATE TABLE SLOVICKA (
	ID integer PRIMARY KEY AUTOINCREMENT,
	cz varchar,
	preklad varchar,
	lekce_id integer
);

CREATE TABLE VYSLEDKY (
	ID integer PRIMARY KEY AUTOINCREMENT,
	osoba_id integer,
	lekce_id integer,
	uspesnost integer,
	datum datetime,
	testovano_slov varchar DEFAULT ''
);

CREATE TABLE TESTOVANA_SLOVICKA (
	osoba_id integer,
	slovicko_id integer,
	pocet_spravne integer DEFAULT 0,
	pocet_spatne integer DEFAULT 0

);

CREATE TABLE JAZYKY (
	ID integer PRIMARY KEY AUTOINCREMENT,
	nazev varchar,
	to_speak string
);

CREATE TABLE OSOBY_JAZYKY (
	osoba_id integer,
	jazyk_id integer,
	akt_ucebnice_id integer
);

CREATE TABLE INFO (
	nazev varchar,
	verze integer,
	platna_verze integer,
	platnost_od datetime,
	platnost_do datetime,
	popis varchar
);