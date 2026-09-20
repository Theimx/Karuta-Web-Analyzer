/* ============================================================
   KARUTA COLLECTION ANALYZER — logic
   ============================================================ */

"use strict";

// ================= THEME (light / dark) =================

const themeToggle = document.getElementById("themeToggle");
const iconSun  = themeToggle.querySelector(".icon-sun");
const iconMoon = themeToggle.querySelector(".icon-moon");

function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    iconSun.hidden  = theme === "dark";
    iconMoon.hidden = theme !== "dark";
    try { localStorage.setItem("karuta-theme", theme); } catch {}
}

(function initTheme() {
    let saved = null;
    try { saved = localStorage.getItem("karuta-theme"); } catch {}
    if (!saved) {
        saved = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    applyTheme(saved);
})();

themeToggle.addEventListener("click", () => {
    applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
});


// ================= VALUE ESTIMATION =================

function determinePrintType(n) {
    if (n <= 10) return "SP";
    if (n <= 100) return "LP";
    if (n <= 1000) return "MP";
    return "HP";
}

const editionValues = {
    1: { SP: [2, 4],     LP: [8, 14],     MP: [70, 100],  HP: [750, 950] },
    2: { SP: [2, 4],     LP: [8.2, 15.2], MP: [65, 95],   HP: [720, 840] },
    3: { SP: [2, 4],     LP: [8, 15],     MP: [60, 90],   HP: [590, 700] },
    4: { SP: [2, 4],     LP: [7, 13],     MP: [55, 85],   HP: [380, 470] },
    5: { SP: [2, 4],     LP: [8.1, 12.1], MP: [65, 80],   HP: [200, 240] },
    6: { SP: [2, 4],     LP: [8, 11],     MP: [55, 70],   HP: [190, 220] },
    7: { SP: [2, 4],     LP: [9, 12],     MP: [50, 65],   HP: [140, 180] }
};

function estimateTicket(edition, type, wl) {
    const v = editionValues[edition]?.[type];
    if (!v) return 0;
    return wl / ((v[0] + v[1]) / 2);
}

// ================= BACKGROUND MOTIFS =================

const MOTIF_CHARS = ["カ", "ル", "タ", "集", "愛", "神", "龍", "風", "水", "火", "山", "月", "星", "空", "花", "梦", "力", "心"];

(function buildMotifs() {
    const container = document.getElementById("bgMotifs");
    const positions = [
        { top: "4%",  left: "42%", size: 120, rot: -8 },
        { top: "12%", left: "70%", size: 90,  rot: 6 },
        { top: "30%", left: "55%", size: 150, rot: 4 },
        { top: "55%", left: "45%", size: 100, rot: -6 },
        { top: "72%", left: "68%", size: 130, rot: 10 },
        { top: "85%", left: "50%", size: 85,  rot: -4 },
        { top: "8%",  left: "88%", size: 110, rot: 8 },
        { top: "48%", left: "85%", size: 95,  rot: -10 },
        { top: "78%", left: "88%", size: 140, rot: 5 },
        { top: "35%", left: "92%", size: 75,  rot: -5 },
        { top: "62%", left: "38%", size: 70,  rot: 12 },
        { top: "18%", left: "50%", size: 80,  rot: -12 }
    ];
    positions.forEach((p, i) => {
        const el = document.createElement("div");
        el.className = "motif";
        el.textContent = MOTIF_CHARS[i % MOTIF_CHARS.length];
        el.style.top = p.top;
        el.style.left = p.left;
        el.style.width = p.size + "px";
        el.style.height = p.size + "px";
        el.style.fontSize = Math.round(p.size * 0.58) + "px";
        el.style.transform = `rotate(${p.rot}deg)`;
        container.appendChild(el);
    });
})();

// ================= STATE =================

let cards = [];

const filters = {
    search: "",
    minValue: 0,
    maxPrint: 2020,
    sort: "value",
    tag: "any",
    framed: "any",
    morphed: "any",
    trimmed: "any",
    editions: new Set([1, 2, 3, 4, 5, 6, 7])
};

// ================= DOM REFS =================

const dropBox      = document.getElementById("dropBox");
const fileInput    = document.getElementById("fileInput");
const browseBtn    = document.getElementById("browseBtn");
const fileNameEl   = document.getElementById("fileName");
const searchInput  = document.getElementById("searchInput");
const valueRange   = document.getElementById("valueRange");
const valueLabel   = document.getElementById("valueLabel");
const printRange   = document.getElementById("printRange");
const printLabel   = document.getElementById("printLabel");
const sortBtn      = document.getElementById("sortBtn");
const sortMenu     = document.getElementById("sortMenu");
const sortLabel    = document.getElementById("sortLabel");
const rowsEl       = document.getElementById("rows");
const emptyEl      = document.getElementById("empty");
const tableEl      = document.getElementById("table");
const statsEl      = document.getElementById("stats");
const contentTitle = document.getElementById("contentTitle");
const contentSub   = document.getElementById("contentSub");
const resetBtn     = document.getElementById("resetBtn");

const overlay        = document.getElementById("overlay");
const overlayCard    = document.querySelector(".overlay-card");
const overlayClose   = document.getElementById("overlayClose");
const overlayBackdrop = document.getElementById("overlayBackdrop");
const ovSeries       = document.getElementById("ovSeries");
const ovName         = document.getElementById("ovName");
const ovBadges       = document.getElementById("ovBadges");
const ovCode         = document.getElementById("ovCode");
const ovMeta         = document.getElementById("ovMeta");
const codeBox        = document.getElementById("codeBox");
const copyHint       = document.getElementById("copyHint");
const toast          = document.getElementById("toast");

// ================= CSV LOADING =================

dropBox.addEventListener("click", () => fileInput.click());

dropBox.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        fileInput.click();
    }
});

