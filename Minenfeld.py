from tkinter import *
import tkinter as tk
import random as rd
import time

"""def bomben(bomb_numbers):
    durchläufe = 0
    while (durchläufe =< bomb_numbers):
        x = rd.randint(0, size_x)
        y = rd.randint(0, size_y)
"""
def create_button_field(SIZE_X, SIZE_Y, root):
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

    # Create button field
    tiles = {}
    for x in range(0, SIZE_X):
        tiles[x] = {}  # Initialize tiles[x] as an empty dictionary
        for y in range(0, SIZE_Y):
            button = Button(grid_frame, width=4, height=2, bg="white", fg="black")
            button.grid(row=y, column=x, padx=2, pady=2)  # Place button in the grid
            tiles[x][y] = {
                "id": f"{x}{y}",
                "coords": {"x": x, "y": y},
                "button": button,
            }

size_x = int(input("Enter the number of columns: "))
size_y = int(input("Enter the number of rows: "))
# bomb_numbers = int(input("Enter the number of bombs: "))

root = tk.Tk()

create_button_field(size_x, size_y, root)

root.mainloop()