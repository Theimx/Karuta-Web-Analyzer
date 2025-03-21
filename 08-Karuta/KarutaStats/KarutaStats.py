import csv

frames = []
wl = 0
total_value = 0
burnValue = 0
value = 0

def determine_print_type(print_number):
    if 1 <= print_number <= 10:
        return "Special Print"
    elif 11 <= print_number <= 100:
        return "Light Print"
    elif 101 <= print_number <= 1000:
        return "Mid Print"
    else:
        return "High Print"

def estimate_ticket_value(edition, print_type, wl):
    min_value = max_value = 0
    
    if edition == 1:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8, 14
        elif print_type == "Mid Print":
            min_value, max_value = 70, 100
        elif print_type == "High Print":
            min_value, max_value = 750, 950
    elif edition == 2:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8.2, 15.2
        elif print_type == "Mid Print":
            min_value, max_value = 65, 95
        elif print_type == "High Print":
            min_value, max_value = 720, 840
    elif edition == 3:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8, 15
        elif print_type == "Mid Print":
            min_value, max_value = 60, 90
        elif print_type == "High Print":
            min_value, max_value = 590, 700
    elif edition == 4:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 7, 13
        elif print_type == "Mid Print":
            min_value, max_value = 55, 85
        elif print_type == "High Print":
            min_value, max_value = 380, 470
    elif edition == 5:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8.1, 12.1
        elif print_type == "Mid Print":
            min_value, max_value = 65, 80
        elif print_type == "High Print":
            min_value, max_value = 200, 240
    elif edition == 6:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8, 11
        elif print_type == "Mid Print":
            min_value, max_value = 55, 70
        elif print_type == "High Print":
            min_value, max_value = 190, 220
    elif edition == 7:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 9, 12
        elif print_type == "Mid Print":
            min_value, max_value = 50, 65
        elif print_type == "High Print":
            min_value, max_value = 140, 180
    
    if min_value == 0 and max_value == 0:
        return 0  # Valeur par défaut si aucune correspondance
    
    avg_value = (min_value + max_value) / 2  # Moyenne des valeurs
    return wl / avg_value  # Conversion en tickets


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

        edition = int(ligne[2])  # Convertit en entier
        print_number = int(ligne[1])  # Récupère le numéro du print
        print_type = determine_print_type(print_number)  # Détermine le type de print
        whishList = int(ligne[16])  # Convertit en entier
        ticket_value = (estimate_ticket_value(edition, print_type, whishList)* 100000000000)
        value += ticket_value

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
print(round((value/100000000000)), " Value of every card of the collection (Print,Edition and Whishlist)")
print(" ")
print((total_value+ round((value/100000000000))),"  Tickets (Card + Frame Value)")
print(" ")
