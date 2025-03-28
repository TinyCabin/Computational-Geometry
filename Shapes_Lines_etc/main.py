import os
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
#import matplotlib.animation as animation

class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"

    def rysuj(self, marker='o', color='red', label="Punkt", markersize=5):
        plt.plot(self.x, self.y, marker=marker, markersize=markersize, color=color, label=label)


class Linia:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def rownanie(self):
        #Ax + By + C = 0 - postac ogolna | -By = Ax + C - postac kanoniczna(tylko bez B przed )
        A = self.point2.y - self.point1.y
        B = self.point1.x - self.point2.x
        C = self.point2.x * self.point1.y - self.point1.x * self.point2.y
        return A, B, C

    def wypisz_rownanie(self):
        A, B, C = self.rownanie()
        return f"({-B}y = {A}x + {C})"

    def przynaleznosc_prosta(self, point):
        A, B, C = self.rownanie()
        return A * point.x + B * point.y + C == 0

    def przynaleznosc_odcinek(self, point):
        A, B, C = self.rownanie()
        rownanie = A * point.x + B * point.y + C
        if rownanie == 0:
            pomiedzy_x = min(point1.x, point2.x) <= point.x <= max(point1.x, point2.x)
            pomiedzy_y = min(point1.y, point2.y) <= point.y <= max(point1.y, point2.y)
            if pomiedzy_x and pomiedzy_y:
                return "Nalezy do odcinka"
            else:
                return "Nalezy do prostej, nie odcinka"
        else:
            return "Nie należy do odcinka"

    def przynaleznosc_odcinek_bool(self, point):
        A, B, C = self.rownanie()
        rownanie = A * point.x + B * point.y + C
        if rownanie == 0:
            pomiedzy_x = min(point1.x, point2.x) <= point.x <= max(point1.x, point2.x)
            pomiedzy_y = min(point1.y, point2.y) <= point.y <= max(point1.y, point2.y)
            if pomiedzy_x and pomiedzy_y:
                return True
            else:
                return False
        else:
            return False

    def przynaleznosc_punktu_prosta(self, point):
        A, B, C = self.rownanie()
        value = A * point.x + B * point.y + C
        if value > 0:
            return "Prawo"
        elif value < 0:
            return "Lewo"
        else:
            return "Na linii"

    def translacja(self, wektor):
        self.point1.x += wektor.x
        self.point1.y += wektor.y
        self.point2.x += wektor.x
        self.point2.y += wektor.y

    def odbicie_punktu_wzgledem_prostej(self, punkt):
        A, B, C = self.rownanie()

        punkt_przeciecia_x = (B * (B * punkt.x - A * punkt.y) - A * C) / (A ** 2 + B ** 2)
        punkt_przeciecia_y = (A * (-B * punkt.x + A * punkt.y) - B * C) / (A ** 2 + B ** 2)
        #punkt_przecia = (punkt_przeciecia_x,punkt_przeciecia_y)

        odleglosc_x = punkt_przeciecia_x - punkt.x
        odleglosc_y = punkt_przeciecia_y - punkt.y
        wektor_odl = Punkt(odleglosc_x, odleglosc_y)
        odwrocony_wektor = Punkt(-1 * wektor_odl.x, -1 * wektor_odl.y)

        odbity = Punkt(punkt_przeciecia_x - odwrocony_wektor.x, punkt_przeciecia_y - odwrocony_wektor.y)
        x = round(odbity.x, 2)
        y = round(odbity.y, 2)
        koncowy_punkty = Punkt(x,y)
        return koncowy_punkty

    @staticmethod
    def punkt_przeciecia_postac_ogolna(linia1, linia2):
        A1, B1, C1 = linia1.rownanie()
        A2, B2, C2 = linia2.rownanie()

        W = A1 * B2 - B1 * A2
        Wx = -C1 * B2 + B1 * C2
        Wy = -A1 * C2 + C1 * A2

        if W != 0:
            x = Wx / W
            y = Wy / W
            return Punkt(x, y)
        else:
            return None

    @staticmethod
    def punkt_przeciecia_dwoch_linii(linia1, linia2):
        x1, y1, x2, y2 = linia1.point1.x, linia1.point1.y, linia1.point2.x, linia1.point2.y
        x3, y3, x4, y4 = linia2.point1.x, linia2.point1.y, linia2.point2.x, linia2.point2.y

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        return Punkt(px, py)

    def odleglosc_od_punktu_do_prostej(self, punkt):
        A, B, C = self.rownanie()
        odleglosc_do_prostej = abs(A * punkt.x + B * punkt.y + C) / math.sqrt(A ** 2 + B ** 2)
        return odleglosc_do_prostej

    def odleglosc_punktu_przeciecia_do_odcinka(self, punkt):
        if self.przynaleznosc_odcinek_bool(punkt):
            return 0
        else:
            odleglosc_do_punkt1 = math.sqrt((punkt.x - self.point1.x)**2 + (punkt.y - self.point1.y)**2)
            odleglosc_do_punkt2 = math.sqrt((punkt.x - self.point2.x)**2 + (punkt.y - self.point2.y)**2)
            return min(odleglosc_do_punkt1, odleglosc_do_punkt2)

    def dlugosc_linii(self):
        dlugosc = math.sqrt((self.point1.x - self.point2.x)**2 + (self.point1.y - self.point2.y)**2)
        return dlugosc

    @staticmethod
    def kat_pomiedzy_liniami(linia1, linia2):
        modul_u = linia1.dlugosc_linii()
        modul_v = linia2.dlugosc_linii()
        wektor_u = [linia1.point1.x - linia1.point2.x, linia1.point1.y - linia1.point2.y]
        wektor_v = [linia2.point1.x - linia2.point2.x, linia2.point1.y - linia2.point2.y]
        modul_uv = abs((wektor_u[0]*wektor_v[0]) + (wektor_u[1]*wektor_v[1]))
        kat = math.acos(modul_uv/(modul_u * modul_v))
        kat = (180*kat)/math.pi
        return round(kat, 3)


    def rysuj(self):
        x = [self.point1.x, self.point2.x]
        y = [self.point1.y, self.point2.y]
        plt.plot(x, y, label=f'Linia od {self.point1} do {self.point2}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Wykres')
        plt.grid(True)

    def rysuj_kat(ax, linia1, linia2, color='red'):
        angle = Linia.kat_pomiedzy_liniami(linia1, linia2)

        vec1 = [linia1.point2.x - linia1.point1.x, linia1.point2.y - linia1.point1.y]
        vec2 = [linia2.point2.x - linia2.point1.x, linia2.point2.y - linia2.point1.y]

        wedge = patches.Wedge(center=(linia1.point1.x, linia1.point1.y), r=0.5,
                              theta1=np.degrees(np.arctan2(vec1[1], vec1[0])),
                              theta2=np.degrees(np.arctan2(vec2[1], vec2[0])), color=color)
        ax.add_patch(wedge)

