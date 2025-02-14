import tkinter as tk
import ttkbootstrap as ttk
# Ablak létrehozása
root = ttk.Window(themename="superhero")  # Használhatsz más témákat is, mint 'flatly', 'darkly', 'cerulean' stb.
root.title("Bootstrap GUI")
root.geometry("400x300")

# Egy gomb létrehozása
button = ttk.Button(root, text="Kattints rám!", bootstyle="primary")
button.pack(pady=20)

# A fő ciklus indítása
root.mainloop()