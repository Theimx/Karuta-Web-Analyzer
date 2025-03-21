import csv

frames = []
wl = 0
total_value = 0
burnValue = 0

frame_values = {  # Dictionnaire associant chaque frame à une valeur (En tickets)
    'yearofthesnake': 3,
    'yearoftherabbit': 3,
    'yearofthesheep': 3,
    'yearofthedragon': 3,
    'yearoftheboar': 3,
    'yearoftheox': 3,
    'yearofthehorse': 3,
    'yearofthedog': 3,
    'yearoftherooster': 3,
    'yearoftherat': 3,

    'mingvase': 5,
    'springrain': 4,
    'alienalloy': 7,
    'kitsune': 12,

    'cherryberry': 3,
    'carnations': 3,
    'blossom': 3,
    'musicalnotes': 3,    
    'abandonedchurch': 3,    
    'labpunk': 3,

    'grimrose': 30,
    'apollo': 30,
    'ripple': 20,
    'roseknight': 49,
    



    'archlight': 10000,
    'ashes': 10000,
    'ascendant': 10000,
    'autumnbreeze': 10000,
    'autumnview': 10000,
    'azureclaw': 10000,
    'barbecue': 10000,
    'baroque': 10000,
    'beach': 10000,
    'beachtowel': 10000,
    'bloodmoonbite': 10000,
    'boneslasher': 10000,
    'brass': 10000,
    'bridesmaid': 10000,
    'brokenmirror': 10000,
    'bubbletea': 10000,
    'bunnypaws': 10000,
    'butterflywoods': 10000,
    'butterflygarden': 10000,
    'chaosborn': 10000,
    'cleave': 10000,
    'coffeeshop': 10000,
    'coralreef': 10000,
    'cosmicentity': 10000,
    'crystalwings': 10000,
    'crystallinelocket': 10000,
    'crow': 10000,
    'cursedplace': 10000,
    'divinity': 10000,
    'dragonfruit': 10000,
    'dragonhunt': 10000,
    'easel': 10000,
    'edofurin': 10000,
    'electrified': 10000,
    'explosion': 10000,
    'faerieforest': 10000,
    'flyingdragon': 10000,
    'frenchmaid': 10000,
    'gamingchair': 10000,
    'gildedstars': 10000,
    'glinted': 10000,
    'glory': 10000,
    'goldrank': 10000,
    'gothiccloak': 10000,
    'gothictower': 10000,
    'groomsman': 10000,
    'hacker': 10000,
    'hangingscrolls': 10000,
    'harpstring': 10000,
    'heartbreak': 10000,
    'heartofsilver': 10000,
    'higasa': 10000,
    'holyknight': 10000,
    'husband': 10000,
    'icicle': 10000,
    'illusion': 10000,
    'infinityvoid': 10000,
    'interface': 10000,
    'islandluau': 10000,
    'japanesealley': 10000,
    'karutaboy': 10000,
    'kawaiibento': 10000,


    'lifedeath': 10000,
    'lich': 10000,
    'lighthousestorm': 10000,
    'livestream': 10000,
    'magicalgirl': 10000,
    'magitek': 10000,
    'magitor': 10000,
    'magus': 10000,
    'malicetree': 10000,
    'mahou': 10000,
    'manekineko': 10000,
    'mermaid': 10000,
    'midnightbloom': 10000,
    'mirroredenergy': 10000,
    'nether': 10000,
    'nightfestival': 10000,
    'nightmare': 25,
    'nightooze': 3,
    'nova': 40,
    'nightwalker': 20,
    'wizardshut': 3,
    'winnerspodium': 3
}

with open('Theimx.csv', 'r', newline='', encoding='utf-8') as fichier:
    reader = csv.reader(fichier)  

    next(reader)# Ignore la première ligne (en-tête)

    for ligne in reader:
        burnValue += int(ligne[8])  
        wl += int(ligne[16])

        if ligne[11]:  # Vérifie si la colonne 12 (index 11) n'est pas vide
            frames.append(ligne[11])

for frame in frames:
    if frame in frame_values:  
        total_value += frame_values[frame]



print("----- Statistiques -----")
print(burnValue," Gold (Total Gold )")
print(wl," Whishlist (Total Whishlist )")
print(" ")
print("----- Tickets -----")
print(total_value, " Tickets ( Values of the Frames)")
print(burnValue // 2500, "Tickets (In gold )")
print(" ")
print((total_value+(burnValue // 2500)),"  Tickets (Total)")
print(" ")