browseBtn.addEventListener("click", e => {
    e.stopPropagation();
    fileInput.click();
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length) loadFile(fileInput.files[0]);
});

dropBox.addEventListener("dragover", e => {
    e.preventDefault();
    dropBox.classList.add("dragover");
});

dropBox.addEventListener("dragleave", () => {
    dropBox.classList.remove("dragover");
});

dropBox.addEventListener("drop", e => {
    e.preventDefault();
    dropBox.classList.remove("dragover");

    if (e.dataTransfer.files.length) {
        loadFile(e.dataTransfer.files[0]);
    }
});

function loadFile(file) {
    fileNameEl.textContent = file.name;

    Papa.parse(file, {
        skipEmptyLines: true,
        complete: res => analyse(res.data)
    });
}

function analyse(data) {
    cards = data.slice(1).map(r => {
        const print = +r[1];
        const edition = +r[2];
        const wishlist = +r[16] || 0;
        const type = determinePrintType(print);
        const value = estimateTicket(edition, type, wishlist) * 1e11;

        return {
            code: r[0],
            print,
            edition,
            character: r[3],
            series: r[4],
            quality: +r[6] || 0,
            burn: +r[8] || 0,
            frame: r[11] || "",
            morphed: (r[12] || "").toLowerCase() === "yes",
            trimmed: (r[13] || "").toLowerCase() === "yes",
            tag: (r[14] || "").trim(),
            wishlist,
            type,
            value
        };
    });

    contentTitle.textContent = "Your collection";
    contentSub.textContent = `${cards.length} cards loaded — click a row to view and copy its code.`;
    statsEl.hidden = false;
    tableEl.hidden = false;

    render();
}

// ================= FILTERING & RENDERING =================

function yesNoMatch(value, mode) {
    if (mode === "any") return true;
    if (mode === "yes") return value === true || value !== "";
    return value === false || value === "";
}

const sortRules = {
    value: (a, b) => b.value - a.value,
    print: (a, b) => a.print - b.print,
    wishlist: (a, b) => b.wishlist - a.wishlist
};

