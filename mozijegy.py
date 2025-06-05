# Frissített teljes kód Cinema City-stílusú jeggyel, árakkal és törlés funkcióval

import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import sqlite3
import uuid
from tkinter import messagebox

# Adatbázis csatlakozás
conn = sqlite3.connect("mozijegy.db")
cursor = conn.cursor()

# Jegyárak
PRICES = {
    "Felnőtt": 3500,
    "Gyerek": 2800,
    "Nyugdíjas": 2900
}

# Ablak
root = ttk.Window(themename="superhero")
root.title("Mozi Jegyfoglalás")
root.geometry("500x500")

info_label = ttk.Label(root, text="Jelenleg játszott filmeink!", font=("Arial", 12))
info_label.pack(pady=10)

# PDF generálás Cinema City stílusban
def generate_ticket(movie_title, keresztnev, vezeteknev, email, seats, ticket_type, quantity, price_per_ticket):
    from fpdf import FPDF
    import uuid

    try:
        pdf = FPDF("P", "mm", (100, 140))
        pdf.add_page()
        pdf.set_auto_page_break(auto=False)

        # Keret
        pdf.set_line_width(0.4)
        pdf.rect(5, 5, 90, 130)

        # Fejléc
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "CINEMA CITY", ln=True, align="C")

        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Előadás: {movie_title}", ln=True, align="C")
        pdf.cell(0, 6, f"Név: {keresztnev} {vezeteknev}", ln=True, align="C")
        pdf.cell(0, 6, f"Email: {email}", ln=True, align="C")
        pdf.cell(0, 6, f"Jegytípus: {ticket_type}", ln=True, align="C")
        pdf.cell(0, 6, f"Darabszám: {quantity}", ln=True, align="C")
        pdf.cell(0, 6, f"Ár: {price_per_ticket * quantity} Ft", ln=True, align="C")
        pdf.ln(5)

        for szek in seats:
            pdf.cell(0, 5, f"Szék: {szek}", ln=True, align="C")

        jegy_id = str(uuid.uuid4())[:8]
        pdf.ln(5)
        pdf.cell(0, 6, f"Jegyazonosító: {jegy_id}", ln=True, align="C")

        pdf_filename = f"mozijegy_{jegy_id}.pdf"
        pdf.output(pdf_filename)

        send_email(email, pdf_filename)
        return pdf_filename

    except Exception as e:
        print("Hiba a PDF készítésnél:", e)
        return None

# Email küldés

