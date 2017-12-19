from svg import SVG, Point


class SierpinskiTriangle:
    def __init__(self, depth: int):
        self.depth = depth
        self.svg = SVG(100, 87)
        self.colors = ["orange", "red", "yellow", "pink"]
        base_triangle = [Point(0, 87), Point(100, 87), Point(50, 0)]
        self.svg.polygon(*base_triangle, fill="blue")
        self.triangle(*base_triangle, depth=0)

    def triangle(self, p1: Point, p2: Point, p3: Point, depth):
        if depth == self.depth:
            return

        sub1 = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
        sub2 = Point((p2.x + p3.x) / 2, (p2.y + p3.y) / 2)
        sub3 = Point((p3.x + p1.x) / 2, (p3.y + p1.y) / 2)

        self.svg.polygon(sub1, sub2, sub3, fill=self.colors[depth])

        self.triangle(p1, sub1, sub3, depth + 1)
        self.triangle(p2, sub1, sub2, depth + 1)
        self.triangle(p3, sub2, sub3, depth + 1)

    def __str__(self):
        return self.svg.__str__()


class SierpinskiCarpet:
    def __init__(self, depth: int):
        self.depth = depth
        self.svg = SVG(100, 100)
        self.colors = ["#F2D1B3", "#F2E77E", "#DA7698", "#E3A7C0"]
        self.svg.square(Point(0, 0), Point(100, 100), '#4C9385')
        self.square(Point(0, 0), Point(100, 100), 0)

    def square(self, top_left: Point, bottom_right: Point, depth):
        if depth == self.depth:
            return

        sub_width = (bottom_right.x - top_left.x) / 3
        sub_height = (bottom_right.y - top_left.y) / 3
        for i in range(0, 3):
            for j in range(0, 3):
                sub_top_left = Point(top_left.x + sub_width * j, top_left.y + sub_height * i)
                sub_bottom_right = Point(
                    sub_top_left.x + sub_width,
                    sub_top_left.y + sub_height
                )
                if i == 1 and j == 1:
                    self.svg.square(sub_top_left, sub_bottom_right, self.colors[depth])
                else:
                    self.square(sub_top_left, sub_bottom_right, depth + 1)

    def __str__(self):
        return self.svg.__str__()


if __name__ == '__main__':
    fractals = {
        "triangle": SierpinskiTriangle(4),
        "carpet": SierpinskiCarpet(4)
    }

    for name, fractal in fractals.items():
        file = open(f"{name}.svg", 'w')
        with file:
            file.write(fractal.__str__())
