import math
import matplotlib.pyplot as plt

class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"

    @staticmethod
    def ccw(p1, p2, p3):
        return (p2.y - p1.y) * (p3.x - p2.x) < (p2.x - p1.x) * (p3.y - p2.y)

    @staticmethod
    def czytaj_z_pliku(nazwa_pliku):
        punkty = []
        with open(nazwa_pliku, 'r') as file:
            liczba_punktow = int(file.readline())
            for _ in range(liczba_punktow):
                x, y = map(float, file.readline().split())
                punkty.append(Punkt(x, y))
        return punkty

    def rysuj(self, marker='o', color='red', label="Punkt", markersize=5):
        plt.plot(self.x, self.y, marker=marker, markersize=markersize, color=color, label=label)

class Linia:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def dlugosc_linii(self):
        dlugosc = math.sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)
        return dlugosc

class BrylaBrzegowa:

    def __init__(self, krawedzie=None):
        if krawedzie is None:
            krawedzie = []
        self.krawedzie = krawedzie

    def rysuj(self):
        for krawedz in self.krawedzie:
            start, koniec = krawedz.point1, krawedz.point2
            plt.plot([start.x, koniec.x], [start.y, koniec.y], 'b-')
            plt.plot(start.x, start.y, 'ro')  # Rysuje wierzchołki
            plt.plot(koniec.x, koniec.y, 'ro')

        plt.title('Bryła Brzegowa')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axis('equal')
        plt.grid(True)

    def czy_wewnatrz(self, punkt):
        # Ray-casting algorithm do sprawdzania, czy punkt jest wewnątrz wielokąta
        liczba_przeciec = 0
        x_intercept = punkt.x + 1  # mała wartość, aby uniknąć problemów z precyzją float

        for krawedz in self.krawedzie:
            p1, p2 = krawedz.point1, krawedz.point2
            if min(p1.y, p2.y) <= punkt.y <= max(p1.y, p2.y):
                if p1.y != p2.y:
                    x_temp = p1.x + (punkt.y - p1.y) / (p2.y - p1.y) * (p2.x - p1.x)
                    if punkt.x <= x_temp:
                        liczba_przeciec += 1

        return liczba_przeciec % 2 == 1

class Otoczka:

    def __init__(self, punkty):
        self.punkty = punkty

    def rysuj(self):
        for i in range(len(self.punkty)):
            # Rysowanie linii między punktami
            x = [self.punkty[i].x, self.punkty[(i + 1) % len(self.punkty)].x]
            y = [self.punkty[i].y, self.punkty[(i + 1) % len(self.punkty)].y]
            plt.plot(x, y, label=f'Linia od {self.punkty[i]} do {self.punkty[(i + 1) % len(self.punkty)]}')

        for i, punkt in enumerate(self.punkty):
            plt.plot(punkt.x, punkt.y, marker='o')

        plt.axis('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Otoczka wypukła')
        plt.grid(True)
        #plt.show()

    @staticmethod
    def otoczka_wypukla_jarvisa(punkty):
        # Znajdź punkt o najniższej współrzędnej y (jeśli jest ich więcej, wybierz ten z najmniejszą współrzędną x)
        punkt_startowy = min(punkty, key=lambda punkt: (punkt.y, punkt.x))
        otoczka = [punkt_startowy]
        punkt_referencyjny = punkt_startowy
        punkty_do_przeszukania = punkty.copy()

        while True:
            # Wybierz następny punkt jako pierwszy z listy punktów do przeszukania
            nastepny_punkt = punkty_do_przeszukania[0]

            for punkt in punkty_do_przeszukania:
                if punkt == punkt_referencyjny:
                    continue

                # Sprawdź, czy punkt jest po lewej stronie od odcinka (punkt_referencyjny - nastepny_punkt)
                wektor = [nastepny_punkt.x - punkt_referencyjny.x, nastepny_punkt.y - punkt_referencyjny.y]
                wektor_do_punktu = [punkt.x - punkt_referencyjny.x, punkt.y - punkt_referencyjny.y]
                iloczyn_wektorowy = wektor[0] * wektor_do_punktu[1] - wektor[1] * wektor_do_punktu[0]

                if iloczyn_wektorowy < 0 or (
                        iloczyn_wektorowy == 0 and Linia(punkt_referencyjny, punkt).dlugosc_linii() > Linia(
                    punkt_referencyjny, nastepny_punkt).dlugosc_linii()):
                    nastepny_punkt = punkt

            punkt_referencyjny = nastepny_punkt
            if punkt_referencyjny == punkt_startowy:
                break

            otoczka.append(nastepny_punkt)
            punkty_do_przeszukania.remove(nastepny_punkt)

        return otoczka

    @staticmethod
    def otoczka_wypukla_grahama(punkty):
        punkty.sort(key=lambda p: (p.x, p.y))

        dolna_otoczka = []
        for p in punkty:
            while len(dolna_otoczka) >= 2 and not Punkt.ccw(dolna_otoczka[-2], dolna_otoczka[-1], p):
                dolna_otoczka.pop()
            dolna_otoczka.append(p)

        gorna_otoczka = []
        for p in reversed(punkty):
            while len(gorna_otoczka) >= 2 and not Punkt.ccw(gorna_otoczka[-2], gorna_otoczka[-1], p):
                gorna_otoczka.pop()
            gorna_otoczka.append(p)

        return dolna_otoczka[:-1] + gorna_otoczka[:-1]

    def czy_wewnatrz(self, punkt):
        liczba_przeciec = 0
        for i in range(len(self.punkty)):
            p1 = self.punkty[i]
            p2 = self.punkty[(i + 1) % len(self.punkty)]

            # Sprawdzanie, czy punkt leży na krawędzi
            if min(p1.y, p2.y) <= punkt.y <= max(p1.y, p2.y):
                if p1.y == p2.y:  # Linia pozioma
                    if min(p1.x, p2.x) <= punkt.x <= max(p1.x, p2.x):
                        return True
                else:  # Linia niepozioma
                    x_intercept = p1.x + (punkt.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)
                    if abs(punkt.x - x_intercept) < 1e-9:
                        return True

            # Sprawdzanie, czy punkt znajduje się wewnątrz wielokąta
            if p1.y != p2.y and punkt.x < (p1.x + (punkt.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)):
                liczba_przeciec += 1

        return liczba_przeciec % 2 == 1

    def czy_na_otoczce(self, punkt):
        epsilon = 1e-9
        for i in range(len(self.punkty)):
            p1 = self.punkty[i]
            p2 = self.punkty[(i + 1) % len(self.punkty)]
            if abs(Linia(p1, p2).dlugosc_linii() - (
                    Linia(p1, punkt).dlugosc_linii() + Linia(punkt, p2).dlugosc_linii())) < epsilon:
                return True
        return False

