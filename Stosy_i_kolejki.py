# --- 1. STRUKTURA: STOS (LIFO) ---
class Stos:
    """Implementacja Stosu (LIFO) przy użyciu listy Pythona."""

    def __init__(self):
        self._items = []

    def push(self, element):
        """Dodaje element na wierzchołek stosu."""
        self._items.append(element)

    def is_empty(self):
        """Zwraca True, jeśli stos nie zawiera elementów."""
        return len(self._items) == 0

    def pop(self):
        """Usuwa i zwraca element z wierzchołka stosu. Zwraca None, jeśli pusty."""
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        """Zwraca element z wierzchołka, ale go nie usuwa. Zwraca None, jeśli pusty."""
        if self.is_empty():
            return None
        return self._items[-1]


# --- 2. STRUKTURA: KOLEJKA (FIFO) ---
class Kolejka:
    """Implementacja Kolejki (FIFO) przy użyciu listy Pythona."""

    def __init__(self):
        self._items = []

    def enqueue(self, element):
        """Dodaje element na koniec kolejki."""
        self._items.append(element)

    def dequeue(self):
        """Usuwa i zwraca element z początku kolejki. Zwraca None, jeśli pusta."""
        if self.is_empty():
            return None
        return self._items.pop(0)

    def is_empty(self):
        """Zwraca True, jeśli kolejka nie zawiera elementów."""
        return len(self._items) == 0

    def __len__(self):
        """Zwraca liczbę elementów w kolejce."""
        return len(self._items)

# ====================================================================
# CZĘŚĆ II: Wdrożenie Modułów Aplikacyjnych (Użycie Stosu i Kolejki)
# ====================================================================

# --- MODUŁ A: MENEDŻER HISTORII OPERACJI (STOS) ---
class MenedzerHistorii:
    """Symuluje mechanizm Undo przy użyciu klasy Stos."""

    def __init__(self):
        self.historia = Stos()
        print("\n--- INICJALIZACJA: Menedżer Historii ---")

    def wykonaj_akcje(self, opis):
        """Dodaje nową akcję do historii operacji."""
        self.historia.push(opis)
        print(f"Dodano akcję: {opis}")

    def cofnij(self):
        """Cofa ostatnią akcję i wyświetla komunikat."""
        akcja = self.historia.pop()
        if akcja is None:
            print("Brak akcji do cofnięcia.")
        else:
            print(f"Wycofano akcję: {akcja}")

    def aktualny_stan(self):
        """Wyświetla akcję, która zostanie cofnięta jako następna."""
        akcja = self.historia.peek()
        if akcja is None:
            print("Brak akcji w historii.")
        else:
            print(f"Następna akcja do cofnięcia: {akcja}")


# --- MODUŁ B: SYSTEM KOLEJKOWY ZGŁOSZEŃ (KOLEJKA) ---
class SystemZgloszen:
    """Symuluje system obsługi zgłoszeń (FIFO)."""

    def __init__(self):
        self.kolejka_zgloszen = Kolejka()
        print("\n--- INICJALIZACJA: System Zgłoszeń ---")

    def dodaj_zgloszenie(self, klient_id, kategoria):
        """Dodaje nowe zgłoszenie na koniec kolejki."""
        self.kolejka_zgloszen.enqueue((klient_id, kategoria))
        print(f"Dodano zgłoszenie: Klient {klient_id}, Kategoria: {kategoria}")

    def obsluz_nastepne(self):
        """Obsługuje zgłoszenie z początku kolejki."""
        zgloszenie = self.kolejka_zgloszen.dequeue()
        if zgloszenie is None:
            print("Brak zgłoszeń do obsłużenia.")
        else:
            print(f"Obsłużono klienta {zgloszenie[0]}, Kategoria: {zgloszenie[1]}")

    def liczba_oczekujacych(self):
        """Wyświetla ilu klientów czeka na obsługę."""
        print(f"Liczba oczekujących zgłoszeń: {len(self.kolejka_zgloszen)}")



if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("START TESTÓW PROJEKTOWYCH")
    print("=" * 60)

    print("\n" + "=" * 20 + " TEST MODUŁU A " + "=" * 20)
    menedzer = MenedzerHistorii()
    menedzer.wykonaj_akcje("Utworzono nowy plik")
    menedzer.wykonaj_akcje("Zapisano tytuł")
    menedzer.aktualny_stan()

    menedzer.cofnij()
    menedzer.wykonaj_akcje("Dodano obrazek")
    menedzer.cofnij()
    menedzer.cofnij()
    menedzer.cofnij()

    print("\n" + "=" * 20 + " TEST MODUŁU B " + "=" * 20)
    system = SystemZgloszen()
    system.dodaj_zgloszenie(10, "Sieć")
    system.dodaj_zgloszenie(20, "Konto")
    system.liczba_oczekujacych()

    system.obsluz_nastepne()
    system.dodaj_zgloszenie(30, "Płatność")
    system.liczba_oczekujacych()

    system.obsluz_nastepne()
    system.obsluz_nastepne()
    system.obsluz_nastepne()

    print("\n" + "=" * 60)
    print("KONIEC TESTÓW")
    print("=" * 60)
