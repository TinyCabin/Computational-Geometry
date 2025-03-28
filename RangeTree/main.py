class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node2D:
    def __init__(self, point):
        self.point = point
        self.Y = None
        self.left = None
        self.right = None

class Node1D:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None

class RangeTree2D:
    def __init__(self, points):
        self.root = self.build_range_tree2D(points)

    def build_range_tree2D(self, points, depth=0):
        if not points:
            return None

        points.sort(key=lambda point: point.x)

        median_idx = len(points) // 2

        node = Node2D(points[median_idx])

        node.Y = self.build_range_tree1D(points)

        node.left = self.build_range_tree2D(points[:median_idx], depth + 1)
        node.right = self.build_range_tree2D(points[median_idx + 1:], depth + 1)

        return node

    def build_range_tree1D(self, points, depth=0):
        if not points:
            return None

        points.sort(key=lambda point: point.y)

        median_idx = len(points) // 2

        node = Node1D(points[median_idx])

        node.left = self.build_range_tree1D(points[:median_idx], depth + 1)
        node.right = self.build_range_tree1D(points[median_idx + 1:], depth + 1)

        return node

def print2DUtil(node, space):
    if node is None:
        return

    space += 10

    print2DUtil(node.right, space)

    print()
    for i in range(10, space):
        print(" ", end="")
    print(f"{node.point.x}, {node.point.y}")

    print2DUtil(node.left, space)

def print2D(root):
    print2DUtil(root, 0)


# Przykładowe użycie
points = [Point(3, 6), Point(17, 15), Point(13, 15), Point(6, 12), Point(9, 1),
          Point(2, 7), Point(10, 19)]

range_tree = RangeTree2D(points)

print("Drzewo KD:")
print2D(range_tree.root)
print("Drzewo Y:")
print2D(range_tree.root.Y)