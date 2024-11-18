import numpy as np

x_offset = -781
pixel_x_offset = -30
pixel_y_offset = -27
pixel_multiplier = 9.206349

mittaus = input("(P)ituus, (A)lue vai (K)oordinaatin muutos: ")

if "p" in mittaus.lower():
    pikselit = int(input("Anna pituus pikseleinä: "))
    pituus = int(np.round(pikselit * pixel_multiplier, 0))
    print(f"Pituus on ~{pituus} senttimetriä.")

elif "a" in mittaus.lower():
    x1 = int(input("Anna x1-koordinaatti: "))
    y1 = int(input("Anna y1-koordinaatti: "))
    x2 = int(input("Anna x2-koordinaatti: "))
    y2 = int(input("Anna y2-koordinaatti: "))
    # Alue neliömetreinä
    alue = np.round(((x2 - x1) * (y2 - y1) * pixel_multiplier) / 10000, 2)
    print(f"Alue on ~{alue} neliömetriä.")

elif "k" in mittaus.lower():
    x = int(input("Anna x-koordinaatti: "))
    y = int(input("Anna y-koordinaatti: "))
    x = x + pixel_x_offset
    y = y + pixel_y_offset
    x = round(x * pixel_multiplier + x_offset)
    y = round(y * pixel_multiplier)
    print(f"Koordinaatit ovat {x}, {y}.")
