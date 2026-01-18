// ===================== LOGIQUE =====================

function determinePrintType(n) {
    if (n <= 10) return "SP";
    if (n <= 100) return "LP";
    if (n <= 1000) return "MP";
    return "HP";
}

const editionValues = {
    1:{SP:[2,4],LP:[8,14],MP:[70,100],HP:[750,950]},
    2:{SP:[2,4],LP:[8.2,15.2],MP:[65,95],HP:[720,840]},
    3:{SP:[2,4],LP:[8,15],MP:[60,90],HP:[590,700]},
    4:{SP:[2,4],LP:[7,13],MP:[55,85],HP:[380,470]},
    5:{SP:[2,4],LP:[8.1,12.1],MP:[65,80],HP:[200,240]},
    6:{SP:[2,4],LP:[8,11],MP:[55,70],HP:[190,220]},
    7:{SP:[2,4],LP:[9,12],MP:[50,65],HP:[140,180]}
};

const frameValues = {
    yearoftherat:3, yearoftherabbit:3, yearofthesheep:3,
    yearofthedragon:3, yearoftheboar:3, yearoftheox:3,
    yearofthehorse:3, yearofthedog:3, yearoftherooster:3,
    yearofthesnake:3, yearofthetiger:3, yearofthemonkey:3,
    mingvase:5, springrain:4, alienalloy:7, kitsune:12,
    grimrose:30, apollo:30, ripple:20, roseknight:49,
    nightmare:25, nova:40, nightwalker:20
};

function estimateTicket(edition, type, wl) {
    const v = editionValues[edition]?.[type];
    if (!v) return 0;
    return wl / ((v[0] + v[1]) / 2);
}

// ===================== CSV =====================

const dropBox = document.getElementById("drop-box");

dropBox.addEventListener("dragover", e => {
    e.preventDefault();
    dropBox.classList.add("dragover");
});

dropBox.addEventListener("dragleave", () =>
    dropBox.classList.remove("dragover")
);

dropBox.addEventListener("drop", e => {
    e.preventDefault();
    dropBox.classList.remove("dragover");

    Papa.parse(e.dataTransfer.files[0], {
        skipEmptyLines: true,
        complete: res => analyse(res.data)
    });
});

function analyse(data) {
    let gold = 0, wl = 0, cardTickets = 0;
    let frames = [], sp = [], cards = [];

    data.slice(1).forEach(r => {
        const print = +r[1];
        const edition = +r[2];
        const wishlist = +r[16] || 0;
        const burn = +r[8] || 0;

        gold += burn;
        wl += wishlist;

        const type = determinePrintType(print);
        const value = estimateTicket(edition, type, wishlist) * 1e11;
        cardTickets += value;

        cards.push([r[0], r[3], r[4], value]);

        if (print <= 10)
            sp.push(`Code : ${r[0]} | Print : ${print} | Edition : ${edition} | ${r[3]} ${r[4]}`);

        if (r[11]) frames.push(r[11]);
    });

    const frameTickets = frames.reduce((s,f)=>s+(frameValues[f]||0),0);
    const goldTickets = Math.floor(gold / 2500);
    const cardsT = Math.round(cardTickets / 1e11);
    const total = frameTickets + cardsT;

    document.getElementById("gold").textContent = gold;
    document.getElementById("wl").textContent = wl;
    document.getElementById("frameTickets").textContent = frameTickets;
    document.getElementById("goldTickets").textContent = goldTickets;
    document.getElementById("cardTickets").textContent = cardsT;
    document.getElementById("totalTickets").textContent = total;

    document.getElementById("frames").innerHTML =
        frames.map(f => `<span class="badge">${f}</span>`).join("");

    document.getElementById("specialPrints").innerHTML =
        sp.map(x => `<li>${x}</li>`).join("");

    cards.sort((a,b)=>b[3]-a[3]);
    document.getElementById("topCards").innerHTML =
        cards.slice(0,20)
            .map(c => `<li>${c[0]}, ${c[1]}, ${c[2]} — ${Math.round(c[3]/1e11)} Tickets</li>`)
            .join("");
}
