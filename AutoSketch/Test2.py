import numpy as np
from PIL import Image
import cv2  # OpenCV pour conversion RGB -> Lab

# Liste des couleurs disponibles
available_colors = np.array([
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

# Convertir les couleurs disponibles en Lab
available_colors_lab = cv2.cvtColor(available_colors.reshape(1, -1, 3), cv2.COLOR_RGB2LAB).reshape(-1, 3)

# Charger l'image
input_image_path = 'image.jpg'  # Remplacez par votre image
output_image_path = 'output_image.jpg'
image = Image.open(input_image_path).convert('RGB')
pixels = np.array(image, dtype=np.uint8)

# Convertir les pixels en Lab
pixels_lab = cv2.cvtColor(pixels, cv2.COLOR_RGB2LAB)

# Reshape pour comparer en une seule opération vectorisée
pixels_flat_lab = pixels_lab.reshape(-1, 3)

# Trouver la couleur la plus proche en Lab
def find_closest_color_lab(pixel_lab):
    distances = np.linalg.norm(available_colors_lab - pixel_lab, axis=1)
    return available_colors[np.argmin(distances)]  # On renvoie la couleur originale en RGB

# Appliquer la correspondance
new_pixels_flat = np.apply_along_axis(find_closest_color_lab, 1, pixels_flat_lab)
new_pixels = new_pixels_flat.reshape(pixels.shape)

# Créer et sauvegarder l'image modifiée
output_image = Image.fromarray(new_pixels, mode='RGB')
output_image.save(output_image_path)

print(f"Image modifiée sauvegardée sous : {output_image_path}")