class Trojkat:

    def __init__(self, punkt1, punkt2, punkt3):
        if self.czy_wspolliniowe(punkt1, punkt2, punkt3):
            raise ValueError("Punkty są współliniowe, nie można utworzyć trójkąta")
        self.punkt1 = punkt1
        self.punkt2 = punkt2
        self.punkt3 = punkt3

    @staticmethod
    def czy_wspolliniowe(p1, p2, p3):
        linia = Linia(p1, p2)
        return linia.przynaleznosc_odcinek_bool(p3)


    @staticmethod
    def stworz_na_podstawie_prostych(prosta1, prosta2, prosta3):
        punkt1 = Linia.punkt_przeciecia_postac_ogolna(prosta1, prosta2)
        punkt2 = Linia.punkt_przeciecia_postac_ogolna(prosta2, prosta3)
        punkt3 = Linia.punkt_przeciecia_postac_ogolna(prosta3, prosta1)

        if punkt1 and punkt2 and punkt3 and punkt1 != punkt2 and punkt2 != punkt3 and punkt1 != punkt3:
            Trojkat(punkt1, punkt2, punkt3)
        else:
            return None

    def oblicz_pole(self):
        bok_a = Linia(self.punkt1, self.punkt2).dlugosc_linii()
        bok_b = Linia(self.punkt2, self.punkt3).dlugosc_linii()
        bok_c = Linia(self.punkt1, self.punkt3).dlugosc_linii()
        p = 1/2 * (bok_a + bok_b + bok_c)
        area = math.sqrt(p*(p-bok_a)*(p-bok_b)*(p-bok_c))
        return round(area, 5)

    def punkt_przynalezny_1(self, punkt):
        punkty = [(self.punkt1, self.punkt2), (self.punkt2, self.punkt3), (self.punkt3, self.punkt1)]
        S=0.0
        for punkt1, punkt2, in punkty:
            if Trojkat.czy_wspolliniowe(punkt1, punkt2,punkt) == False:
                S += Trojkat(punkt1, punkt2, punkt).oblicz_pole()
            else:
                return "Punkt lezy na prostej trojkata"

        Pole = self.oblicz_pole()
        if S == Pole:
            return "Punkt znajduje sie wewnatrz trojkata"
        elif S > Pole:
            return "Punkt znajduje sie poza trojkatem"

    def punkt_przynalezny_2(self, punkt):
        punkty = [(self.punkt1, self.punkt2), (self.punkt2, self.punkt3), (self.punkt3, self.punkt1)]
        strona = []
        for punkt1, punkt2 in punkty:
            linia = Linia(punkt1, punkt2)
            A, B, C = linia.rownanie()
            wynik = A * punkt.x + B * punkt.y + C
            strona.append(wynik > 0)
        return all(strona) or not any(strona)

    def rysuj(self):
        # Rysowanie linii
        linia1 = Linia(self.punkt1, self.punkt2)
        linia2 = Linia(self.punkt2, self.punkt3)
        linia3 = Linia(self.punkt3, self.punkt1)
        linia1.rysuj()
        linia2.rysuj()
        linia3.rysuj()

        plt.plot(self.punkt1.x, self.punkt1.y, marker='o', color='blue')
        plt.plot(self.punkt2.x, self.punkt2.y, marker='o', color='orange')
        plt.plot(self.punkt3.x, self.punkt3.y, marker='o', color='green')

        plt.axis('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Trójkąt')
        plt.grid(True)
        #plt.show()

