import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

TARGET_WIDTH = 520
TARGET_HEIGHT = 720

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def charger_image():
    filepath = filedialog.askopenfilename(
        title="Choisir une image",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    
    if not filepath:
        return

    try:
        img = Image.open(filepath).convert("RGBA")
        largeur, hauteur = img.size

        if largeur < TARGET_WIDTH and hauteur < TARGET_HEIGHT:
            messagebox.showwarning(
                "Image trop petite", 
                f"L'image est plus petite que {TARGET_WIDTH}x{TARGET_HEIGHT}.\n"
                f"Taille actuelle : {largeur}x{hauteur}"
            )

        # Redimensionnement proportionnel
        ratio_w = TARGET_WIDTH / largeur
        ratio_h = TARGET_HEIGHT / hauteur
        ratio = min(ratio_w, ratio_h)

        new_width = int(largeur * ratio)
        new_height = int(hauteur * ratio)
        img_redim = img.resize((new_width, new_height), Image.LANCZOS)

        # Création de l'image finale avec transparence
        image_finale = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
        x_offset = (TARGET_WIDTH - new_width) // 2
        y_offset = (TARGET_HEIGHT - new_height) // 2
        image_finale.paste(img_redim, (x_offset, y_offset), img_redim)

        # Prépare le nom de fichier basé sur l’original
        nom_fichier = os.path.basename(filepath)
        nom_sans_ext = os.path.splitext(nom_fichier)[0]
        nom_output = nom_sans_ext + "_ready.png"

        # Enregistre sur le bureau
        chemin_bureau = get_desktop_path()
        output_path = os.path.join(chemin_bureau, nom_output)
        image_finale.save(output_path)

        messagebox.showinfo(
            "Succès", 
            f"L'image a été sauvegardée sur le bureau :\n{output_path}"
        )
        afficher_image(image_finale)

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du traitement de l'image : {e}")

def afficher_image(img):
    img_tk = ImageTk.PhotoImage(img)
    canvas.config(width=img.width, height=img.height)
    canvas.delete("all")
    canvas.image = img_tk
    canvas.create_image(0, 0, anchor="nw", image=img_tk)

# Interface graphique
root = tk.Tk()
root.title("Redimensionneur 520x720 (avec fond transparent)")

btn_charger = tk.Button(root, text="Charger une image", command=charger_image)
btn_charger.pack(pady=10)

canvas = tk.Canvas(root, bg="lightgrey")
canvas.pack(padx=10, pady=10)

root.mainloop()
