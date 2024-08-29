from tab1 import create_tab1
from tab2 import create_tab2

import tkinter as tk
from tkinter import *
from tkinter import ttk

def create_gui():
    background_color = "#F1F6F5"
    root = tk.Tk()
    icon = tk.PhotoImage(file="Seed_Recovery-main/seed_recovery.png")
    root.iconphoto(False, icon)
    root.title("Seed Phrase Recovery")
    root.geometry("1000x580")
    root.config(bg=background_color)

    style = ttk.Style()
    style.configure("TNotebook", background=background_color)
    style.map("TNotebook.Tab", background=[("selected", background_color), ("active", background_color)])

    # Creating Tabs
    notebook = ttk.Notebook(root)
    tab1 = create_tab1(notebook)
    tab2 = create_tab2(notebook)
    notebook.add(tab1, text="Unknown Words", sticky="nsew")
    notebook.add(tab2, text="Knwon Words", sticky="nsew")
    notebook.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
