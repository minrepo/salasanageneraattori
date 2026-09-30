"""Salasanageneraattori. jokaisessa salasanassa on:
3–4 erilaista suomenkielistä sanaa
satunnainen luku
yksi satunnainen erikoismerkki"""

import secrets
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

SANALISTA = Path("sanalista.txt")

if not SANALISTA.exists():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Sanalistaa ei löytynyt",
        "Tiedostoa sanalista.txt ei löytynyt ohjelman kansiosta."
    )
    root.destroy()
    raise SystemExit

def lataa_sanat():
    """Lataa vähintään kolme kirjainta sisältävät sanat sanalistasta."""
    sanat = []
    try:
        with SANALISTA.open("r", encoding="utf-8") as tiedosto:
            # ohita otsikkorivi
            next(tiedosto, None)
            for rivi in tiedosto:
                osat = rivi.strip().split("\t")
                if not osat[0]:
                    continue
                sana = "".join(osat[0].split())
                if len(sana) >= 3 and sana.isalpha():
                    sanat.append(sana)
    except (OSError, UnicodeError) as virhe:
        messagebox.showerror(
            "Sanalistan lukeminen epäonnistui",
            f"Sanalistaa ei voitu lukea:\n{virhe}"
        )
        raise SystemExit from virhe

    return sanat

SANAT = lataa_sanat()

if len(SANAT) < 4:
    messagebox.showerror(
        "Sanalistavirhe",
        "Sanalistassa täytyy olla vähintään 4 sopivaa sanaa."
    )
    raise SystemExit

def valitse_uniikit_sanat(maara):
    """Valitsee eri sanat ilman toistoja."""
    return secrets.SystemRandom().sample(SANAT, maara)

MAX_PITUUS = 40
ERIKOISMERKIT = "!#%&+-=?@"

def generoi_salasana():
    """Luo satunnaisen salasanan, jolla on maksimipituus."""
    for _ in range(1000):
        # 3 tai 4 sanaa
        sanojen_maara = secrets.choice([3, 4])
        sanat = [
            sana.capitalize()
            for sana in valitse_uniikit_sanat(sanojen_maara)
        ]
       # sanat = valitse_uniikit_sanat(sanojen_maara)
        # Satunnainen numero ja erikoismerkki
        numero = f"{secrets.randbelow(10000)}"
        erikoismerkki = secrets.choice(ERIKOISMERKIT)

        osat = sanat + [numero, erikoismerkki]

        # Sekoitetaan osien järjestys
        secrets.SystemRandom().shuffle(osat)

        salasana = "".join(osat)
        if len(salasana) <= MAX_PITUUS:
            return salasana
    raise RuntimeError(
        "Sopivaa salasanaa ei löytynyt 1000 yrityksellä."
    )

# Käyttöliittymä
ikkuna = tk.Tk()
ikkuna.title("Salasanageneraattori")
ikkuna.geometry("700x200")

salasana_var = tk.StringVar()

def uusi_salasana():
    """Luo ja näyttää salasanan"""
    salasana_var.set(generoi_salasana())

otsikko = tk.Label(
    ikkuna,
    text="Valitse vahva salasana",
    font=("Arial", 14)
)
otsikko.pack(pady=10)

salasana_kentta = tk.Entry(
    ikkuna,
    textvariable=salasana_var,
    font=("Consolas", 16),
    justify="center",
    width=50
)
salasana_kentta.pack(pady=10)

salasana_var.set(generoi_salasana())

painike = tk.Button(
    ikkuna,
    text="Luo uusi salasana",
    command=uusi_salasana,
    font=("Arial", 12)
)
painike.pack(pady=10)

ikkuna.mainloop()
