import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import sqlite3
import uuid

# Adatbázis összekapcsolása
conn = sqlite3.connect("mozijegy.db")
cursor = conn.cursor()

# Ablak létrehozása
root = ttk.Window(themename="superhero")
root.title("Mozi Jegyfoglalás")
root.geometry("500x400")

info_label = ttk.Label(root, text="Jelenleg játszott filmeink!", font=("Arial", 12))
info_label.pack(pady=10)

def generate_ticket(movie_title, keresztnev, vezeteknev, email):
    try:
        pdf = FPDF("L", "mm", (90, 50))  # Vízszintes, mozijegy méret
        pdf.add_page()
        pdf.set_auto_page_break(auto=False)

        # Keret
        pdf.set_line_width(0.4)
        pdf.rect(2, 2, 86, 46)

        # Fejléc / cím
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 10, "🎬 MoziJegy", ln=True, align="C")

        # Vonal
        pdf.set_draw_color(100, 100, 100)
        pdf.line(5, 14, 85, 14)

        # Film és név adatok
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        pdf.cell(0, 6, f"🎞️  Film: {movie_title}", ln=True)
        pdf.cell(0, 6, f"👤 Név: {keresztnev} {vezeteknev}", ln=True)
        pdf.cell(0, 6, f"📧 Email: {email}", ln=True)

        # Jegy sorszáma
        jegy_id = str(uuid.uuid4())[:8]
        pdf.cell(0, 6, f"🎟️  Jegyazonosító: {jegy_id}", ln=True)

        # Dátum, terem, szék - ide lehet fejleszteni, ha vannak ezek
        pdf.cell(0, 6, "🕒 Dátum: 2025.05.23", ln=True)
        pdf.cell(0, 6, "🪑 Terem: Automatikus", ln=True)

        # Alsó szürke sáv (pl. vágás vagy vonalkód hely)
        pdf.set_fill_color(220, 220, 220)
        pdf.rect(2, 42, 86, 6, style="F")

        # Logo opcionálisan
        try:
            pdf.image("logo.png", x=70, y=3, w=15)
        except Exception as e:
            print("Nem sikerült betölteni a logót:", e)

        pdf_filename = "mozi_jegy.pdf"
        pdf.output(pdf_filename)

        send_email(email, pdf_filename)

    except Exception as e:
        print("Hiba a PDF generálása közben:", e)


def send_email(email, pdf_filename):
    msg = EmailMessage()
    msg["Subject"] = "Mozi Jegy Foglalás"
    msg["From"] = "11c-banko@ipari.vein.hu"
    msg["To"] = email
    msg.set_content("Kedves Néző! Csatoltan küldjük a mozijegyét.")

    with open(pdf_filename, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename="mozi_jegy.pdf")

    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login("11c-banko@ipari.vein.hu", "jbmn kjdp fuer uibh")
        smtp.send_message(msg)
        smtp.quit()
    except Exception as e:
        print("Hiba az email küldésekor:", e)

