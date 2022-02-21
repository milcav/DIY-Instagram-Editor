import tkinter as tk
from tkinter import filedialog
from PIL import Image
from sredjivanje import sredjivanje
from prikaz_slike import platno


class Main(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
        
            self.filename = ""
            self.prava_slika = None
            self.sredjena_slika = None
        
            self.title("Instagram za sirotinju")
            logo = tk.PhotoImage(file = 'insta.png')
            self.call('wm', 'iconphoto', self._w, logo)
            
            self.ucitaj = tk.Button(self, text = "Ucitaj novu sliku", padx = 50, pady = 50)
            self.ucitaj.bind("<ButtonRelease>", self.ucitavanje_slike)
            self.ucitaj.pack()
            
        def ucitavanje_slike(self, event):
            global slika
            if self.winfo_containing(event.x_root, event.y_root) == self.ucitaj:
                filename = filedialog.askopenfilename()
                slika = Image.open(filename).convert("RGB")
                if slika is not None:
                    self.filename = filename
                    self.prava_slika = slika
                    self.sredjena_slika = slika
                    self.platno = platno(master = self)
                    self.platno.prikaz_slike()
                    self.platno.pack()
                    self.ucitaj.destroy()
                    self.sredjivanje = sredjivanje(master = self)
                    self.sredjivanje.grab_set()