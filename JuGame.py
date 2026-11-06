"""
JuGame - joc în Python inspirat de Snake.

O mașină (A) merge pe o stradă. Colectează puncte (*) și evită obstacolele (#).
Rulează oriunde, inclusiv în Google Colab, pentru că folosește doar
biblioteca standard Python.

Comenzi (scrie litera și apasă Enter):
  a = stânga   d = dreapta   w = sus   s = jos
  Enter = rămâi pe loc       q = ieșire
"""
import random

LATIME = 11              # numărul de coloane ale străzii
INALTIME = 12            # numărul de rânduri
VIETI_START = 3          # câte ciocniri poți suporta
PUNCTE_VICTORIE = 15     # scorul necesar pentru a câștiga
PROBABILITATE_PUNCT = 0.35
PROBABILITATE_OBSTACOL = 0.30


def stare_noua():
    """Creează starea de început a jocului."""
    return {
        "masina": [INALTIME - 1, LATIME // 2],   # [rând, coloană]
        "obiecte": [],                           # liste de [rând, coloană, tip]
        "scor": 0,
        "vieti": VIETI_START,
    }


def muta_masina(stare, comanda):
    """Mută mașina o poziție, fără să iasă de pe stradă."""
    rand, col = stare["masina"]
    if comanda == "a":
        col -= 1
    elif comanda == "d":
        col += 1
    elif comanda == "w":
        rand -= 1
    elif comanda == "s":
        rand += 1
    rand = max(0, min(INALTIME - 1, rand))
    col = max(0, min(LATIME - 1, col))
    stare["masina"] = [rand, col]


def verifica_ciocniri(stare):
    """Dacă un obiect e pe poziția mașinii: punct = +1 scor, obstacol = -1 viață."""
    rest = []
    for rand, col, tip in stare["obiecte"]:
        if [rand, col] == stare["masina"]:
            if tip == "*":
                stare["scor"] += 1
            else:
                stare["vieti"] -= 1
        else:
            rest.append([rand, col, tip])
    stare["obiecte"] = rest


def deplaseaza_obiecte(stare):
    """Strada se derulează: obiectele coboară cu un rând, cele ieșite dispar."""
    for obiect in stare["obiecte"]:
        obiect[0] += 1
    stare["obiecte"] = [o for o in stare["obiecte"] if o[0] < INALTIME]


def adauga_obiecte(stare):
    """Pe rândul de sus pot apărea puncte și obstacole, pe coloane diferite."""
    coloane = list(range(LATIME))
    random.shuffle(coloane)
    if random.random() < PROBABILITATE_PUNCT:
        stare["obiecte"].append([0, coloane.pop(), "*"])
    if random.random() < PROBABILITATE_OBSTACOL:
        stare["obiecte"].append([0, coloane.pop(), "#"])


def deseneaza(stare):
    """Afișează strada în text."""
    harta = [["." for _ in range(LATIME)] for _ in range(INALTIME)]
    for rand, col, tip in stare["obiecte"]:
        harta[rand][col] = tip
    rand, col = stare["masina"]
    harta[rand][col] = "A"
    print()
    print("+" + "-" * LATIME + "+")
    for linie in harta:
        print("|" + "".join(linie) + "|")
    print("+" + "-" * LATIME + "+")
    print(f"Scor: {stare['scor']}/{PUNCTE_VICTORIE}   Vieți: {stare['vieti']}")


def joaca(seed=None, comenzi=None):
    """Bucla principală. `comenzi` (opțional) e folosit doar pentru teste."""
    if seed is not None:
        random.seed(seed)
    stare = stare_noua()
    print("Bine ai venit la JuGame! Colectează * și evită #.")
    print("Comenzi: a/d/w/s + Enter (stânga/dreapta/sus/jos), q = ieșire.")

    while True:
        deseneaza(stare)
        if stare["scor"] >= PUNCTE_VICTORIE:
            print("Ai câștigat! Felicitări!")
            return "victorie"
        if stare["vieti"] <= 0:
            print("Ai pierdut. Încearcă din nou!")
            return "infrangere"

        if comenzi is not None:
            comanda = next(comenzi, "q")
        else:
            try:
                comanda = input("Mutare: ").strip().lower()
            except EOFError:
                comanda = "q"
        if comanda == "q":
            print("Ieșire din joc.")
            return "iesire"

        muta_masina(stare, comanda)
        verifica_ciocniri(stare)      # ciocniri după mutarea mașinii
        deplaseaza_obiecte(stare)
        verifica_ciocniri(stare)      # ciocniri după derularea străzii
        adauga_obiecte(stare)


if __name__ == "__main__":
    joaca()