def open_seat_selection(movie_title, keresztnev, vezeteknev, email):
    seat_window = tk.Toplevel(root)
    seat_window.title("Válassz ülőhelyet")
    seat_window.geometry("600x500")

    ttk.Label(seat_window, text=f"Válassz helyet a(z) {movie_title} filmhez!", font=("Arial", 12)).pack(pady=10)

    seat_frame = ttk.Frame(seat_window)
    seat_frame.pack(padx=20, pady=10)

    FREE = "success"
    TAKEN = "secondary"
    SELECTED = "warning"

    cursor.execute("SELECT Terem_szam, Terem_kapacitas FROM termek WHERE Film_cime = ?", (movie_title,))
    result = cursor.fetchone()
    if not result:
        print("Nincs ilyen film az adatbázisban.")
        seat_window.destroy()
        return

    terem_szam, kapacitas = result
    rows, cols = 9, 12

    seat_buttons = []

    cursor.execute("SELECT Szekszam FROM foglalások WHERE Terem_szam = ?", (terem_szam,))
    taken_seats = [row[0] for row in cursor.fetchall()]

    def toggle_seat(r, c):
        seat = seat_buttons[r][c]
        if seat['selected']:
            seat['button'].config(bootstyle=FREE)
            seat['selected'] = False
        else:
            seat['button'].config(bootstyle=SELECTED)
            seat['selected'] = True

    for r in range(rows):
        row_buttons = []
        for c in range(cols):
            szekszam = r * cols + c + 1
            style = TAKEN if szekszam in taken_seats else FREE
            btn = ttk.Button(seat_frame, text=f"{r+1}-{c+1}", width=4, bootstyle=style)
            btn.grid(row=r, column=c, padx=2, pady=2)

            btn.config(command=lambda r=r, c=c: toggle_seat(r, c))

            row_buttons.append({'button': btn, 'selected': False})
        seat_buttons.append(row_buttons)

    def confirm_booking():
        success = False

        for r in range(rows):
            for c in range(cols):
                seat = seat_buttons[r][c]
                if seat['selected']:
                    szek_szam = r * cols + c + 1
                    sorszam = str(uuid.uuid4())[:8] 

                    try:
                        cursor.execute("""
                            INSERT INTO foglalások (Sorszam, Keresztnev, Vezeteknev, Terem_szam, Szekszam)
                            VALUES (?, ?, ?, ?, ?)
                        """, (sorszam, keresztnev, vezeteknev, terem_szam, szek_szam))
                        conn.commit()
                        success = True
                    except sqlite3.IntegrityError as e:
                        print(f"Hely {szek_szam} már foglalt, kihagyva.")
                    except Exception as e:
                        print("Foglalás hiba:", e)

        if success:
            generate_ticket(movie_title, keresztnev, vezeteknev, email)
            seat_window.destroy()
        else:
            print("Nem történt foglalás.")

    ttk.Button(seat_window, text="Foglalás megerősítése", bootstyle="primary", command=confirm_booking).pack(pady=10)

def open_booking_window(movie_title):
    booking_window = tk.Toplevel(root)
    booking_window.title("Jegyfoglalás")
    booking_window.geometry("300x300")
    
    ttk.Label(booking_window, text=f"Jegyfoglalás: {movie_title}", font=("Arial", 12)).pack(pady=10)
    
    ttk.Label(booking_window, text="Keresztnév:").pack()
    entry_firstname = ttk.Entry(booking_window)
    entry_firstname.pack(pady=5)
    
    ttk.Label(booking_window, text="Vezetéknév:").pack()
    entry_lastname = ttk.Entry(booking_window)
    entry_lastname.pack(pady=5)
    
    ttk.Label(booking_window, text="Email cím:").pack()
    entry_email = ttk.Entry(booking_window)
    entry_email.pack(pady=5)
    
    status_label = ttk.Label(booking_window, text="", font=("Arial", 10))
    status_label.pack(pady=5)
    
    def validate_and_open_seats():
        keresztnev = entry_firstname.get()
        vezeteknev = entry_lastname.get()
        email = entry_email.get()
        
        if keresztnev and vezeteknev and email:
            booking_window.destroy()
            open_seat_selection(movie_title, keresztnev, vezeteknev, email)
        else:
            status_label.config(text="Töltsd ki az összes mezőt!", bootstyle="warning")
    
    ttk.Button(booking_window, text="Foglalás", bootstyle="success", command=validate_and_open_seats).pack(pady=10)

def show_info(text):
    info_label.config(text=text)
    book_button.pack(pady=10)
    book_button.config(command=lambda: open_booking_window(text))

def load_image(path, size=(160, 240)):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

image_data = [
    ("rocky_film.jpg", "Rocky - Egy legendás sportfilm"),
    ("badboys.png", "Bad Boys - Akció és humor egyben"),
    ("uvegtigris.jpg", "Üvegtigris - Magyar vígjáték klasszikus"),
    ("kabitoigazsag.jpeg", "Kábító igazság - Valós történeten alapul"),
    ("rush.jpg", "Rush - Forma 1 és rivalizálás"),
    ("it.png", "Az - Stephen King horror remekműve")
]

frame = ttk.Frame(root)
frame.pack()

buttons = []
columns = 3

for i, (path, description) in enumerate(image_data):
    try:
        img = load_image(path)
        button = ttk.Button(frame, image=img, bootstyle="light", command=lambda desc=description: show_info(desc))
        button.image = img
        button.grid(row=i // columns, column=i % columns, padx=10, pady=10)
        buttons.append(button)
    except Exception as e:
        print(f"Hiba a kép betöltésekor: {e}")

book_button = ttk.Button(root, text="Foglalj jegyet", bootstyle="primary")
root.mainloop()
