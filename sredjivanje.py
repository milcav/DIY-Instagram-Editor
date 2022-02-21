import tkinter as tk
from tkinter import filedialog
from rotacija import rotacija_prozor
from menjanje_boje import menjanje_boje_prozor
from izostravanje import izostravanje_prozor
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np

class sredjivanje(tk.Toplevel):
    def __init__(self, master = None):
        tk.Toplevel.__init__(self, master = master)
# =============================================================================
#         Definisanje,bajndovanje i pakovanje dugmadi
# =============================================================================
        self.rotacija = tk.Button(self, text="Rotacija i to")
        self.menjanje_boje = tk.Button(self, text = "Osvetljenje, kontrast, toplina and saturation")
        self.izostravanje = tk.Button(self, text = "Izostravanje i vinjeta")
        self.sacuvaj = tk.Button(self, text = "Sacuvaj kao:")
        self.histogrami = tk.Button(self, text = "Histogrami")
        self.original = tk.Button(self, text = "Vrati original")
        
        self.rotacija.bind("<ButtonRelease>", self.rotacija_klik)
        self.menjanje_boje.bind("<ButtonRelease>", self.menjanje_boje_klik)
        self.izostravanje.bind("<ButtonRelease>", self.izostravanje_klik)
        self.sacuvaj.bind("<ButtonRelease>", self.sacuvaj_klik)
        self.histogrami.bind("<ButtonRelease>", self.histogrami_klik)
        self.original.bind("<ButtonRelease>", self.original_klik)
        
        self.rotacija.grid(row = 0, column = 0)
        self.menjanje_boje.grid(row = 1, column = 0)
        self.izostravanje.grid(row = 2, column = 0)
        self.sacuvaj.grid(row = 3, column = 0)
        self.histogrami.grid(row = 4, column = 0)
        self.original.grid(row = 5, column = 0)
        
        
    def rotacija_klik(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.rotacija:
            self.master.rotacija_prozor = rotacija_prozor(master = self.master)
            self.master.rotacija_prozor.grab_set()

    def menjanje_boje_klik(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.menjanje_boje:
            self.master.menjanje_boje_prozor = menjanje_boje_prozor(master = self.master)
            self.master.menjanje_boje_prozor.grab_set()
    
    def izostravanje_klik(self,event):
        if self.winfo_containing(event.x_root, event.y_root) == self.izostravanje:
            self.master.izostravanje_prozor = izostravanje_prozor(master = self.master)
            self.master.izostravanje_prozor.grab_set()
            
    def sacuvaj_klik(self,event):
        if self.winfo_containing(event.x_root, event.y_root) == self.sacuvaj:
            originalni_tip = self.master.filename.split('.')[-1]
            filename = filedialog.asksaveasfilename()
            filename = filename + "." + originalni_tip
            
            sacuvana_slika = self.master.sredjena_slika
            sacuvana_slika.save(filename)
            self.master.filename = filename
            
    def histogrami_klik(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.histogrami:
            #plt.close("all")
            slika = np.array(self.master.sredjena_slika)
            print(slika.shape)
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
            ax1.hist(slika[:,:,0].ravel(),256,[0,256], color = 'r')
            ax2.hist(slika[:,:,1].ravel(),256,[0,256], color = 'g')
            ax3.hist(slika[:,:,2].ravel(),256,[0,256], color = 'b')
            ax4.hist((slika.sum(axis=-1)/3).ravel(),256,[0,256], color = 'k')
            plt.show()
            
    def original_klik(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.original:
            self.master.sredjena_slika = self.master.prava_slika
            self.master.platno.prikaz_slike()
            
            
            
            
            
            
            