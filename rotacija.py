import tkinter as tk
from PIL import Image
import numpy as np
import math as m

class rotacija_prozor(tk.Toplevel):
    
    def __init__(self, master = None):
        tk.Toplevel.__init__(self, master = master)
        
        self.nivo_rotacije = 0
        
        self.prava_slika = self.master.sredjena_slika
        self.sredjena_slika = self.master.sredjena_slika
        
        self.rotacija_label = tk.Label(self, text = "Stepen rotacije [-25,25]")
        self.rotacija_scale = tk.Scale(self, from_ = -25, to_= 25, length = 250, resolution = 1, orient = tk.HORIZONTAL)
        self.zum_label = tk.Label(self, text = "Zumiraj")
        self.zum_scale = tk.Scale(self, from_=1.0, to_=10, length = 250, resolution = 0.01, orient = tk.HORIZONTAL)
        
        self.primeni_button = tk.Button(self, text = "Primeni")
        self.vidi_button = tk.Button(self, text = "Vidi")
        self.odustani_button = tk.Button(self, text = "Odustani")
        
        self.primeni_button.bind("<ButtonRelease>", self.primeni_promene)
        self.vidi_button.bind("<ButtonRelease>", self.vidi_promene)
        self.odustani_button.bind("<ButtonRelease>", self.odustani_promene)
        
        self.rotacija_label.pack()
        self.rotacija_scale.pack()
        self.zum_label.pack()
        self.zum_scale.pack()
        
        self.primeni_button.pack(side = tk.LEFT)
        self.vidi_button.pack(side = tk.LEFT)
        self.odustani_button.pack()
    
    def primeni_promene(self, event):
        self.master.sredjena_slika = self.sredjena_slika
        self.close()
    
    def vidi_promene(self,event):
        self.sredjena_slika = self.master.sredjena_slika
        self.sredjena_slika = self.zumiranje(self.zum_scale.get(), self.sredjena_slika)
        self.sredjena_slika = self.rotacija(self.rotacija_scale.get(), self.sredjena_slika)
        self.prikaz_slike(self.sredjena_slika)
    
    def odustani_promene(self, event):
        self.close()
    
    def prikaz_slike(self, slika = None):
        self.master.platno.prikaz_slike(slika=slika)
    
    def close(self):
        self.prikaz_slike(self.master.sredjena_slika)
        self.destroy()
        
        
        
        
    def zumiranje(self, alpha, slika):
        '''
        Zumiranje slike koriscenjem bilinearne interpolacije
        Parameters
        ----------
        alpha : float
            Od 1 do 10 koeficijent zuma
        slika : PIL.Image
            slika koja se sredjuje

        Returns
        -------
        PIL.Image
            sredjena slika

        '''
        if alpha == 1:
            return slika
        slika = np.int16(np.array(slika))
        sirina = slika.shape[1] - 1
        visina = slika.shape[0] - 1 
        
        nova_sirina = int(alpha*sirina)
        nova_visina = int(alpha*visina)
        
        odnos_sirina = float(sirina)/float(nova_sirina)
        odnos_visina = float(visina)/float(nova_visina)
        
        count = 0
        nova_slika = []
        
        for i in range(nova_visina):
            for j in range(nova_sirina):
                x = int(odnos_sirina*j)
                y = int(odnos_visina*i)
                x_diff = (odnos_sirina*j) - x
                y_diff = (odnos_visina*i) - y
                
                if (x>=(nova_sirina-1) or y>=(nova_visina-1)):
                    A_boja = slika[y][x]
                else:
                    A_boja = slika[y][x]
                if ((x+1)>=(nova_sirina-1) or (y>=(nova_visina-1))):
                    B_boja = slika[y][x]
                else:
                    B_boja = slika[y+1][x]
                if (x>=(nova_sirina-1) or ((y+1)>=(nova_visina-1))):
                    C_boja = slika[y][x]
                else:
                    C_boja = slika[y][x+1]
                if ((x+1)>=(nova_sirina-1) or (y+1)>=(nova_visina-1)):
                    D_boja = slika[y][x]
                else:
                    D_boja = slika[y+1][x+1]
                
                boja = np.int16( (A_boja * (1 - x_diff) * (1 - y_diff)) + (B_boja * (x_diff) * (1 - y_diff))
                                + (C_boja * (y_diff)*(1 - x_diff)) + (D_boja * (x_diff*y_diff)))
        
                
                newrow=int(count/(nova_sirina))
                newcol=count%(nova_sirina)
                if(newcol == 0):
                    nova_slika.append([])
                nova_slika[newrow].append(boja)
                count +=1
                
        slika = np.uint8(nova_slika)
        return Image.fromarray(slika)
    
    def rotacija(self, alpha, slika):
        '''
        Zumira za odredjeni faktor da pokrije  uglove koji postaju crni posle rotacije
        zatim rotira koristeci three shears metod

        Parameters
        ----------
        alpha : float
            ugao rotacije od -25 do 25
        slika : PIL.Image
            slika koja se sredjuje

        Returns
        -------
        PIL.Image
            sredjena slika

        '''
        if alpha == 0:
            return slika
        slika = np.int16(np.array(slika))
        alpha = m.radians(alpha)
        visina = slika.shape[0]
        sirina = slika.shape[1]
        if visina < sirina:
            tmp = visina
            visina = sirina
            sirina = tmp
            
        koef_zuma = (m.sqrt(visina**2+sirina**2)*m.sin(m.atan(sirina/visina)+abs(alpha)))/sirina
        
        stara_visina = visina
        stara_sirina = sirina
        nova_slika = self.zumiranje(koef_zuma,slika)
        nova_slika = np.int16(nova_slika)
        
        visina = nova_slika.shape[0]
        sirina = nova_slika.shape[1]
        centar_visina = round(((visina+1)/2)-1)
        centar_sirina = round(((sirina+1)/2)-1)
        nova_visina = round(abs(visina*m.cos(alpha))+abs(sirina*m.cos(alpha)))+1
        nova_sirina = round(abs(sirina*m.cos(alpha))+abs(visina*m.cos(alpha)))+1
        novi_centar_visina = round(((nova_visina+1)/2)-1)
        novi_centar_sirina = round(((nova_sirina+1)/2)-1)
        
        slika = np.zeros((nova_visina, nova_sirina, 3))
        
        for i in range(visina):
            for j in range(sirina):
                
                x = visina - 1 - i - centar_visina
                y = sirina - 1 - j - centar_sirina
                
                x1 = round(x - y*m.tan(alpha/2))
                y1 = round(x1*m.sin(alpha) + y)
                x1 = round(x1 - y1*m.tan(alpha/2))
                
                x1 = novi_centar_visina - x1
                y1 = novi_centar_sirina - y1
                slika[x1,y1, :] = nova_slika[i, j, :]
                
                
                

        slika = slika[round((nova_visina - visina)/2):round((nova_visina - visina)/2) + visina+1,
                      round((nova_sirina - sirina)/2):round((nova_sirina - sirina)/2) + sirina+1]
        slika = slika[round((koef_zuma-1)/2*stara_visina):round((koef_zuma-1)/2*stara_visina)+stara_visina,
                      round((koef_zuma-1)/2*stara_sirina):round((koef_zuma-1)/2*stara_sirina)+stara_sirina]
        slika = np.uint8(slika)
        return Image.fromarray(slika)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    