from tkinter import *
import tkinter as tk
import tkinter.messagebox
import random as rd
import time

def bomben(bomb_numbers, size_x, size_y):
    durchläufe = 0
    bomben = []
    while (durchläufe < bomb_numbers):
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
        
def create_button_field(SIZE_X, SIZE_Y, root, bomb_coordinates,bomb_numbers):
    # Create window
    root.title("Minesweeper")
    root.geometry(f"{SIZE_X*100}x{SIZE_Y*100}")
    root.configure(bg="black")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    title = Label(root, text="Minesweeper", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=10)

    grid_frame = Frame(root, bg="black")
    grid_frame.pack(pady=10)

    flagged_coords = set()  
    #Für Christoph, Sets funktionieren so wie Listen,
    #nur dass sie keine doppelten Werte haben können
    #Die brauch i eif für die Flaggen weil falls ma an fehler macht
    #kann man die Flag sonst nd weg löschen

    def on_left_click(x, y):
        if (x, y) in bomb_coordinates:
            tk.messagebox.showinfo("Game Over", "You hit a bomb!")
            root.destroy()
            print("Flagged coordinates:", flagged_coords)
        else:
            print(f"Left click on tile {x}_{y}")
        
    def on_right_click(event, x, y):
            if (x, y) in flagged_coords:
                flagged_coords.remove((x, y))
                print(f"Unflagged tile {x}_{y}")
            else:
                if len(flagged_coords) < bomb_numbers:  
                    flagged_coords.add((x, y))
                    print(f"flagged tile {x}_{y}")
                else:
                    tk.messagebox.showinfo("All flags Used!", "All flags Used! Please remove one before adding another.")
                    return
            print(f"Flagged tiles: {flagged_coords}")


    tiles = {}
    for x in range(0, SIZE_X):
        tiles[x] = {}
        for y in range(0, SIZE_Y):
            button = Button(grid_frame, width=4, height=2, bg="white", fg="black")
            button.grid(row=y, column=x, padx=2, pady=2)
            button.bind("<Button-1>", lambda event, x=x, y=y: on_left_click(x, y))
            button.bind("<Button-3>", lambda event, x=x, y=y: on_right_click(event, x, y))
            tiles[x][y] = {
                "id": f"{x}{y}",
                "coords": {"x": x, "y": y},
                "button": button,
            }
    return flagged_coords
    

size_x = int(input("Enter the number of columns: "))
size_y = int(input("Enter the number of rows: "))
bombenanzahl_y = size_y -1
bombenanzahl_x = size_x -1

root = tk.Tk()

bomb_numbers = int(input("Enter the number of bombs: "))
bomb_coordinates = bomben(bomb_numbers, bombenanzahl_x, bombenanzahl_y)
print("Bomben-Koordinaten:", bomb_coordinates)

create_button_field(size_x, size_y, root, bomb_coordinates, bomb_numbers)

root.mainloop()