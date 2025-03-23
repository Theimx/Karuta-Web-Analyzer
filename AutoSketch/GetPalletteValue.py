from PIL import Image

# Ouvrir l'image
image = Image.open('AutoSketch/palette.png')
image = image.convert('RGB')
largeur, hauteur = image.size
pixels = []

# Parcourir tous les pixels de l'image
for y in range(hauteur):
    for x in range(largeur):
        
        r, g, b = image.getpixel((x, y))
        pixels.append((r, g, b))

#supprimer les doublons 
pixels_uniques = list(set(pixels))
pixels_uniques.remove((40, 40, 40))


print(pixels_uniques) #Afficher les valeurs 
print(len(pixels_uniques)) #Afficher le nombre de valeurs 


#image.putpixel((x, y), (255, 0, 0))  # Remplacer un pixel par du rouge