def send_email(email, pdf_filename=None, subject="Mozi Jegy", msg_body="Köszönjük, hogy nálunk foglalt! Csatoltan a jegyed."):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "11c-banko@ipari.vein.hu"
    msg["To"] = email
    msg.set_content(msg_body)

    try:
        if pdf_filename:
            with open(pdf_filename, "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_filename)

        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login("11c-banko@ipari.vein.hu", "jbmn kjdp fuer uibh")
        smtp.send_message(msg)
        smtp.quit()

    except Exception as e:
        print("Hiba az email küldésénél:", e)
# Foglalás törlés

def torles_ablak():
    win = tk.Toplevel(root)
    win.title("Foglalás törlése")
    win.geometry("300x150")

    ttk.Label(win, text="Add meg az email címed:").pack(pady=10)
    entry_email = ttk.Entry(win)
    entry_email.pack(pady=5)

    status = ttk.Label(win, text="")
    status.pack(pady=5)

    def torol():
        email = entry_email.get()
        if email:
            cursor.execute("DELETE FROM foglalások WHERE Email = ?", (email,))
            conn.commit()
            send_email(email, subject="Foglalás törölve", msg_body="Foglalása sikeresen törölve lett.")
            status.config(text="Foglalás törölve.", bootstyle="success")
        else:
            status.config(text="Adj meg email címet!", bootstyle="danger")

    ttk.Button(win, text="Törlés", bootstyle="danger", command=torol).pack(pady=10)

# Foglalási ablak jegytípus és darab választással

def open_booking_window(movie_title):
    booking_window = tk.Toplevel(root)
    booking_window.title("Jegyfoglalás")
    booking_window.geometry("350x400")

    ttk.Label(booking_window, text=f"Foglalás a(z) {movie_title} filmre", font=("Arial", 12)).pack(pady=10)

    ttk.Label(booking_window, text="Keresztnév:").pack()
    entry_firstname = ttk.Entry(booking_window)
    entry_firstname.pack()

    ttk.Label(booking_window, text="Vezetéknév:").pack()
    entry_lastname = ttk.Entry(booking_window)
    entry_lastname.pack()

    ttk.Label(booking_window, text="Email:").pack()
    entry_email = ttk.Entry(booking_window)
    entry_email.pack()

    ttk.Label(booking_window, text="Jegytípus:").pack()
    ticket_type_var = tk.StringVar()
    ticket_type_dropdown = ttk.Combobox(booking_window, textvariable=ticket_type_var, values=["Felnőtt", "Gyerek", "Nyugdíjas"])
    ticket_type_dropdown.pack()

    ttk.Label(booking_window, text="Darabszám:").pack()
    quantity_spinbox = ttk.Spinbox(booking_window, from_=1, to=10)
    quantity_spinbox.pack()

 

    status_label = ttk.Label(booking_window, text="", font=("Arial", 10))
    status_label.pack(pady=5)

    def proceed_to_seat_selection():
        keresztnev = entry_firstname.get()
        vezeteknev = entry_lastname.get()
        email = entry_email.get()
        ticket_type = ticket_type_var.get()
        quantity = int(quantity_spinbox.get())

        if not (keresztnev and vezeteknev and email and ticket_type):
            status_label.config(text="Minden mezőt tölts ki!", bootstyle="warning")
            return

        price_dict = {"Felnőtt": 3500, "Gyerek": 2800, "Nyugdíjas": 2900}
        price_per_ticket = price_dict.get(ticket_type, 3500)

        booking_window.destroy()
        open_seat_selection(movie_title, keresztnev, vezeteknev, email, ticket_type, quantity, price_per_ticket)

    ttk.Button(booking_window, text="Tovább a helyfoglaláshoz", command=proceed_to_seat_selection, bootstyle="success").pack(pady=10)

def open_seat_selection(movie_title, keresztnev, vezeteknev, email, ticket_type, quantity, price_per_ticket):
    seat_window = tk.Toplevel(root)
    seat_window.title("Helyválasztás")
    seat_window.geometry("600x500")

    ttk.Label(seat_window, text=f"Helyválasztás - {movie_title}", font=("Arial", 12)).pack(pady=10)

    seat_frame = ttk.Frame(seat_window)
    seat_frame.pack()

    rows, cols = 9, 12
    seat_buttons = []

    cursor.execute("SELECT Terem_szam FROM termek WHERE Film_cime = ?", (movie_title,))
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Hiba", "Nincs ilyen filmhez terem.")
        seat_window.destroy()
        return

    terem_szam = result[0]
    cursor.execute("SELECT Szekszam FROM foglalások WHERE Terem_szam = ?", (terem_szam,))
    taken_seats = [row[0] for row in cursor.fetchall()]

    selected_seats = []

    def toggle_seat(r, c):
        szekszam = r * cols + c + 1
        btn = seat_buttons[r][c]
        if btn['selected']:
            btn['button'].config(bootstyle="success")
            btn['selected'] = False
            selected_seats.remove(szekszam)
        else:
            if len(selected_seats) < quantity:
                btn['button'].config(bootstyle="warning")
                btn['selected'] = True
                selected_seats.append(szekszam)

    for r in range(rows):
        row = []
        for c in range(cols):
            szekszam = r * cols + c + 1
            style = "secondary" if szekszam in taken_seats else "success"
            btn = ttk.Button(seat_frame, text=f"{r+1}-{c+1}", width=4, bootstyle=style)
            btn.grid(row=r, column=c, padx=1, pady=1)

            btn.config(command=lambda r=r, c=c: toggle_seat(r, c))
            row.append({'button': btn, 'selected': False})
        seat_buttons.append(row)

    def confirm_booking():
        if len(selected_seats) != quantity:
            messagebox.showwarning("Hibás foglalás", f"{quantity} szék szükséges!")
            return

        sorszam = str(uuid.uuid4())[:8]

        for szek in selected_seats:
            cursor.execute("""
                INSERT INTO foglalások (Sorszam, Keresztnev, Vezeteknev, Email, Terem_szam, Szekszam)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (sorszam, keresztnev, vezeteknev, email, terem_szam, szek))
        conn.commit()

        pdf_file = generate_ticket(movie_title, keresztnev, vezeteknev, email, selected_seats, ticket_type, quantity, price_per_ticket)
        if pdf_file:
            messagebox.showinfo("Sikeres foglalás", "A jegy elkészült és emailben elküldtük.")
        else:
            messagebox.showerror(" Hiba", "Nem sikerült létrehozni a jegyet.")

        
        seat_window.destroy()

    
    ttk.Button(seat_window, text="Foglalás véglegesítése", command=confirm_booking, bootstyle="primary").pack(pady=10)

    



# Film betöltés

def show_info(text):
    info_label.config(text=text)
    book_button.config(command=lambda: open_booking_window(text))
    book_button.pack(pady=10)


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
        print(f"Kép betöltési hiba: {e}")

book_button = ttk.Button(root, text="Foglalj jegyet", bootstyle="primary")
book_button.pack_forget()
tt_del = ttk.Button(root, text="Foglalás törlése", bootstyle="danger", command=torles_ablak)
tt_del.pack(pady=10)


root.mainloop()
