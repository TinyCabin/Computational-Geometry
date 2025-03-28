import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import numpy as np
import time

def wczytaj_pkt(plikTekstowy):
    with open(plikTekstowy, 'r') as dane:
        iloscPunktow = int(dane.readline().strip())
        punkty_x = []
        punkty_y = []
        for i in range(iloscPunktow):
            line = dane.readline().strip()
            if line:
                punkt = line.split()
                if len(punkt) == 2:
                    punkty_x.append(int(punkt[0]))
                    punkty_y.append(int(punkt[1]))
                else:
                    print(f"Skipping line: {line}")
    return punkty_x, punkty_y


def DelaunayTri(lista):
    x, y = lista
    points = np.array(list(zip(x, y)))

    start_time = time.time()
    tri = Delaunay(points)
    end_time = time.time()
    execution_time = end_time - start_time

    plt.triplot(points[:, 0], points[:, 1], tri.simplices, c='r')
    plt.plot(points[:, 0], points[:, 1], 'o', c="blue")
    plt.show()

    #Analiza
    num_simplices = len(tri.simplices)
    shape_quality = []
    for simplex in tri.simplices:
        p1, p2, p3 = points[simplex]
        edges = [np.linalg.norm(p2 - p1), np.linalg.norm(p3 - p1), np.linalg.norm(p3 - p2)]
        shape_quality.append(min(edges) / max(edges))

    median_quality = np.median(shape_quality)
    mode_quality = np.argmax(np.bincount((np.array(shape_quality) * 100).astype(int))) / 100

    print("Informacje o sympleksach (Delaunay):")
    print("Liczba elementów:", num_simplices)
    print("Mediana jakości kształtów:", median_quality)
    print("Moda jakości kształtów:", mode_quality)
    print("Czas wykonania triangulacji:", execution_time, "s")

    plt.hist(shape_quality, bins=20)
    plt.xlabel("Jakość kształtu")
    plt.ylabel("Liczba sympleksów")
    plt.title("Histogram jakości kształtów (Delaunay)")
    plt.show()


def EarClippingTri(lista):
    x, y = lista
    points = np.array(list(zip(x, y)))

    vertices = list(range(len(points)))

    triangles = []
    start_time = time.time()

    #więcej niż 3 wierzchołki
    while len(vertices) > 3:
        for i in range(len(vertices)):
            #czy jest uchem
            if ucho(points, vertices, i):
                triangles.append([vertices[i], vertices[(i + 1) % len(vertices)], vertices[(i - 1) % len(vertices)]])
                vertices.pop(i)
                break

    triangles.append([vertices[0], vertices[1], vertices[2]])
    end_time = time.time()
    execution_time = end_time - start_time

    for triangle in triangles:
        plt.fill(points[triangle, 0], points[triangle, 1], 'r', alpha=0.5)
    plt.plot(points[:, 0], points[:, 1], 'bo')
    plt.show()

    #analiza
    num_simplices = len(triangles)
    shape_quality = []
    for triangle in triangles:
        p1, p2, p3 = points[triangle]
        edges = [np.linalg.norm(p2 - p1), np.linalg.norm(p3 - p1), np.linalg.norm(p3 - p2)]
        shape_quality.append(min(edges) / max(edges))
    median_quality = np.median(shape_quality)
    mode_quality = np.argmax(np.bincount((np.array(shape_quality) * 100).astype(int))) / 100

    print("Informacje o sympleksach (Ear Clipping):")
    print("Liczba elementów:", num_simplices)
    print("Mediana jakości kształtów:", median_quality)
    print("Moda jakości kształtów:", mode_quality)
    print("Czas wykonania triangulacji:", execution_time, "s")

    plt.hist(shape_quality, bins=20)
    plt.xlabel("Jakość kształtu")
    plt.ylabel("Liczba sympleksów")
    plt.title("Histogram jakości kształtów (Ear Clipping)")
    plt.show()


def ucho(points, vertices, i):
    #inny punkt nie leży wewnątrz trójkąta
    p1 = points[vertices[i]]
    p2 = points[vertices[(i + 1) % len(vertices)]]
    p3 = points[vertices[(i - 1) % len(vertices)]]

    for j in range(len(vertices)):
        if j != i and j != (i + 1) % len(vertices) and j != (i - 1) % len(vertices):
            if czy_w_trojkacie(points[vertices[j]], p1, p2, p3):
                return False

    return True


def czy_w_trojkacie(p, p1, p2, p3):
    area = 0.5 * (-p2[1] * p3[0] + p1[1] * (-p2[0] + p3[0]) + p1[0] * (p2[1] - p3[1]) + p2[0] * p3[1])
    s = 1 / (2 * area) * (p1[1] * p3[0] - p1[0] * p3[1] + (p3[1] - p1[1]) * p[0] + (p1[0] - p3[0]) * p[1])
    t = 1 / (2 * area) * (p1[0] * p2[1] - p1[1] * p2[0] + (p1[1] - p2[1]) * p[0] + (p2[0] - p1[0]) * p[1])

    return s > 0 and t > 0 and (1 - s - t) > 0


lista = wczytaj_pkt("ksztalt_2.txt")
DelaunayTri(lista)
print('  ')
EarClippingTri(lista)