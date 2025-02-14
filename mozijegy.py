import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import mysql.connector

# MySQL kapcsolat beállítása
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Ha van jelszavad, írd be ide
    password="",
    database="mozijegy"
)

cursor = db.cursor()

# Ablak létrehozása
root = ttk.Window(themename="superhero")
root.title("Mozi Jegyfoglalás")
root.geometry("500x400")

# Információs címke
info_label = ttk.Label(root, text="Jelenleg játszó filmeink!", font=("Arial", 12))
info_label.pack(pady=10)

# Jegyfoglalás funkció
def book_ticket(movie_title):
    """Jegyfoglalás adatbázisba mentése"""
    terem_szam = 1  # Példa teremszám, ezt dinamikusan is be lehet állítani
    szek_szam = 5   # Példa szék szám
    keresztnev = entry_firstname.get()
    vezeteknev = entry_lastname.get()
    
    if keresztnev and vezeteknev:
        try:
            cursor.execute(
                "INSERT INTO foglalások (Sorszam, Keresztnev, Vezeteknev, Terem_szam, Szekszam) VALUES (%s, %s, %s, %s, %s)",
                (None, keresztnev, vezeteknev, terem_szam, szek_szam)
            )
            db.commit()
            status_label.config(text="Foglalás sikeres!", bootstyle="success")
        except mysql.connector.Error as err:
            status_label.config(text=f"Hiba: {err}", bootstyle="danger")
    else:
        status_label.config(text="Töltsd ki az adatokat!", bootstyle="warning")

# Jegyfoglalás ablak megnyitása
def open_booking_window(movie_title):
    global entry_firstname, entry_lastname, status_label

    booking_window = tk.Toplevel(root)
    booking_window.title("Jegyfoglalás")
    booking_window.geometry("300x250")
    
    ttk.Label(booking_window, text=f"Jegyfoglalás: {movie_title}", font=("Arial", 12)).pack(pady=10)
    
    ttk.Label(booking_window, text="Keresztnév:").pack()
    entry_firstname = ttk.Entry(booking_window)
    entry_firstname.pack(pady=5)
    
    ttk.Label(booking_window, text="Vezetéknév:").pack()
    entry_lastname = ttk.Entry(booking_window)
    entry_lastname.pack(pady=5)
    
    status_label = ttk.Label(booking_window, text="", font=("Arial", 10))
    status_label.pack(pady=5)
    
    ttk.Button(booking_window, text="Foglalás", bootstyle="success", command=lambda: book_ticket(movie_title)).pack(pady=10)

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
frame = ttk.Frame(root)
frame.pack()

buttons = []
columns = 3

for i, (path, description) in enumerate(image_data):
    try:
        img = load_image(path)
        button = ttk.Button(frame, image=img, bootstyle="light", command=lambda desc=description: show_info(desc))
        button.image = img  # Referencia megtartása
        button.grid(row=i // columns, column=i % columns, padx=10, pady=10)
        buttons.append(button)
    except Exception as e:
        print(f"Hiba a kép betöltésekor: {e}")

# Jegyfoglalás gomb létrehozása (kezdetben elrejtve)
book_button = ttk.Button(root, text="Foglalj jegyet", bootstyle="primary")

# A fő ciklus indítása
root.mainloop()
