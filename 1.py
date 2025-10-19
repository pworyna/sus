plik = "gieldaliczby.txt"

with open(plik, "r", encoding="utf-8") as f:
    dane = [linia.strip().replace(",", " ").split() for linia in f if linia.strip()]

liczba_kolumn = len(dane[0])
atrybuty = [f"a{i+1}" for i in range(liczba_kolumn - 1)] + ["d"]

print("TABELA DECYZYJNA")
for w in dane:
    print(w)

print("\nLICZBA MOŻLIWYCH WARTOŚCI KAŻDEGO ATRYBUTU\n")
for i, nazwa in enumerate(atrybuty):
    wartosci = [wiersz[i] for wiersz in dane]
    unikalne = sorted(set(wartosci))
    print(f"{nazwa}: {len(unikalne)} wartości -> {unikalne}")

print("\nLICZBA WYSTĄPIEŃ KAŻDEJ WARTOŚCI KAŻDEGO ATRYBUTU")
for i, nazwa in enumerate(atrybuty):
    wartosci = [wiersz[i] for wiersz in dane]
    unikalne = sorted(set(wartosci))
    print(f"\nAtrybut: {nazwa}")
    for val in unikalne:
        print(f"{val}: {wartosci.count(val)}")
