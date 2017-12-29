#!/usr/bin/env python3
from abc import ABC
from math import sqrt, sin, cos, fabs, pi

from svg import SVG, Point


class Fractal(ABC):
    def __init__(self, depth: int):
        self.depth = depth
        self.svg = SVG(self.width, self.height)

    @property
    def width(self):
        return 100

    @property
    def height(self):
        return 100

    def __str__(self):
        return self.svg.__str__()


class SierpinskiTriangle(Fractal):
    def __init__(self, depth: int):
        super().__init__(depth)
        self.colors = ["orange", "red", "yellow", "pink"]
        base_triangle = [Point(0, 87), Point(100, 87), Point(50, 0)]
        self.svg.polygon(*base_triangle, fill="blue")
        self.triangle(*base_triangle, depth=0)

    @property
    def height(self):
        return 87

    def triangle(self, p1: Point, p2: Point, p3: Point, depth: int):
        if depth == self.depth:
            return

        sub1 = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
        sub2 = Point((p2.x + p3.x) / 2, (p2.y + p3.y) / 2)
        sub3 = Point((p3.x + p1.x) / 2, (p3.y + p1.y) / 2)

        self.svg.polygon(sub1, sub2, sub3, fill=self.colors[depth])

        self.triangle(p1, sub1, sub3, depth + 1)
        self.triangle(p2, sub1, sub2, depth + 1)
        self.triangle(p3, sub2, sub3, depth + 1)


class SierpinskiCarpet(Fractal):
    def __init__(self, depth: int):
        super().__init__(depth)
        self.colors = ["#9c546c", "#ae5e79", "#DA7698", "#E3A7C0"]
        self.svg.square(Point(0, 0), Point(100, 100), '#ffe8ff')
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


class BoxFractal(Fractal):
    def __init__(self, depth: int, color_shift=0):
        super().__init__(depth)
        self.svg.square(Point(0, 0), Point(100, 100), 'white')
        self.color_shift = color_shift
        self.square(Point(0, 0), Point(100, 100), 0)

    def square(self, top_left: Point, bottom_right: Point, depth):
        if depth == self.depth:
            color = "#%06x" % int(
                0xFFFFFF
                / (top_left.x + top_left.y + .001 + self.color_shift)
                * (top_left.y + self.color_shift)
            )
            self.svg.square(top_left, bottom_right, fill=color)
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
                if (i + j) % 2 == 0:
                    self.square(sub_top_left, sub_bottom_right, depth + 1)


class CrossFractal(Fractal):
    def __init__(self, depth: int, color_shift=1):
        super().__init__(depth)
        self.color_shift = color_shift
        self.svg.square(Point(0, 0), Point(self.width, self.height), '#212121')
        self.cross(Point(0, 0), Point(self.width, self.height), 0)

    def cross(self, top_left: Point, bottom_right: Point, depth):
        if depth == self.depth:
            size = bottom_right.x - top_left.x
            center = Point(top_left.x + size / 2, top_left.y + size / 2)
            distance = sqrt(
                (self.width / 2 - center.x) ** 2
                + (self.height / 2 - center.y) ** 2
            )
            color = "#%06x" % int(0xFFFFFF * fabs(cos(distance * self.color_shift)))
            self.svg.square(top_left, bottom_right, fill=color)
            return

        sub_width = (bottom_right.x - top_left.x) / 3
        sub_height = (bottom_right.y - top_left.y) / 3
        for i in range(0, 3):
            for j in range(0, 3):
                if ((i + j) % 2 == 1) or (i == 1 and j == 1):
                    sub_top_left = Point(top_left.x + sub_width * j, top_left.y + sub_height * i)
                    sub_bottom_right = Point(
                        sub_top_left.x + sub_width,
                        sub_top_left.y + sub_height
                    )

                    self.cross(sub_top_left, sub_bottom_right, depth + 1)


if __name__ == '__main__':
    fractals = {
        "triangle": SierpinskiTriangle(4),
        "carpet": SierpinskiCarpet(4),
        "box": BoxFractal(4, 1),
        "cross": CrossFractal(4, 16),
    }

    for name, fractal in fractals.items():
        file = open(f"{name}.svg", 'w')
        with file:
            file.write(fractal.__str__())