function applyFilters() {
    const q = filters.search.trim().toLowerCase();

    return cards.filter(c => {
        if (!filters.editions.has(c.edition)) return false;

        if (Math.round(c.value / 1e11) < filters.minValue) {
            return false;
        }

        // 2020 = 2000+ = aucune limite supérieure de print
        if (filters.maxPrint < 2020 && c.print > filters.maxPrint) {
            return false;
        }

        if (!yesNoMatch(c.tag, filters.tag)) return false;
        if (!yesNoMatch(c.frame, filters.framed)) return false;
        if (!yesNoMatch(c.morphed, filters.morphed)) return false;
        if (!yesNoMatch(c.trimmed, filters.trimmed)) return false;

        if (
            q &&
            ![c.code, c.character, c.series]
                .some(x => (x || "").toLowerCase().includes(q))
        ) {
            return false;
        }

        return true;
    }).sort(sortRules[filters.sort] || sortRules.value);
}

function flagHtml(c) {
    const flags = [];

    if (c.tag) flags.push('<span class="flag tag">TAG</span>');
    if (c.frame) flags.push('<span class="flag">FRAME</span>');
    if (c.morphed) flags.push('<span class="flag">MORPHED</span>');
    if (c.trimmed) flags.push('<span class="flag">TRIMMED</span>');

    return flags.join("");
}

function render() {
    if (!cards.length) return;

    const list = applyFilters();

    document.getElementById("stCards").textContent = list.length;

    document.getElementById("stGold").textContent =
        list.reduce((s, c) => s + c.burn, 0).toLocaleString("en-US");

    document.getElementById("stWl").textContent =
        list.reduce((s, c) => s + c.wishlist, 0).toLocaleString("en-US");

    document.getElementById("stTickets").textContent =
        Math.round(
            list.reduce((s, c) => s + c.value, 0) / 1e11
        ).toLocaleString("en-US");

    rowsEl.innerHTML = list.map((c, i) => `
        <div class="row" data-index="${i}">
            <span class="code">${escapeHtml(c.code)}</span>
            <span class="char">${escapeHtml(c.character)}</span>
            <span class="series">${escapeHtml(c.series)}</span>
            <span>Ed. ${c.edition}</span>
            <span>#${c.print.toLocaleString("en-US")}</span>
            <span>
                <span class="type-badge type-${c.type}">
                    ${c.type}
                </span>
            </span>
            <span class="num value">
                ${Math.round(c.value / 1e11)} TCX
            </span>
            <span class="flags">${flagHtml(c)}</span>
        </div>
    `).join("");

    emptyEl.classList.toggle("show", list.length === 0);
}

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, m => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    }[m]));
}

// ================= ROW CLICK → OVERLAY =================

rowsEl.addEventListener("click", e => {
    const row = e.target.closest(".row");

    if (!row) return;

    const list = applyFilters();

    openOverlay(list[+row.dataset.index]);
});

// ================= FILTER UI EVENTS =================

searchInput.addEventListener("input", () => {
    filters.search = searchInput.value;
    render();
});

valueRange.addEventListener("input", () => {
    filters.minValue = +valueRange.value;

    valueLabel.textContent =
        filters.minValue >= 150
            ? "150+ TCX"
            : `${filters.minValue}+ TCX`;

    render();
});

printRange.addEventListener("input", () => {
    filters.maxPrint = +printRange.value;

    printLabel.textContent =
        filters.maxPrint >= 2020
            ? "2000+"
            : `${filters.maxPrint}`;

    render();
});

// ================= SORT MENU =================

sortBtn.addEventListener("click", e => {
    e.stopPropagation();

    sortMenu.hidden = !sortMenu.hidden;
    sortBtn.classList.toggle("open", !sortMenu.hidden);
});

sortMenu.addEventListener("click", e => {
    const opt = e.target.closest(".sort-opt");

    if (!opt) return;

    filters.sort = opt.dataset.sort;
    sortLabel.textContent = opt.textContent;

    sortMenu
        .querySelectorAll(".sort-opt")
        .forEach(o => o.classList.toggle("active", o === opt));

    sortMenu.hidden = true;
    sortBtn.classList.remove("open");

    render();
});

