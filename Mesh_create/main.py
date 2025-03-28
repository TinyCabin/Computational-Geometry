import cv2
import numpy as np
import matplotlib.pyplot as plt


class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def find_contour(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 200)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_points = [Punkt(point[0][0], point[0][1]) for point in contours[0]]
    return contour_points

def konturowanie(points, epsilon):
    if len(points) < 3:
        return points
    new_points = [points[0]]  # 1st point
    current_distance = 0
    for i in range(1, len(points) - 1):
        dx = points[i].x - points[i - 1].x
        dy = points[i].y - points[i - 1].y
        distance = np.sqrt(dx ** 2 + dy ** 2)
        if current_distance + distance >= epsilon:
            new_points.append(points[i])
            current_distance = 0
        else:
            current_distance += distance
    new_points.append(points[-1])
    return new_points

def plot_triangles(triangles, text=None):
    plt.figure(figsize=(8, 8))
    plt.axis('equal')
    plt.grid(True)
    for triangle in triangles:
        x = [point.x for point in triangle]
        y = [point.y for point in triangle]
        plt.scatter(x, y, s=20, c='r', marker='o', alpha=1)
        for i in range(len(triangle)):
            p1 = triangle[i]
            p2 = triangle[(i + 1) % len(triangle)]
            plt.plot([p1.x, p2.x], [p1.y, p2.y], 'b-')
    plt.xlabel('Oś x')
    plt.ylabel('Oś y')
    plt.gca().invert_yaxis()
    if text:
        plt.title(text)
    plt.show()

def find_center(points):
    x_sum = sum(point.x for point in points)
    y_sum = sum(point.y for point in points)
    n = len(points)
    return Punkt(x_sum / n, y_sum / n)

def triangulate(points):
    center = find_center(points)
    triangles = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        triangles.append((p1, p2, center))
    return triangles

def create_equidistant_grid(contour_points, distance):
    contour_array = np.array([[[point.x, point.y]] for point in contour_points], dtype=np.int32)
    x_min, y_min, w, h = cv2.boundingRect(contour_array)
    triangle_height = (np.sqrt(3) / 2) * distance
    points = []
    y = y_min
    row = 0
    while y < y_min + h:
        x_offset = (triangle_height if row % 2 == 1 else 0)
        x = x_min + x_offset
        while x < x_min + w:
            if cv2.pointPolygonTest(contour_array, (x, y), False) >= 0:
                points.append(Punkt(x, y))
            x += distance
        y += triangle_height
        row += 1

    return points


# Wczytanie obrazu
image = cv2.imread('pacman_duch.png')
#image = cv2.imread('trudny_wariant.png')

otoczka = find_contour(image)
siatka = konturowanie(otoczka, 100)
triangles = triangulate(siatka)
plot_triangles(triangles)

internal_points = create_equidistant_grid(siatka, 75)
all_points = siatka + internal_points
triangles = triangulate(all_points)
plot_triangles(triangles)
