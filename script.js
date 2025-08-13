const message = document.getElementById("message");
const curseur = document.getElementById("monCurseur");
const valeurAffichee = document.getElementById("valeurAffichee");
const btn1 = document.getElementById("monBouton");
const btn2 = document.getElementById("secondBouton");

let valeurCurseur = curseur.value;

// Mise à jour en direct
curseur.addEventListener("input", () => {
    valeurCurseur = curseur.value;
    valeurAffichee.textContent = valeurCurseur;
});

// Bouton 1
btn1.addEventListener("click", () => {
    message.textContent = "Valeur du curseur : " + valeurCurseur;
});

// Bouton 2
btn2.addEventListener("click", () => {
    message.textContent = "Bouton 2 cliqué avec curseur à " + valeurCurseur;
});