document.addEventListener("click", e => {
    if (!sortMenu.hidden && !e.target.closest(".sort-wrap")) {
        sortMenu.hidden = true;
        sortBtn.classList.remove("open");
    }
});

document.addEventListener("keydown", e => {
    if (e.key === "Escape" && !sortMenu.hidden) {
        sortMenu.hidden = true;
        sortBtn.classList.remove("open");
    }
});

document.querySelectorAll(".segmented").forEach(group => {
    group.addEventListener("click", e => {
        const btn = e.target.closest(".seg");

        if (!btn) return;

        group
            .querySelectorAll(".seg")
            .forEach(b => b.classList.remove("active"));

        btn.classList.add("active");

        filters[group.dataset.filter] = btn.dataset.value;

        render();
    });
});

document.getElementById("editionChips").addEventListener("click", e => {
    const chip = e.target.closest(".chip");

    if (!chip) return;

    chip.classList.toggle("active");

    const ed = +chip.dataset.value;

    if (chip.classList.contains("active")) {
        filters.editions.add(ed);
    } else {
        filters.editions.delete(ed);
    }

    render();
});

// ================= RESET =================

resetBtn.addEventListener("click", () => {
    filters.search = "";
    filters.minValue = 0;

    // 2020 = 2000+ = toutes les cartes
    filters.maxPrint = 2020;

    filters.tag =
        filters.framed =
        filters.morphed =
        filters.trimmed = "any";

    filters.editions = new Set([1, 2, 3, 4, 5, 6, 7]);

    searchInput.value = "";

    valueRange.value = 0;
    valueLabel.textContent = "0+ TCX";

    printRange.value = 2020;
    printLabel.textContent = "2000+";

    document.querySelectorAll(".segmented").forEach(g =>
        g.querySelectorAll(".seg").forEach(b =>
            b.classList.toggle("active", b.dataset.value === "any")
        )
    );

    document
        .querySelectorAll("#editionChips .chip")
        .forEach(c => c.classList.add("active"));

    render();
});

// ================= OVERLAY & COPY =================

let currentCard = null;

function openOverlay(card) {
    if (!card) return;

    currentCard = card;

    ovSeries.textContent = card.series;
    ovName.textContent = card.character;
    ovCode.textContent = card.code;

    ovMeta.textContent =
        `Edition ${card.edition} · Print #${card.print.toLocaleString("en-US")} · ${card.type}` +
        ` · ~${Math.round(card.value / 1e11)} TCX` +
        (card.frame ? ` · Frame: ${card.frame}` : "");

    const badges = [];

    if (card.tag) badges.push('<span class="flag tag">TAG</span>');
    if (card.frame) badges.push('<span class="flag">FRAME</span>');
    if (card.morphed) badges.push('<span class="flag">MORPHED</span>');
    if (card.trimmed) badges.push('<span class="flag">TRIMMED</span>');

    ovBadges.innerHTML = badges.join("");

    codeBox.classList.remove("copied");
    copyHint.innerHTML = copyHintSvg() + " Click to copy";

    overlay.hidden = false;
    document.body.style.overflow = "hidden";
}

function closeOverlay() {
    overlay.hidden = true;
    document.body.style.overflow = "";
    currentCard = null;
}

overlayClose.addEventListener("click", closeOverlay);
overlayBackdrop.addEventListener("click", closeOverlay);

document.addEventListener("keydown", e => {
    if (e.key === "Escape" && !overlay.hidden) {
        closeOverlay();
    }
});

function copyHintSvg() {
    return '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>';
}

codeBox.addEventListener("click", async () => {
    if (!currentCard) return;

    try {
        await navigator.clipboard.writeText(currentCard.code);
    } catch {
        const ta = document.createElement("textarea");

        ta.value = currentCard.code;

        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        ta.remove();
    }

    codeBox.classList.add("copied");

    copyHint.innerHTML =
        '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12l5 5L20 7"/></svg> Copied!';

    toast.classList.add("show");

    clearTimeout(toast._t);

    toast._t = setTimeout(
        () => toast.classList.remove("show"),
        1800
    );
});