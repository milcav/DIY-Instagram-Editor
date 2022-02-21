import tkinter as tk
from PIL import Image
import numpy as np
import konverter as k



class menjanje_boje_prozor(tk.Toplevel):
    
    def __init__(self, master = None):
        tk.Toplevel.__init__(self, master = master)
# =============================================================================
#         Pakovanje skala, i etiketa
# =============================================================================
        
        self.prava_slika = self.master.sredjena_slika
        self.sredjena_slika = self.master.sredjena_slika
        
        self.osvetljenje_label = tk.Label(self, text = "Osvetljenje")
        self.osvetljenje_scale = tk.Scale(self, from_ = 0, to_= 3, length = 250, resolution = 0.01, orient = tk.HORIZONTAL)
        self.osvetljenje_scale.set(1)
        
        self.kontrast_label = tk.Label(self, text="Kontrast")
        self.kontrast_scale = tk.Scale(self, from_ = -50, to_ = 50, length = 250, resolution = 1, orient = tk.HORIZONTAL)
        self.kontrast_scale.set(0)
        
        self.toplina_label = tk.Label(self, text = "Toplina")
        self.toplina_scale = tk.Scale(self, from_ = -50, to_ = 50, length = 250, resolution = 1, orient = tk.HORIZONTAL)
        
        self.zasicenje_label = tk.Label(self, text = "Zasicenje")
        self.zasicenje_scale = tk.Scale(self, from_ = 0, to_ = 3, length = 250, resolution = 0.01, orient = tk.HORIZONTAL)
        self.zasicenje_scale.set(1)
        
        self.akcenat_label = tk.Label(self, text = "Akcenat")
        self.akcenat_scale = tk.Scale(self, from_ = -50, to_ = 50, length = 250, resolution = 1, orient = tk.HORIZONTAL)
        
        self.senka_label = tk.Label(self, text = "Senka")
        self.senka_scale = tk.Scale(self, from_ = -50, to_ = 50, length = 250, resolution = 1, orient = tk.HORIZONTAL)
        
        self.primeni_button = tk.Button(self, text = "Primeni")
        self.vidi_button = tk.Button(self, text = "Vidi")
        self.odustani_button = tk.Button(self, text = "Odustani")
        
        self.primeni_button.bind("<ButtonRelease>", self.primeni_promene)
        self.vidi_button.bind("<ButtonRelease>", self.vidi_promene)
        self.odustani_button.bind("<ButtonRelease>", self.odustani_promene)
        
        self.osvetljenje_label.pack()
        self.osvetljenje_scale.pack()
        self.kontrast_label.pack()
        self.kontrast_scale.pack()
        self.toplina_label.pack()
        self.toplina_scale.pack()
        self.zasicenje_label.pack()
        self.zasicenje_scale.pack()
        self.akcenat_label.pack()
        self.akcenat_scale.pack()
        self.senka_label.pack()
        self.senka_scale.pack()
        self.primeni_button.pack(side = tk.LEFT)
        self.vidi_button.pack(side = tk.LEFT)
        self.odustani_button.pack()
    
    def primeni_promene(self, event):
        self.vidi_promene(event)
        self.master.sredjena_slika = self.sredjena_slika
        self.close()
    
    def vidi_promene(self, event):
        self.sredjena_slika = self.master.sredjena_slika
        self.sredjena_slika = self.osv_i_zas(self.osvetljenje_scale.get(),self.zasicenje_scale.get(), self.sredjena_slika)
        #self.sredjena_slika = self.kontrast(self.kontrast_scale.get(), self.sredjena_slika)
        self.sredjena_slika = self.akc_i_sen(self.kontrast_scale.get(), -self.kontrast_scale.get(), self.sredjena_slika)
        self.sredjena_slika = self.toplina(self.toplina_scale.get(), self.sredjena_slika)
        self.sredjena_slika = self.akc_i_sen(self.akcenat_scale.get(),self.senka_scale.get(), self.sredjena_slika)
        self.prikaz_slike(self.sredjena_slika)
    
    def odustani_promene(self, event):
        self.close()
    
    def prikaz_slike(self, slika = None):
        self.master.platno.prikaz_slike(slika=slika)
    
    def close(self):
        self.prikaz_slike(self.master.sredjena_slika)
        self.destroy()
    
    def osv_i_zas(self, alpha, beta, slika):
        '''
        Prebacuje RGB vrednosti u HSV i povecava V alpha puta i S parametar
        beta puta

        Parameters
        ----------
        alpha : float
            koef osvetljenja
        beta : float
            koef zasicenja
        slika : PIL.Image
            slika koju obradjujemo

        Returns
        -------
            PIL.Image
                sredjena slika

        '''
        slika = np.float64(np.array(slika))
        slika = k.RGBtoHSV(slika)
        slika[:,:, 2] *= alpha
        slika[:,:, 2] = np.where(slika[:,:, 2]>1, 1, slika[:,:,2])
        slika[:,:, 2] = np.where(slika[:,:, 2]<0, 0, slika[:,:,2])
        slika[:,:, 1] *= beta
        slika[:,:, 1] = np.where(slika[:,:, 1]>1, 1, slika[:,:,1])
        slika[:,:, 1] = np.where(slika[:,:, 1]<0, 0, slika[:,:,1])
        slika = k.HSVtoRGB(slika)
        slika = np.uint8(slika)
        return Image.fromarray(slika)
    
    def toplina(self, value, slika):
        '''
        

        Parameters
        ----------
        value : int
             vrednost za koju menjamo toplinu
        slika : PIL.Image
            slika koja se sredjuje

        Returns
        -------
        PIL.Image
            sredjena slika

        '''
        if value == 0:
            return slika
        slika = np.int16(np.array(slika))
        slika[:,:,0] = slika[:, :, 0] + value
        slika[:,:,2] = slika[:, :, 2] - value
        slika = np.where(slika<255, slika, 255)
        slika = np.where(slika>0, slika, 0)
        slika = np.uint8(slika)
        return Image.fromarray(slika)
    
    
    def akc_i_sen(self, alpha, beta, slika):
        '''
        Menja akcente i senke u odnosu na osvetnjenje, svetlije menja vise kad
        menja akcenat, tamnije menja vise kad menja senke

        Parameters
        ----------
        alpha : float
            koeficijent menjanja akcenta
        beta : float
            koeficijent menjanja senki
        slika : PIL.Image
            slika koja se sredjuje 

        Returns
        -------
        PIL.Image
            sredjena slika

        '''
        slika = np.float64(np.array(slika))
        slika = k.RGBtoHSV(slika)
        slika[:,:, 2] = np.where(slika[:,:,2]>0.3, slika[:,:, 2]*(1+slika[:,:, 2]*alpha/100.0), slika[:,:,2])           
        slika[:,:, 2] = np.where(slika[:,:,2]<0.7,
                                 slika[:,:, 2]*(1+(1-slika[:,:, 2])*beta/100.0),
                                 slika[:,:,2])
        slika[:,:, 2] = np.where(slika[:,:, 2]>1, 1, slika[:,:,2])
        slika[:,:, 2] = np.where(slika[:,:, 2]<0, 0, slika[:,:,2])
        slika = k.HSVtoRGB(slika)
        slika = np.uint8(slika)
        return Image.fromarray(slika)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        