from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class SVG:
    def __init__(self, width, height):
        self.content = ""
        self.header = f"""<svg version="1.1"
 width="{width}" height="{height}"
 xmlns="http://www.w3.org/2000/svg">\n"""
        self.footer = "</svg>"

    def write(self, text):
        self.content += f"\t{text}\n"

    def line(self, p1: Point, p2: Point):
        self.write(f'<line x1="{p1.x}" y1="{p1.y}" x2="{p2.x}" y2="{p2.y}"'
                   f' style="stroke:rgb(0,0,0);stroke-width:2" />')

    def polygon(self, *points: Point, fill: str = "black"):
        points_str = " ".join([f'{p.x},{p.y}' for p in points])

        self.write(f'<polygon points="{points_str}"'
                   f' style="fill:{fill};stroke:black;stroke-width:0" />')

    def square(self, top_left: Point, bottom_right: Point, fill: str = "black"):
        self.polygon(
            top_left,
            Point(top_left.x + (bottom_right.x - top_left.x), top_left.y),
            Point(top_left.x + (bottom_right.x - top_left.x),
                  top_left.y + (bottom_right.y - top_left.y)),
            Point(top_left.x, top_left.y + (bottom_right.y - top_left.y)),
            fill=fill
        )

    def circle(self, center: Point, radius: float, fill: str):
        self.write(f'<circle cx="{center.x}" cy="{center.y}" r="{radius}" fill="{fill}" />"')

    def __str__(self):
        return self.header + self.content + self.footer
