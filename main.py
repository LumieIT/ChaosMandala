import random
import math
from PIL import Image, ImageDraw, ImageColor

def hsv_to_rgb(h, s, v):
    return ImageColor.getrgb(f"hsv({int(h*360)},{int(s*100)}%,{int(v*100)}%)")

def create_mandala(size):
    image = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(image)
    center = size // 2
    max_radius = min(size, size) // 2

    # Palette di colori più armoniosa
    base_hue = random.random()
    colors = [
        hsv_to_rgb((base_hue + i/7) % 1, random.uniform(0.6, 1), random.uniform(0.6, 1))
        for i in range(random.randint(4, 8))
    ]

    def draw_petal(x, y, size, angle, color, fill=True):
        points = []
        for i in range(60):
            a = math.radians(i * 6 - 90 + angle + random.uniform(-15, 15))
            r = size * math.sin(a * 3 + random.uniform(-0.3, 0.3))
            px = x + r * math.cos(a)
            py = y + r * math.sin(a)
            points.append((px, py))
        if fill:
            draw.polygon(points, fill=color, outline=color)
        else:
            draw.line(points + [points[0]], fill=color, width=max(1, int(size/50)))

    def draw_star(x, y, size, points, color, fill=True):
        angle = random.uniform(0, 360)
        step = 360 / points
        star_points = []
        for i in range(points * 2):
            r = size if i % 2 == 0 else size * random.uniform(0.4, 0.7)
            theta = math.radians(i * step / 2 + angle)
            px = x + r * math.cos(theta)
            py = y + r * math.sin(theta)
            star_points.append((px, py))
        if fill:
            draw.polygon(star_points, fill=color, outline=color)
        else:
            draw.line(star_points + [star_points[0]], fill=color, width=max(1, int(size/50)))

    def draw_spiral(x, y, size, color):
        points = []
        turns = random.randint(2, 5)
        for i in range(360 * turns):
            angle = math.radians(i)
            r = size * (i / (360 * turns))
            px = x + r * math.cos(angle + random.uniform(-0.1, 0.1))
            py = y + r * math.sin(angle + random.uniform(-0.1, 0.1))
            points.append((px, py))
        draw.line(points, fill=color, width=max(1, int(size/100)))

    def draw_polygon(x, y, size, sides, color, fill=True):
        angle = random.uniform(0, 360)
        step = 360 / sides
        poly_points = []
        for i in range(sides):
            theta = math.radians(i * step + angle)
            px = x + size * math.cos(theta)
            py = y + size * math.sin(theta)
            poly_points.append((px, py))
        if fill:
            draw.polygon(poly_points, fill=color, outline=color)
        else:
            draw.line(poly_points + [poly_points[0]], fill=color, width=max(1, int(size/50)))

    def draw_layer(radius, shape_type, shape_params, color):
        shape_count = random.randint(6, shape_params['max_shapes'])
        for i in range(shape_count):
            angle = (360 / shape_count) * i + random.uniform(-30, 30)
            x = center + radius * math.cos(math.radians(angle))
            y = center + radius * math.sin(math.radians(angle))
            if shape_type == 'petal':
                draw_petal(x, y, radius * random.uniform(0.5, 0.9), angle, color, fill=random.choice([True, False]))
            elif shape_type == 'star':
                draw_star(x, y, radius * random.uniform(0.3, 0.6), random.randint(5, 8), color, fill=random.choice([True, False]))
            elif shape_type == 'spiral':
                draw_spiral(x, y, radius * random.uniform(0.4, 0.8), color)
            elif shape_type == 'polygon':
                draw_polygon(x, y, radius * random.uniform(0.4, 0.8), random.randint(3, 6), color, fill=random.choice([True, False]))

    # Strati centrali con forme miste
    central_layers = random.randint(5, 10)
    shape_types = ['petal', 'star', 'spiral', 'polygon']
    for i in range(central_layers):
        radius = max_radius * (i + 1) / (central_layers * 1.8)
        shape_type = random.choice(shape_types)
        shape_params = {
            'max_shapes': 12 if shape_type == 'spiral' else 8
        }
        petal_count = random.randint(6, 12) + i * 2
        draw_layer(radius, shape_type, shape_params, random.choice(colors))

    # Strato esterno con forma mista
    outer_radius = max_radius * 0.9
    outer_shape_type = random.choice(shape_types)
    outer_shape_params = {
        'max_shapes': 20 if outer_shape_type == 'spiral' else 16
    }
    draw_layer(outer_radius, outer_shape_type, outer_shape_params, random.choice(colors))

    # Dettagli interni con forme miste
    for i in range(random.randint(3, 6)):
        radius = max_radius * (0.2 + i * 0.1 + random.uniform(-0.05, 0.05))
        shape_type = random.choice(shape_types)
        shape_params = {
            'max_shapes': 10 if shape_type == 'spiral' else 14
        }
        draw_layer(radius, shape_type, shape_params, random.choice(colors))

    # Cerchio centrale con vari dettagli
    central_circle_radius = max_radius * random.uniform(0.12, 0.18)
    draw.ellipse([center-central_circle_radius, center-central_circle_radius,
                  center+central_circle_radius, center+central_circle_radius],
                 fill=random.choice(colors), outline='black')

    inner_detail_count = random.randint(6, 10)
    for i in range(inner_detail_count):
        angle = (360 / inner_detail_count) * i + random.uniform(-10, 10)
        x = center + central_circle_radius * 0.7 * math.cos(math.radians(angle))
        y = center + central_circle_radius * 0.7 * math.sin(math.radians(angle))
        shape_choice = random.choice(['ellipse', 'polygon'])
        size = central_circle_radius * random.uniform(0.25, 0.35)
        if shape_choice == 'ellipse':
            draw.ellipse([x-size, y-size, x+size, y+size], fill='white', outline='black')
        elif shape_choice == 'polygon':
            draw_polygon(x, y, size, random.randint(3, 6), 'black', fill=False)

    # Linee decorative casuali
    for i in range(random.randint(20, 40)):
        angle = random.uniform(0, 360)
        start_radius = random.uniform(0.3, 0.6) * max_radius
        end_radius = random.uniform(0.7, 0.95) * max_radius
        start_x = center + start_radius * math.cos(math.radians(angle))
        start_y = center + start_radius * math.sin(math.radians(angle))
        end_x = center + end_radius * math.cos(math.radians(angle))
        end_y = center + end_radius * math.sin(math.radians(angle))
        line_width = random.randint(1, 3)
        draw.line([(start_x, start_y), (end_x, end_y)], fill='black', width=line_width)

    return image

def main():
    size = 3000
    while True:
        mandala = create_mandala(size)
        mandala.show()  # Mostra l'immagine all'utente
        scelta = input("Vuoi salvare questa creazione? (s per salvare, c per crearne un'altra): ").strip().lower()
        if scelta == 's':
            filename = f'mandala_{random.randint(1000,9999)}.png'
            mandala.save(filename)
            print(f"Mandala salvato come '{filename}' con dimensioni {size}x{size}")
            break
        elif scelta == 'c':
            print("Generando una nuova creazione...")
        else:
            print("Input non valido. Per favore, inserisci 's' per salvare o 'c' per creare un'altra immagine.")

if __name__ == "__main__":
    main()
