import logging #používal jsem pro debugování, přijde mi přehlednější než všude dávat print()

#otevře soubor a vloží jeho obsah do slovníku
def open_file(f):
    dictionary = {}
    for line in f:
        (key, hodnota) = line.split()
        dictionary[(key)] = hodnota
    return dictionary

#sifruje/desifruje heslo
def sifruj(vstup,slovnik):
    global sifra
    sifra = ""
    for znak in vstup:
        if znak in slovnik.keys():
            sifra += slovnik[znak]
        else:
            sifra += znak
    return sifra

#vloží obsah slovníku do souboru
def add_to_file(soubor, h):
    file = open(soubor, "w")
    for klic,hodnota in h.items():
        file.write(klic + "\t" + hodnota + "\n")
    file.close()

#zeptá se uživatele zda chce pokračovat v použití programu
def opak():
    opakuj = input(f"{dashline} \nPřeješ si pokračovat nebo chceš opustit? [p = pokračuj | u = ukončit] ")
    if opakuj == "p":
        start()
    elif opakuj == "u":
        exit()
    else:
        print(f"{dashline}\nZadal si neplatnou možnost!\n{dashline}")
        opak()

#podprogram na zápis zašifrovného hesla do souboru
def zapis_hesla(slovnik):
    nazev_souboru = input('Zadej název textového souboru se zašifrovanými hesly ve formátu "název.txt": ')  #otevře soubor a převede ho do slovníku
    soubor_s_hesly = open(nazev_souboru)
    radky_hesel = soubor_s_hesly.readlines()
    hesla = open_file(radky_hesel)
    #logging.debug(hesla)
    soubor_s_hesly.close()
    nazev_klice = input("Zadej pod kterým názvem chceš heslo vyvolávat: ") # zeptá se uživatele na název pod kterým chce heslo uložit
    heslo = input("Zadej heslo které si přeješ uložit: ") # zeptá se uživatele na heslo
    if heslo == "" or nazev_klice == "": # pokud heslo nebo název je prázdný, donutí uživatele opakovat akci
        print(f"{dashline}\nZadal si prázdný řetězec, prosím opakuj akci\n{dashline}")
        zapis_hesla(slovnik)
    else: # pokud je řetězec plný
        heslo = sifruj(heslo,slovnik) #zašifruje heslo
        #logging.debug(heslo)
        hesla.update({nazev_klice:heslo}) #vloží heslo do předtím načteného slovníku
        add_to_file(nazev_souboru, hesla) # vloží slovník do souboru
        print(f"{dashline} \nHeslo bylo úspěšně zašifrováno a přidáno do souboru! \n{dashline}") #informuje uživatele že se heslo uložilo
        opak() #zeptá se uživatele na zda chce opakovat akci

# vyhledá heslo pomocí klíče se slovníku
def vyhledani_hesla(slovnik):
    nazev_souboru = input('Zadej název textového souboru se zašifrovanými hesly ve formátu "název.txt": ') #otevře soubor a převede ho do slovníku
    soubor_s_hesly = open(nazev_souboru)
    radky_hesel = soubor_s_hesly.readlines()
    hesla = open_file(radky_hesel)
    soubor_s_hesly.close()
    print("Výpis všech uložených hesel: ") #vypíše všechny názvy hesel (klíče) ze slovníku
    for key in hesla.keys():
        print(key)
    klic = input(f"{dashline}\nZadej název hesla které chceš vyhledat a rozšifrovat: ") #zeptá se uživatele na klíč

    if klic in hesla:
        print(f'Pro klic "{klic}" jsme našli toto heslo: {hesla[klic]}') #vypíše nerozšifrované heslo
        desifrovat = input("Přejete si rozšifrovat toto heslo? A/N: ") #zeptá se uživatele zda chce heslo dešifrovat
        if desifrovat == "A" or desifrovat == "a": #dešifruje heslo
            dictionary = {hodnota: klic for klic, hodnota in slovnik.items()}
            heslo = hesla[klic]
            print(f'Tvé rozšifrované heslo je: "{sifruj(heslo,dictionary)}"')
            opak()
        elif desifrovat == "N" or desifrovat == "n": #nedešifruje heslo
            print("Heslo jsme nedeširovali, vracíme vás do hlavního menu.")
            start()
        else: #spustí se pokud uživatel zadá špatnou hodnotu, vrátí ho do menu
            print("Zadali jste špatnou hodnotu, prosím opakujte akci")
            start()
    else: #pokud uživatel zadá neexistující klíč, zeptá se ho zda chce opakovat
        opakuj = input(f'Pro klic "{klic} jsme nenalezli zadne heslo, prejete si opakovat vyhledavani? A/N:')
        if opakuj == "A" or opakuj == "a":
            vyhledani_hesla(slovnik)
        elif opakuj == "N" or opakuj == "n":
            start()
        else:
            print("Zadali jste spatnou hodnotu, prosím restartujte program")
            exit()

#hlavní menu programu
def start():
    soubor = open("znaky.txt")
    obsah = soubor.readlines()
    dictionary = open_file(obsah)

    print(f"{dashline} \n\t\t\t  Vítej ve správcí hesel! \n{dashline}")

    akce = input("Co si přejete dělat za akci?: [z = zápis hesla, v = vyhledání hesla]: ") #dá uživateli možnost výběru akce

    if akce == "z":
        zapis_hesla(dictionary)
    elif akce == "v":
        vyhledani_hesla(dictionary)
    else:
        print("Zadal jsi špatnou akci, prosím opakuj")
        start()

#nastavení pro logování do konzole
format = '[%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format)

# LINE SETS
dashline = "═══════════════════════════════════════════════════"
start()