class Wielokat:

    def __init__(self, punkty):
        if len(punkty) < 3:
            raise ValueError("Za mało punktów do utworzenia wielokąta")
        if len(punkty) == 3:
            punkt1, punkt2, punkt3 = punkty
            Trojkat(punkt1, punkt2, punkt3)
        self.punkty = punkty

    def punkt_przynalezny(self, punkt):
        liczba_przeciec = 0
        for i in range(len(self.punkty) - 1):
            punkt1, punkt2 = self.punkty[i], self.punkty[i + 1]

            #Na Wierzcholek
            if (punkt.x == punkt1.x and punkt.y == punkt1.y) or (punkt.x == punkt2.x and punkt.y == punkt2.y):
                return True

            # Na Linii
            if min(punkt1.y, punkt2.y) <= punkt.y <= max(punkt1.y, punkt2.y):
                if punkt1.y == punkt2.y:  # Linia pozioma
                    if min(punkt1.x, punkt2.x) <= punkt.x <= max(punkt1.x, punkt2.x):
                        return True
                else:  # Linia niepozioma
                    x = punkt1.x + ((punkt.y - punkt1.y) / (punkt2.y - punkt1.y)) * (punkt2.x - punkt1.x)
                    if abs(punkt.x - x) < 1e-9:
                        return True

                # wewnątrz wielokąta
                if punkt.x < (punkt1.x + ((punkt.y - punkt1.y) / (punkt2.y - punkt1.y)) * (punkt2.x - punkt1.x)):
                    liczba_przeciec += 1

        return liczba_przeciec % 2 == 1

    def rysuj(self):
        for i in range(len(self.punkty)):
            # Rysowanie linii między punktami
            x = [self.punkty[i].x, self.punkty[(i + 1) % len(self.punkty)].x]
            y = [self.punkty[i].y, self.punkty[(i + 1) % len(self.punkty)].y]
            plt.plot(x, y, label=f'Linia od {self.punkty[i]} do {self.punkty[(i + 1) % len(self.punkty)]}')

        # Rysowanie punktów
        for i, punkt in enumerate(self.punkty):
            plt.plot(punkt.x, punkt.y, marker='o')

        plt.axis('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Wielokąt')
        plt.grid(True)
        #plt.show()

def wizualizacja(points, lines=None):
    fig, ax = plt.subplots()
    for point in points:
        ax.scatter(point.x, point.y, color='red', label='Point')
    for line in lines:
        ax.plot([line.point1.x, line.point2.x], [line.point1.y, line.point2.y], color='blue')
    ax.set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Wykres')
    plt.grid(True)
    plt.show()



