import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

# Ablak létrehozása
root = ttk.Window(themename="superhero")
root.title("Mozi Jegyfoglalás")
root.geometry("500x400")

info_label = ttk.Label(root, text="Jelenleg játszó filmeink!", font=("Arial", 12))
info_label.pack(pady=10)

def generate_ticket(movie_title, keresztnev, vezeteknev, email):
    """Létrehoz egy PDF mozijegyet."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "MoziJegy", ln=True, align="C")
    pdf.image("logo.png", x=80, y=20, w=50)
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Film: {movie_title}", ln=True, align="L")
    pdf.cell(200, 10, f"Név: {keresztnev} {vezeteknev}", ln=True, align="L")
    pdf.cell(200, 10, f"Email: {email}", ln=True, align="L")
    
    # Mentés
    pdf_filename = "mozi_jegy.pdf"
    pdf.output(pdf_filename)
    
    # Küldés emailben
    send_email(email, pdf_filename)

def send_email(email, pdf_filename):
    """Email küldése a felhasználónak a PDF jeggyel."""
    msg = EmailMessage()
    msg["Subject"] = "Mozi Jegy Foglalás"
    msg["From"] = "11c-banko@ipari.vein.hu"
    msg["To"] = email
    msg.set_content("Kedves Néző! Csatoltan küldjük a mozijegyét.")

    with open(pdf_filename, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename="mozi_jegy.pdf")

    # SMTP kapcsolat (pl. Gmail SMTP szerver)
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
    seat_window.geometry("550x500")
    
    ttk.Label(seat_window, text=f"Válassz helyet a(z) {movie_title} filmhez!", font=("Arial", 12)).pack(pady=10)
    
    seat_frame = ttk.Frame(seat_window)
    seat_frame.pack(padx=20, pady=10)
    
    FREE = "success"
    TAKEN = "secondary"
    SELECTED = "warning"
    
    rows, cols = 9, 12
    seat_buttons = []

    def toggle_seat(row, col):
        button = seat_buttons[row][col]
        if button['bootstyle'] == FREE:
            button.config(bootstyle=SELECTED)
        elif button['bootstyle'] == SELECTED:
            button.config(bootstyle=FREE)

    for r in range(rows):
        row_buttons = []
        for c in range(cols):
            state = FREE
            btn = ttk.Button(seat_frame, text=f"{r+1}-{c+1}", width=4, bootstyle=state,
                             command=lambda r=r, c=c: toggle_seat(r, c))
            btn.grid(row=r, column=c, padx=2, pady=2)
            row_buttons.append(btn)
        seat_buttons.append(row_buttons)

    def confirm_booking():
        generate_ticket(movie_title, keresztnev, vezeteknev, email)
        seat_window.destroy()
    
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
