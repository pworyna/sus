import math
import re

def entropia(klasy_decyzyjne):
    if not klasy_decyzyjne:
        return 0
    liczniki = {klasa: klasy_decyzyjne.count(klasa) for klasa in set(klasy_decyzyjne)}
    return sum(-(licznik/len(klasy_decyzyjne)) * math.log2(licznik/len(klasy_decyzyjne)) for licznik in liczniki.values())

def raport_statystyczny(dane):
    liczba_kolumn = len(dane[0])
    for indeks in range(liczba_kolumn):
        kolumna = [wiersz[indeks] for wiersz in dane]
        statystyki = {wartosc: kolumna.count(wartosc) for wartosc in set(kolumna)}
        nazwa = "Decyzja" if indeks == liczba_kolumn - 1 else f"Atrybut warunkowy {indeks + 1}"
        print(f"{nazwa}: {len(statystyki)} unikalne wartości -> {statystyki}")
    print()

def warunekStopu(dane):
    klasy_decyzyjne = [wiersz[-1] for wiersz in dane]
    return len(set(klasy_decyzyjne)) == 1 or len(dane[0]) == 1

def wyborNajlepszegoPodzialu(dane, pokaz_obliczenia):
    klasy_decyzyjne = [wiersz[-1] for wiersz in dane]
    entropia_bazowa = entropia(klasy_decyzyjne)

    if pokaz_obliczenia:
        print(f"Entropia zbioru: {entropia_bazowa}")
        print("Gain(X,T) = Entropia zbioru - Info(X,T)\n")

    najlepszy_wspolczynnik = -1.0
    najlepszy_atrybut = -1

    for indeks_atrybutu in range(len(dane[0]) - 1):
        wartosci_atrybutu = set(wiersz[indeks_atrybutu] for wiersz in dane)
        info_x = 0
        split_info = 0

        for wartosc in wartosci_atrybutu:
            podzbior_klas = [wiersz[-1] for wiersz in dane if wiersz[indeks_atrybutu] == wartosc]
            waga = len(podzbior_klas) / len(dane)
            info_x += waga * entropia(podzbior_klas)
            split_info -= waga * math.log2(waga)

        zysk = entropia_bazowa - info_x
        wspolczynnik_zysku = zysk / split_info if split_info != 0 else 0

        if pokaz_obliczenia:
            print(f"    Info(Atrybut {indeks_atrybutu + 1}, T) = {info_x}")
            print(f"    Gain(Atrybut {indeks_atrybutu + 1}, T) = {zysk}")
            print(f"    GainRatio(Atrybut {indeks_atrybutu + 1}, T) = {wspolczynnik_zysku}")

        if wspolczynnik_zysku > najlepszy_wspolczynnik:
            najlepszy_wspolczynnik = wspolczynnik_zysku
            najlepszy_atrybut = indeks_atrybutu

    if pokaz_obliczenia:
        print(f"\n    Wybrany Atrybut A{najlepszy_atrybut + 1}, bo w tym przypadku najwyższa jest wartość GainRatio: {najlepszy_wspolczynnik}\n")

    return najlepszy_atrybut, najlepszy_wspolczynnik

def konstruujDrzewo(dane, pokaz_obliczenia=False):
    wezel = {'lisc': False, 'test': None, 'potomek': {}, 'decyzja': None}
    klasy_decyzyjne = [wiersz[-1] for wiersz in dane]

    if not warunekStopu(dane):
        atrybut, zysk = wyborNajlepszegoPodzialu(dane, pokaz_obliczenia)

        if zysk == 0:
            wezel['lisc'] = True
            wezel['decyzja'] = max(set(klasy_decyzyjne), key=klasy_decyzyjne.count)
        else:
            wezel['test'] = atrybut
            unikalne_wartosci = sorted(set(wiersz[atrybut] for wiersz in dane))
            for wartosc in unikalne_wartosci:
                dane_potomka = [wiersz for wiersz in dane if wiersz[atrybut] == wartosc]
                wezel['potomek'][wartosc] = konstruujDrzewo(dane_potomka, False)
    else:
        wezel['lisc'] = True
        wezel['decyzja'] = max(set(klasy_decyzyjne), key=klasy_decyzyjne.count)

    return wezel

def wizualizuj(wezel, wciecie=""):
    if wezel['lisc']:
        print(f"D: {wezel['decyzja']}")
        return

    print(f"Atrybut: {wezel['test'] + 1}")
    for wartosc, potomek in wezel['potomek'].items():
        prefix = wciecie + "          " + str(wartosc) + "->"
        print(prefix, end=(" " if potomek['lisc'] else ""))
        wizualizuj(potomek, wciecie + "          " + " " * len(str(wartosc)) + "  ")

if __name__ == "__main__":
    plik = 'test.txt'
    try:
        with open(plik, 'r') as uchwyt_pliku:
            dane = [re.split(r'[ ,;\t|]+', linia.strip()) for linia in uchwyt_pliku if linia.strip()]

        raport_statystyczny(dane)

        drzewo = konstruujDrzewo(dane, pokaz_obliczenia=True)

        wizualizuj(drzewo)

    except FileNotFoundError:
        print(f"Brak pliku {plik}")
