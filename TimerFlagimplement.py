from tkinter import *
import tkinter as tk
import tkinter.messagebox
import random as rd
from PIL import Image, ImageTk
import time

# Funktion zum Generieren der Bombenpositionen
def bomben(bomb_numbers, size_x, size_y):
    durchläufe = 0
    bomben = []
    while durchläufe < bomb_numbers:
        try:
            X_Cordinate = rd.randint(0, size_x)
            Y_Cordniante = rd.randint(0, size_y)
            if (X_Cordinate, Y_Cordniante) not in bomben:
                bomben.append((X_Cordinate, Y_Cordniante))
                durchläufe += 1
            else:
                continue
        except:
            print("Zu viele Bomben")
            continue
    return bomben

# Funktion zum Finden der Nachbarfelder
def nachbarfelder_des_gecklickten_Feldes(x, y, size_x, size_y):
    nachbarn = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Feld selbst auslassen
            nachbar_x = x + dx
            nachbar_y = y + dy
            if 0 <= nachbar_x <= size_x and 0 <= nachbar_y <= size_y:
                nachbarn.append((nachbar_x, nachbar_y))
    return nachbarn

def anzahl_bomben_in_nachbarn(x, y, bomben_koord, size_x, size_y):
    nachbarn = nachbarfelder_des_gecklickten_Feldes(x, y, size_x, size_y)
    anzahl = sum((nx, ny) in bomben_koord for (nx, ny) in nachbarn)
    return anzahl


# Erzeugung des Spielfelds
def create_button_field(SIZE_X, SIZE_Y, root, bomb_coordinates, bomb_numbers):
    root.title("Minesweeper")
    root.geometry(f"{SIZE_X*100}x{SIZE_Y*100}")
    root.configure(bg="black")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    tiles = {}

    title = Label(root, text="Minesweeper", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=10)

    grid_frame = Frame(root, bg="black")
    grid_frame.pack(pady=10)

    flagged_coords = set()


    flag_img_pil = Image.open("Flagge.png").resize((40, 40))
    flag_img = ImageTk.PhotoImage(flag_img_pil)

    def on_left_click(x, y):
        if (x, y) in bomb_coordinates:
            end_time = time.time()
            elapsed_time = end_time - start_time
            tk.messagebox.showinfo(f"Game Over", "You hit a bomb!\nTime taken: {:.2f} seconds".format(elapsed_time))
            root.destroy()
            print("Flagged coordinates:", flagged_coords)
        else:
            nachbarn = nachbarfelder_des_gecklickten_Feldes(x, y, SIZE_X - 1, SIZE_Y - 1)
            print(f"Linksklick auf Feld {x}_{y}")
            print(f"Nachbarfelder: {nachbarn}")
            anzahl = anzahl_bomben_in_nachbarn(x, y, bomb_coordinates, SIZE_X - 1, SIZE_Y - 1)
            print(f"Es befinden sich {anzahl} Bombe(n) um Feld {x}_{y}")
            button = tiles[x][y]["button"]
            button.config(text=str(anzahl) if anzahl > 0 else "", state="disabled", disabledforeground="black",
                          bg="#e0e0e0")



    def on_right_click(x, y):
        btn = tiles[x][y]["button"]
        if (x, y) in flagged_coords:
            flagged_coords.remove((x, y))
            btn.config(image="", compound=None, width=4, height=2)  # keep size
            print(f"Unflagged tile {x}_{y}")
        else:
            if len(flagged_coords) < bomb_numbers:
                flagged_coords.add((x, y))
                btn.config(image=flag_img, compound="center", width=32, height=35)  # keep size
                print(f"flagged tile {x}_{y}")
            else:
                tk.messagebox.showinfo("All flags Used!", "All flags Used! Please remove one before adding another Flag!")
        print(f"Flagged tiles: {flagged_coords}")

    tiles = {}
    for x in range(0, SIZE_X):
        tiles[x] = {}
        for y in range(0, SIZE_Y):
            button = Button(grid_frame, width=4, height=2, bg="white", fg="black")
            button.grid(row=y, column=x, padx=2, pady=2)
            button.bind("<Button-1>", lambda event, x=x, y=y: on_left_click(x, y))
            button.bind("<Button-3>", lambda event, x=x, y=y: on_right_click( x, y))
            tiles[x][y] = {
                "id": f"{x}{y}",
                "coords": {"x": x, "y": y},
                "button": button,
            }

    return flagged_coords

# Hauptprogramm
size_x = int(input("Enter the number of columns: "))
size_y = int(input("Enter the number of rows: "))
bombenanzahl_x = size_x - 1
bombenanzahl_y = size_y - 1

bomb_numbers = int(input("Enter the number of bombs: "))
start_time = time.time()
bomb_coordinates = bomben(bomb_numbers, bombenanzahl_x, bombenanzahl_y)
print("Bomben-Koordinaten:", bomb_coordinates)

root = tk.Tk()
create_button_field(size_x, size_y, root, bomb_coordinates, bomb_numbers)
root.mainloop()