class Pocisk(Punkt):
    def __init__(self, czas, x, y, vx, vy):
        super().__init__(x, y)
        self.vx = vx
        self.vy = vy
        self.czas = czas

    def pozycja_w_czasie(self, t):
        return Punkt(self.x + self.vx * (t - self.czas), self.y + self.vy * (t - self.czas))

def wczytaj_pociski(nazwa_pliku):
    with open(nazwa_pliku, 'r') as plik:
        pociski = []
        for linia in plik:
            dane = list(map(float, linia.split()))
            pociski.append(Pocisk(dane[0], dane[1], dane[2], dane[3], dane[4]))
    return pociski

def symuluj_pole_walki(statek, pociski, dt, czas):
    t = 0
    krawedzie = []
    punkty_otoczki = Otoczka.otoczka_wypukla_jarvisa(statek)
    for i in range(len(punkty_otoczki)):
        krawedzie.append(Linia(punkty_otoczki[i], punkty_otoczki[(i + 1) % len(punkty_otoczki)]))

    bryla = BrylaBrzegowa(krawedzie)
    otoczka = Otoczka(punkty_otoczki)

    while t <= czas:
        plt.figure()
        bryla.rysuj()
        otoczka.rysuj()
        for pocisk in pociski:
            if t >= pocisk.czas:
                pozycja_pocisku = pocisk.pozycja_w_czasie(t)
                plt.plot(pozycja_pocisku.x, pozycja_pocisku.y, 'ro')

                if bryla.czy_wewnatrz(pozycja_pocisku):
                    if otoczka.czy_na_otoczce(pozycja_pocisku) or otoczka.czy_wewnatrz(pozycja_pocisku):
                        print(f'Obiekt został trafiony przez pocisk w czasie {t} sekund')
        plt.xlim(-500, 500)
        plt.ylim(-500, 500)
        plt.grid(True)
        plt.pause(dt)
        t += dt
    plt.show()

if __name__ == '__main__':
    statek = Punkt.czytaj_z_pliku('craft1_ksztalt.txt')
    pociski = wczytaj_pociski('missiles1.txt')
    symuluj_pole_walki(statek, pociski, 0.1, 2)

    # punkty_z_pliku = Punkt.czytaj_z_pliku("ksztalt_2.txt")
    # for punkt in punkty_z_pliku:
    #     punkt.rysuj()
    # plt.show()
    #
    # punkty_otoczki = Otoczka.otoczka_wypukla_jarvisa(punkty_z_pliku)
    # otoczka = Otoczka(punkty_otoczki)
    # otoczka.rysuj()
    # plt.show()