import tkinter as tk
from PIL import  ImageTk

class platno(tk.Canvas):
    def __init__(self, master = None):
        tk.Canvas.__init__(self, master=master, bg = "gray", width = 400, height = 600)
        
        self.slika_koja_se_prikazuje = None

    def prikaz_slike(self, slika= None):
# =============================================================================
#         Pre prikazivanja brise staro platno, ako se ne prosledi slika
#         koristi obradjivanu sliku
# =============================================================================
        self.ocisti_platno()
        if slika is None:
            slika = self.master.sredjena_slika.copy()
        else:
            slika=slika
            
        sirina, visina = slika.size
        self.slika_koja_se_prikazuje = ImageTk.PhotoImage(slika)

        
        self.config(width = sirina, height = visina)
        self.create_image(sirina / 2, visina / 2, anchor= tk.CENTER, image = self.slika_koja_se_prikazuje)
        self.image = self.slika_koja_se_prikazuje
    def ocisti_platno(self):
        self.delete("all")