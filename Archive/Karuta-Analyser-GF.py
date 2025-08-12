import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import sys
import os

def analyser_fichier():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return

    with open("Karuta-Collection-analyser-V1.py", "r", encoding="utf-8") as f:
        original_code = f.read()

    # Corriger le chemin avec échappement des backslashes
    filepath_fixed = filepath.replace("\\", "\\\\")
    temp_code = original_code.replace('fileToAnalyse = "Theimx.csv"', f'fileToAnalyse = "{filepath_fixed}"')

    temp_script = "temp_script.py"
    with open(temp_script, "w", encoding="utf-8") as f:
        f.write(temp_code)

    # Exécute le script temporaire et récupère la sortie
    result = subprocess.run([sys.executable, temp_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, result.stdout)
    if result.stderr:
        output_box.insert(tk.END, "\n--- Erreurs ---\n" + result.stderr)

    os.remove(temp_script)

# Interface graphique
root = tk.Tk()
root.title("Karuta Analyzer")

btn = tk.Button(root, text="Charger un fichier CSV", command=analyser_fichier)
btn.pack(pady=10)

output_box = scrolledtext.ScrolledText(root, width=110, height=40, font=("Courier", 9))
output_box.pack(padx=10, pady=10)

root.mainloop()
