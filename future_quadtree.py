import pygame
import random
import math
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RADIUS = 50  # Radio del círculo de búsqueda


def line_eq(x, m, b):
    return m * x + b


def distance_point_to_line(x, y, m, b):
    """Calcula la distancia desde un punto (x, y) hasta una línea (m, b)."""
    return abs(m * x - y + b) / math.sqrt(m ** 2 + 1)


class QuadtreeNode:
    def __init__(self, x_min, x_max, y_min, y_max, bucket_capacity=2):
        self.bounds = (x_min, x_max, y_min, y_max)
        self.lines = []  # Lista de líneas [(m, b)]
        self.bucket_capacity = bucket_capacity
        self.children = []

    def insert(self, line):
        if self.children:
            self.insert_to_children(line)
            return

        if line not in self.lines:
            self.lines.append(line)

        if len(self.lines) > self.bucket_capacity:
            self.subdivide()
            for l in self.lines:
                self.insert_to_children(l)
            self.lines = []

    def insert_to_children(self, line):
        for child in self.children:
            if child.intersects(line):
                child.insert(line)

    def intersects(self, line):
        x_min, x_max, y_min, y_max = self.bounds
        m, b = line
        y_left = line_eq(x_min, m, b)
        y_right = line_eq(x_max, m, b)
        return not (y_left > y_max and y_right > y_max or y_left < y_min and y_right < y_min)

    def subdivide(self):
        x_min, x_max, y_min, y_max = self.bounds
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2

        self.children = [
            QuadtreeNode(x_min, x_mid, y_mid, y_max, self.bucket_capacity),
            QuadtreeNode(x_mid, x_max, y_mid, y_max, self.bucket_capacity),
            QuadtreeNode(x_min, x_mid, y_min, y_mid, self.bucket_capacity),
            QuadtreeNode(x_mid, x_max, y_min, y_mid, self.bucket_capacity)
        ]

    def query_range(self, cx, cy, radius, found_lines):
        if not self.circle_intersects_rect(cx, cy, radius):
            return

        for m, b in self.lines:
            if distance_point_to_line(cx, cy, m, b) <= radius:
                found_lines.append((m, b))

        for child in self.children:
            child.query_range(cx, cy, radius, found_lines)

    def remove_lines_in_range(self, cx, cy, radius):
        if self.children:
            for child in self.children:
                child.remove_lines_in_range(cx, cy, radius)
            self.collapse_if_needed()
        else:
            self.lines = [line for line in self.lines if distance_point_to_line(cx, cy, *line) > radius]

    def collapse_if_needed(self):
        """Colapsa nodos hijos si están vacíos y no tienen líneas."""
        if self.children:
            combined_lines = []
            for child in self.children:
                combined_lines.extend(child.lines)
                if child.children:
                    return  # No colapsar si alguno de los hijos tiene subdivisiones

            if len(combined_lines) <= self.bucket_capacity:
                self.lines = combined_lines
                self.children = []

    def circle_intersects_rect(self, cx, cy, radius):
        x_min, x_max, y_min, y_max = self.bounds
        closest_x = max(x_min, min(cx, x_max))
        closest_y = max(y_min, min(cy, y_max))
        distance = math.sqrt((cx - closest_x) ** 2 + (cy - closest_y) ** 2)
        return distance <= radius

    def draw(self, screen):
        x_min, x_max, y_min, y_max = self.bounds
        pygame.draw.rect(screen, BLUE, pygame.Rect(x_min, y_min, x_max - x_min, y_max - y_min), 1)
        for m, b in self.lines:
            x1, x2 = x_min, x_max
            y1, y2 = line_eq(x1, m, b), line_eq(x2, m, b)
            pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 2)
        for child in self.children:
            child.draw(screen)


class Quadtree:
    def __init__(self, x_min, x_max, y_min, y_max, bucket_capacity=2):
        self.root = QuadtreeNode(x_min, x_max, y_min, y_max, bucket_capacity)

    def insert(self, m, b):
        self.root.insert((m, b))

    def query_range(self, cx, cy, radius):
        found_lines = []
        self.root.query_range(cx, cy, radius, found_lines)
        return found_lines

    def remove_lines_in_range(self, cx, cy, radius):
        self.root.remove_lines_in_range(cx, cy, radius)

    def draw(self, screen):
        self.root.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quadtree Line Indexing with Range Query")
    clock = pygame.time.Clock()

    quadtree = Quadtree(0, WIDTH, 0, HEIGHT, bucket_capacity=2)
    for _ in range(20):
        m = random.uniform(-2, 2)
        b = random.uniform(0, HEIGHT)
        quadtree.insert(m, b)

    searching = False
    removing = False
    running = True
    while running:
        screen.fill(WHITE)
        quadtree.draw(screen)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if searching or removing:
            color = BLACK if removing else GREEN
            pygame.draw.circle(screen, color, (mouse_x, mouse_y), RADIUS, 1)
            found_lines = quadtree.query_range(mouse_x, mouse_y, RADIUS)
            for m, b in found_lines:
                x1, x2 = 0, WIDTH
                y1, y2 = line_eq(x1, m, b), line_eq(x2, m, b)
                pygame.draw.line(screen, BLACK if removing else GREEN, (x1, y1), (x2, y2), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    searching = not searching
                elif event.key == pygame.K_e:
                    removing = not removing
                elif event.key == pygame.K_i:
                    try:
                        slope = float(input("Ingrese la pendiente (slope): "))
                        intercept = float(input("Ingrese el intercepto (intercept): "))
                        quadtree.insert(slope, intercept)
                    except ValueError:
                        print("Valores inválidos, intente nuevamente.")
            if event.type == pygame.MOUSEBUTTONDOWN and removing:
                quadtree.remove_lines_in_range(mouse_x, mouse_y, RADIUS)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
