import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

# Ablak létrehozása
root = ttk.Window(themename="superhero")
root.title("Bootstrap GUI")
root.geometry("500x400")

# Információs címke
info_label = ttk.Label(root, text="Jelenleg játszó filmeink!", font=("Arial", 12))
info_label.pack(pady=10)

# Jegyfoglalás ablak megnyitása
def open_booking_window(movie_title):
    booking_window = tk.Toplevel(root)
    booking_window.title("Jegyfoglalás")
    booking_window.geometry("300x200")
    
    ttk.Label(booking_window, text=f"Jegyfoglalás: {movie_title}", font=("Arial", 12)).pack(pady=10)
    
    ttk.Label(booking_window, text="Hány jegyet szeretne foglalni:").pack()
    ticket_entry = ttk.Entry(booking_window)
    ticket_entry.pack(pady=5)
    
    ttk.Button(booking_window, text="Foglalás", bootstyle="success").pack(pady=10)

# Gombokra kattintáskor megjelenő szöveg és jegyfoglaló gomb létrehozása
def show_info(text):
    info_label.config(text=text)
    book_button.pack(pady=10)
    book_button.config(command=lambda: open_booking_window(text))

# Képek betöltése és átméretezése
def load_image(path, size=(160, 240)):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Képek listája és hozzájuk tartozó leírások
image_data = [
    ("rocky_film.jpg", "Rocky - Egy legendás sportfilm"),
    ("badboys.png", "Bad Boys - Akció és humor egyben"),
    ("uvegtigris.jpg", "Üvegtigris - Magyar vígjáték klasszikus"),
    ("kabitoigazsag.jpeg", "Kábító igazság - Valós történeten alapul"),
    ("rush.jpg", "Rush - Forma 1 és rivalizálás"),
    ("it.png", "Az - Stephen King horror remekműve")
]

# Gombok létrehozása
grid_rows = 2
columns = 3
frame = ttk.Frame(root)
frame.pack()

buttons = []
for i, (path, description) in enumerate(image_data):
    try:
        img = load_image(path)
        button = ttk.Button(frame, image=img, bootstyle="light", command=lambda desc=description: show_info(desc))
        button.image = img  # Referencia megtartása
        button.grid(row=i//columns, column=i%columns, padx=10, pady=10)
        buttons.append(button)
    except Exception as e:
        print(f"Hiba a kép betöltésekor: {e}")

# Jegyfoglalás gomb létrehozása (kezdetben elrejtve)
book_button = ttk.Button(root, text="Foglalj jegyet", bootstyle="primary")

# A fő ciklus indítása
root.mainloop()