point1 = Punkt(3, 6)
point2 = Punkt(2, 3)
point3 = Punkt(5,3)
point4 = Punkt(4,6)
point5 = Punkt(2.5,3.5)
point6 = Punkt(3.5,4.5)
punkty = (point1, point2, point3,point4,point5)
#-------------------------------------------





#-------------------------------------------

multibok = Wielokat(punkty)

print(f"Punkt {point6} lezy na wielokacie: ", multibok.punkt_przynalezny(point6))

multibok.rysuj()
point6.rysuj(marker='*', color='purple', markersize=10)
#plt.legend()
plt.show()



# trojkat = Trojkat(point1, point2, point3)
# trojkat.rysuj()
# pole = trojkat.oblicz_pole()
# print(f"Wartosc pola trojkata wynosi {pole}")
#
#
# print(f"Czy punkt przynalezy do trojkata:", trojkat.punkt_przynalezny_2(point5))
# point5.rysuj(marker='*', color='purple', markersize=10)
# plt.show()


# linia1 = Linia(point1, point2)
# linia2 = Linia(point5, point2)
# kat = Linia.kat_pomiedzy_liniami(linia1, linia2)
# print(f"Kat pomiedzy prostymi = {kat} stopni")

# fig, ax = plt.subplots()
#
# linia1.rysuj()
# linia2.rysuj()
#
# Linia.rysuj_kat(ax, linia1, linia2)
#
# plt.axis()
# plt.legend()
# plt.show()

#-------------------------------------------





#------------------------------------------

#trojkat = Trojkat(point1, point2, point3)
#trojkat.rysuj()

#
# linia1 = Linia(point1, point3)
# linia2 = Linia(point2, point4)
#
# punkt_przeciecia = Linia.punkt_przeciecia_postac_ogolna(linia1, linia2)
# # punkt_przeciecia = Linia.punkt_przeciecia_dwoch_linii(linia1, linia2)
# if punkt_przeciecia:
#         print(f'Punkt przecięcia: {punkt_przeciecia}')
#         punkt_przeciecia.rysuj(color='green')
#
#
# odleglosc = linia1.odleglosc_od_punktu_do_prostej(punkt5)
# print(f'Odległość między punktem {punkt5} a linią wynosi {odleglosc}')
#
# linia1.rysuj()
# linia2.rysuj()
# punkt5.rysuj(marker='*', color='purple', label='Odleglosc od punktu', markersize=10)
#
# plt.axis()
# plt.legend()
# plt.show()
#------------------------------------------



#--------------------------------------------------------------------------------------

# line = Linia(point1, point2)
# lines = [line]

# print(f"Równanie prostej: ", line.wypisz_rownanie())
# points = [point1, point2]
# wizualizacja(points, lines)
# os.system("PAUSE")

# punkt3 =Punkt(3, 6)
# print(f"Przynależność punktu ({punkt3.x}, {punkt3.y}) do prostej:", line.przynaleznosc_prosta(punkt3))
# points = [point1, point2, punkt3]
# wizualizacja(points, lines)
# os.system("PAUSE")

# punkt3 =Punkt(-2, 8)
# print(f"Przynależność punktu ({punkt3.x}, {punkt3.y}) do odcinka:", line.przynaleznosc_odcinek(punkt3))
# points = [point1, point2, punkt3]
# wizualizacja(points, lines)
# os.system("PAUSE")

# punkt3 =Punkt(6, 6)
# print(f"Położenie punktu ({punkt3.x}, {punkt3.y}) względem prostej:", line.przynaleznosc_punktu_prosta(punkt3))
# points = [point1, point2, punkt3]
# wizualizacja(points, lines)
# os.system("PAUSE")

# punkt3 =Punkt(2, 2)
# points = [point1, point2]
# wizualizacja(points, lines)
# line.translacja(punkt3)
# os.system("PAUSE")
# print(f"Translacja linii o wektor ({punkt3.x}, {punkt3.y}):", line.point1, line.point2)
# points = [point1, point2]
# wizualizacja(points, lines)
# os.system("PAUSE")

# punkt3 = Punkt(3,4)
# reflected_point = line.odbicie_punktu_wzgledem_prostej(punkt3)
# print(f"Odbicie punktu ({punkt3.x}, {punkt3.y}) względem linii:", reflected_point)
# points = [point1, point2, punkt3, reflected_point ]
# wizualizacja(points, lines)
# os.system("PAUSE")
#-------------------------------------------------------------------------------------