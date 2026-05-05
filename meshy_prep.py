import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

def process_and_split_image(image_path):
    # Učitavanje slike
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Nije moguće učitati sliku. Proveri putanju.")

    h, w = img.shape[:2]
    mid_x = w // 2

    # Pouzdaniji pristup: Prvo sečemo sliku na levu i desnu polovinu
    halves = [
        ("back", img[:, :mid_x]),
        ("front", img[:, mid_x:])
    ]

    saved_files = []
    base_dir = os.path.dirname(image_path)

    for side, half_img in halves:
        gray = cv2.cvtColor(half_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Umesto fiksnog tresholda, koristimo OTSU koji se sam prilagođava gradijentu
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Čišćenje šuma i kidanje preostalih linija poda
        kernel = np.ones((5, 5), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
        morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel, iterations=3)

        # Nalazimo konture na trenutnoj polovini
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            continue

        # Uzimamo samo najveću konturu (to je naš anđeo/srce)
        largest_contour = max(contours, key=cv2.contourArea)

        x, y, w_c, h_c = cv2.boundingRect(largest_contour)

        # Dodajemo padding oko modela
        pad = 20
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(half_img.shape[1], x + w_c + pad)
        y2 = min(half_img.shape[0], y + h_c + pad)

        crop_bgr = half_img[y1:y2, x1:x2]

        # Kreiranje maske za transparentnost
        mask = np.zeros(crop_bgr.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED, offset=(-x1, -y1))

        # Omekšavanje unutrašnjih crnih linija
        smoothed = cv2.bilateralFilter(crop_bgr, d=9, sigmaColor=75, sigmaSpace=75)

        # Dodavanje Alpha kanala
        b, g, r = cv2.split(smoothed)
        rgba = cv2.merge([b, g, r, mask])

        filename = os.path.join(base_dir, f"meshy_ready_{side}.png")
        cv2.imwrite(filename, rgba)
        saved_files.append(filename)

    if not saved_files:
        raise ValueError("Nije uspela detekcija objekata ni na jednoj polovini. Proveri sliku.")

    return saved_files


class CypherMeshApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CypherMesh Prep")
        self.root.geometry("450x250")
        self.root.resizable(False, False)
        
        # Podesi ikonicu aplikacije ako je imaš (otkomentariši ispod kad dodaš icon.ico)
        # self.root.iconbitmap("icon.ico")

        # Stilizacija
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10)
        style.configure("TLabel", font=("Segoe UI", 12))

        # Glavni kontejner
        frame = ttk.Frame(root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Naslov
        self.title_label = ttk.Label(frame, text="Priprema za Meshy.ai", font=("Segoe UI", 16, "bold"))
        self.title_label.pack(pady=(10, 20))

        # Dugme za učitavanje
        self.btn_load = ttk.Button(frame, text="Učitaj sliku i obradi", command=self.load_and_process)
        self.btn_load.pack(pady=10, fill=tk.X)

        # Status
        self.status_label = ttk.Label(frame, text="Spreman.", foreground="gray")
        self.status_label.pack(pady=10)

    def load_and_process(self):
        filepath = filedialog.askopenfilename(
            title="Izaberi sliku",
            filetypes=[("Slike", "*.png;*.jpg;*.jpeg")]
        )
        if not filepath:
            return
        
        self.status_label.config(text="Obrada u toku...", foreground="#0078D7")
        self.root.update()
        
        try:
            saved_images = process_and_split_image(filepath)
            msg = "Uspešno sačuvano:\n" + "\n".join([os.path.basename(f) for f in saved_images])
            self.status_label.config(text="Završeno!", foreground="green")
            messagebox.showinfo("Uspeh", msg)
        except Exception as e:
            self.status_label.config(text="Greška u obradi.", foreground="red")
            messagebox.showerror("Greška", str(e))

def show_splash_screen():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True) # Uklanja prozorske ivice (X, minimize, maximize)
    
    # Centriranje splash screen-a
    window_width = 400
    window_height = 250
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    splash_root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
    
    splash_root.configure(bg="#212121")

    # Tekst umesto slike na splash-u
    tk.Label(splash_root, text="CypherMesh Prep", font=("Segoe UI", 24, "bold"), fg="white", bg="#212121").pack(expand=True)
    tk.Label(splash_root, text="Učitavanje modula...", font=("Segoe UI", 10), fg="gray", bg="#212121").pack(side=tk.BOTTOM, pady=10)

    def main_window():
        splash_root.destroy() # Zatvara splash
        root = tk.Tk()
        app = CypherMeshApp(root)
        root.mainloop()

    # Prikazuje splash screen na 2 sekunde (2000 ms), a onda pali glavnu aplikaciju
    splash_root.after(2000, main_window)
    splash_root.mainloop()

if __name__ == "__main__":
    show_splash_screen()