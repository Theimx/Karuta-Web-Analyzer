from pynput.mouse import Controller, Button
from PIL import Image
import time

# Variables globales
coords = []
draw_start = None
mouse_controller = Controller()

# Palette de couleurs (RGB) et positions
colors = [(146, 161, 185), (57, 31, 33), (90, 197, 79), (255, 200, 37), (39, 39, 39), (199, 207, 221), (180, 180, 180), (249, 230, 207), (0, 105, 170), (148, 253, 255), (28, 18, 28), (253, 210, 237), (202, 82, 201), (61, 61, 61), (26, 25, 50), (87, 28, 39), (93, 44, 40), (48, 3, 217), (0, 152, 220), (12, 46, 68), (42, 47, 78), (27, 27, 27), (19, 19, 19), (219, 63, 253), (3, 25, 63), (234, 50, 60), (237, 118, 20), (255, 255, 255), (255, 80, 0), (237, 171, 80), (12, 2, 147), (230, 156, 105), (147, 56, 143), (245, 85, 93), (0, 0, 0), (93, 93, 93), (14, 7, 27), (12, 241, 255), (191, 111, 74), (59, 20, 67), (98, 36, 97), (255, 235, 87), (101, 115, 146), (66, 76, 110), (19, 76, 76), (122, 9, 250), (133, 133, 133), (153, 230, 95), (0, 205, 249), (224, 116, 56), (142, 37, 29), (246, 129, 135), (196, 36, 48), (246, 202, 159), (198, 69, 36), (51, 152, 75), (137, 30, 43), (255, 162, 20), (211, 252, 126), (0, 57, 109), (243, 137, 245), (30, 111, 80), (200, 80, 134), (138, 72, 54)]

def on_click(x, y, button, pressed):
    if pressed:
        coords.append((x, y))
        print(f"Point enregistré: {x}, {y}")
        
        if len(coords) == 2:
            print("Cliquez sur l'endroit où dessiner l'image.")
            with mouse.Listener(on_click=on_draw_point) as listener:
                listener.join()

def on_draw_point(x, y, button, pressed):
    global draw_start
    if pressed:
        draw_start = (x, y)
        print(f"Point de dessin enregistré: {x}, {y}")
        listener.stop()
        process_image()

def create_grid():
    (x1, y1), (x2, y2) = coords
    width, height = abs(x2 - x1), abs(y2 - y1)
    cell_width, cell_height = width // 16, height // 4
    
    grid = {}
    for row in range(4):
        for col in range(16):
            cx = x1 + col * cell_width + cell_width // 2
            cy = y1 + row * cell_height + cell_height // 2
            grid[colors[row * 16 + col]] = (cx, cy)
    
    return grid

def closest_color(pixel):
    return min(colors, key=lambda color: sum((p - c) ** 2 for p, c in zip(pixel, color)))

def process_image():
    image_path = input("doppio.png")
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    grid = create_grid()
    pixels_by_color = {}
    
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            color = closest_color(pixel)
            if color not in pixels_by_color:
                pixels_by_color[color] = []
            pixels_by_color[color].append((draw_start[0] + x, draw_start[1] + y))
    
    for color, positions in pixels_by_color.items():
        if color in grid:
            mouse_controller.position = grid[color]
            mouse_controller.click(Button.left)
            time.sleep(0.1)
            
            mouse_controller.position = positions[0]
            mouse_controller.press(Button.left)
            for pos in positions:
                mouse_controller.position = pos
                time.sleep(0.05)
            mouse_controller.release(Button.left)
            time.sleep(0.1)

print("Cliquez en haut à gauche puis en bas à droite de la palette.")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
