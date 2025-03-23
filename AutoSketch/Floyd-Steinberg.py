import numpy as np
from scipy.spatial import KDTree
from PIL import Image

# Palette de couleurs donnée
PALETTE = np.array([
    (146, 161, 185), (57, 31, 33), (90, 197, 79), (255, 200, 37), (39, 39, 39),
    (199, 207, 221), (180, 180, 180), (249, 230, 207), (0, 105, 170), (148, 253, 255),
    (28, 18, 28), (253, 210, 237), (202, 82, 201), (61, 61, 61), (26, 25, 50), (87, 28, 39),
    (93, 44, 40), (48, 3, 217), (0, 152, 220), (12, 46, 68), (42, 47, 78), (27, 27, 27),
    (19, 19, 19), (219, 63, 253), (3, 25, 63), (234, 50, 60), (237, 118, 20), (255, 255, 255),
    (255, 80, 0), (237, 171, 80), (12, 2, 147), (230, 156, 105), (147, 56, 143), (245, 85, 93),
    (0, 0, 0), (93, 93, 93), (14, 7, 27), (12, 241, 255), (191, 111, 74), (59, 20, 67),
    (98, 36, 97), (255, 235, 87), (101, 115, 146), (66, 76, 110), (19, 76, 76), (122, 9, 250),
    (133, 133, 133), (153, 230, 95), (0, 205, 249), (224, 116, 56), (142, 37, 29), (246, 129, 135),
    (196, 36, 48), (246, 202, 159), (198, 69, 36), (51, 152, 75), (137, 30, 43), (255, 162, 20),
    (211, 252, 126), (0, 57, 109), (243, 137, 245), (30, 111, 80), (200, 80, 134), (138, 72, 54)
], dtype=np.uint8)

# Création d'un KDTree pour accélérer la recherche des couleurs les plus proches
palette_tree = KDTree(PALETTE)

def closest_palette_color(color):
    """Retourne la couleur la plus proche de la palette."""
    _, index = palette_tree.query(color)
    return PALETTE[index]

def floyd_steinberg_dither(image):
    """Applique l'algorithme de Floyd-Steinberg pour diffuser les erreurs de quantification."""
    img_array = np.array(image, dtype=np.float32)  # Convertir en float pour la propagation d'erreur
    height, width, _ = img_array.shape

    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x]
            new_pixel = closest_palette_color(old_pixel)
            img_array[y, x] = new_pixel

            # Calcul de l'erreur
            error = old_pixel - new_pixel

            # Propagation de l'erreur aux pixels voisins
            if x + 1 < width:
                img_array[y, x + 1] += error * (7 / 16)
            if x - 1 >= 0 and y + 1 < height:
                img_array[y + 1, x - 1] += error * (3 / 16)
            if y + 1 < height:
                img_array[y + 1, x] += error * (5 / 16)
            if x + 1 < width and y + 1 < height:
                img_array[y + 1, x + 1] += error * (1 / 16)

    # Assurer que les valeurs restent dans la plage [0, 255]
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)

    return Image.fromarray(img_array)

# Charger l'image
input_image_path = r"AutoSketch\dio-brando-7.jpg"
output_image_path = "AutoSketch\output_dithered7.png"

image = Image.open(input_image_path).convert("RGB")
dithered_image = floyd_steinberg_dither(image)

dithered_image.save(output_image_path)
print(f"Image convertie avec dithering et palette limitée : {output_image_path}")
