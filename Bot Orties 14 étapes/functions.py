import pyautogui
import time
import pyautogui
from pathlib import Path

def chercher_et_cliquer(image_path, confidence=0.8):
    """
    Cherche une image sur l'écran et clique au centre si elle est trouvée.
    
    Args:
        image_path (str ou Path): Le chemin vers l'image à chercher.
        confidence (float): Niveau de confiance pour la détection (valeur entre 0 et 1).
    """
    image_path = Path(image_path)
    if not image_path.is_file():
        print(f"Image non trouvée : {image_path}")
        return

    print(f"Recherche de l'image : {image_path.name}")
    try:
        location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
        if location:
            center = pyautogui.center(location)
            print(f"Image trouvée à {center}. Clique en cours...")
            pyautogui.click(center)
        else:
            print(f"Image non détectée sur l'écran pour : {image_path.name}")
    except Exception as e:
        print(f"Erreur lors de la recherche de l'image {image_path.name} : {e}")

def cliquer_centre():
    """Clique au centre de l'écran."""
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    pyautogui.click(center_x, center_y)

def cliquer_droite_centre():
    """Clique 40 pixels à droite du centre de l'écran."""
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    pyautogui.click(center_x + 40, center_y)

def cliquer_gauche_centre():
    """Clique 40 pixels à gauche du centre de l'écran."""
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    pyautogui.click(center_x - 40, center_y)

def cliquer_bas_centre():
    """Clique 40 pixels en dessous du centre de l'écran."""
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    pyautogui.click(center_x, center_y + 40)

def cliquer_haut_centre():
    """Clique 40 pixels au-dessus du centre de l'écran."""
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    pyautogui.click(center_x, center_y - 40)

