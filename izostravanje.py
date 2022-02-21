import tkinter as tk
from PIL import Image
import numpy as np
import math as m

class izostravanje_prozor(tk.Toplevel):
    
    def __init__(self, master = None):
        tk.Toplevel.__init__(self, master = master)
        
        self.nivo_rotacije = 0
        
        self.prava_slika = self.master.sredjena_slika
        self.sredjena_slika = self.master.sredjena_slika
        
        self.izostravanje_label = tk.Label(self, text = "Ostrina")
        self.izostravanje_scale = tk.Scale(self, from_ = 0, to_= 3, length = 250, resolution = 0.01, orient = tk.HORIZONTAL)
        self.izostravanje_scale.set(1)
        self.izbledjivanje_label = tk.Label(self, text = "Izbledi")
        self.izbledjivanje_scale = tk.Scale(self, from_=0, to_=1, length = 250, resolution = 0.01, orient = tk.HORIZONTAL)
        self.tilt_shift_variable = tk.StringVar(self)
        self.tilt_shift_variable.set("NISTA")
        self.tilt_shift_label = tk.Label(self, text = "Tilt Sift")
        self.tilt_shift_optionenu = tk.OptionMenu(self, self.tilt_shift_variable, "NISTA", "LINEARNI", "RADIJALNI")
        self.vinjeta_label = tk.Label(self, text = "Vinjeta")
        self.vinjeta_scale = tk.Scale(self, from_ = 0, to_=1, length = 250, resolution = 0.01, orient = tk.HORIZONTAL)
        
        self.primeni_button = tk.Button(self, text = "Primeni")
        self.vidi_button = tk.Button(self, text = "Vidi")
        self.odustani_button = tk.Button(self, text = "Odustani")
        
        self.primeni_button.bind("<ButtonRelease>", self.primeni_promene)
        self.vidi_button.bind("<ButtonRelease>", self.vidi_promene)
        self.odustani_button.bind("<ButtonRelease>", self.odustani_promene)
        
        self.izostravanje_label.pack()
        self.izostravanje_scale.pack()
        self.izbledjivanje_label.pack()
        self.izbledjivanje_scale.pack()
        self.tilt_shift_label.pack()
        self.tilt_shift_optionenu.pack()
        self.vinjeta_label.pack()
        self.vinjeta_scale.pack()
        
        self.primeni_button.pack(side = tk.LEFT)
        self.vidi_button.pack(side = tk.LEFT)
        self.odustani_button.pack()
    
    def primeni_promene(self, event):
        self.master.sredjena_slika = self.sredjena_slika
        self.close()
    
    def vidi_promene(self,event):
        self.sredjena_slika = self.master.sredjena_slika
        self.sredjena_slika = self.izbledjivanje(self.izbledjivanje_scale.get(), self.sredjena_slika)
        self.sredjena_slika = self.izostravanje(self.izostravanje_scale.get(), self.sredjena_slika)
        self.sredjena_slika = self.tilt_shift(self.tilt_shift_variable.get(), self.sredjena_slika)
        self.sredjena_slika = self.vinjeta(self.vinjeta_scale.get(), self.sredjena_slika)
        self.prikaz_slike(self.sredjena_slika)
    
    def odustani_promene(self, event):
        self.close()
    
    def prikaz_slike(self, slika = None):
        self.master.platno.prikaz_slike(slika=slika)
    
    def close(self):
        self.prikaz_slike(self.master.sredjena_slika)
        self.destroy()
        
    
    def izostravanje(self,alpha, slika):
        '''
        pravi blurovanu sliku i onda linearno primenjuje na originalnu sliku,
        za alpha 0 dobijamo blurovanu sliku, za alpha 1 originalnu,
        za alpha 1+ dobijamo ostriju

        Parameters
        ----------
        alpha : float
            koeficijent izostravanja
        slika : PIL.Image
            slika koja se obradjuje

        Returns
        -------
        PIL.Image
            sredjena slika

        '''
        if alpha == 1:
            return slika
        slika = np.array(slika)
        slika = np.int16(slika)
        blur = self.blur(slika)
        slika = (1 - alpha)*blur + alpha*slika

        slika = np.where(slika<255,slika,255)
        slika = np.where(slika<0,0,slika)
        slika = np.uint8(slika)
        return Image.fromarray(slika)
        
    
    def gauss_kernel(self, oblik,sigma):
        '''
        pravi gausov kernel zadatog oblika sa disperzijom sigma

        Parameters
        ----------
        oblik : tuple
            dve dimenzije kernela, koliko piksela uzimamo u obzir kad radimo konvoluciju
        sigma : float
            distribucija gausovog kernela, "jacina promene"

        Returns
        -------
        np.ndarray
            gausov kernel

        '''
        visina = oblik[0]
        sirina = oblik[1]
        centar_visina = visina // 2
        centar_sirina = sirina // 2
        kernel =np.zeros((visina,sirina))
        for i in range(visina):
            for j in range(sirina):            
                diff=((i-centar_visina)**2+(j-centar_sirina)**2)
                kernel[i][j]=np.exp(-(diff)/(2*(sigma**2)))
                
        kernel = kernel/np.sum(kernel)
        
        return np.stack([kernel,kernel,kernel], axis = -1)
    
    
    def convolve2d(self, slika, kernel):
        '''
        Konvolucija kernela i slike, kernel se prevlaci preko slike

        Parameters
        ----------
        slika : np.ndarray
            slika dimnezija (x,y,3)
        kernel : np.ndarray
            kernel dimenzija (z,z,3)

        Returns
        -------
        nova_slika : np.ndarray
            nova slika dimenzije (x,y,3)

        '''
        nova_slika = np.zeros_like(slika)
        dimension = kernel.shape[0]
        if dimension%2==0:
            dimension-=1
        # Channel 1 
        slika_padded = np.zeros((slika.shape[0] + dimension-1, slika.shape[1] + dimension-1,3))
        
        slika_padded[int(np.floor((dimension-1)/2)):-int(np.floor((dimension-1)/2)), int(np.floor((dimension-1)/2)):-int(np.floor((dimension-1)/2))] = slika[:,:]
        for x in range(slika.shape[0]):
            for y in range(slika.shape[1]):
                slika_padded[x: x+dimension, y: y+dimension] = np.where(slika_padded[x: x+dimension, y: y+dimension]<=0, 
                                                          slika_padded[x: x+dimension, y: y+dimension].mean(), slika_padded[x: x+dimension, y: y+dimension])
                nova_slika[x, y]=(kernel * slika_padded[x: x+dimension, y: y+dimension]).sum(axis=(0,1))
                
                         
        return nova_slika
    
    
    def blur(self, slika):
        """
        pomocna funkcija koja bluruje celu sliku koristeci pomocnu funkciju convolve2d

        Parameters
        ----------
        slika : PIL.Image
            slika koja se sredjuje

        Returns
        -------
        slika : PIL.Image
            sredjena slika

        """
        slika = self.convolve2d(slika,self.gauss_kernel((11,11),5))
        return slika

    def izbledjivanje(self, alpha, slika):
        '''
        linearnom transformacijom menja sliku sa potpuno belom slikom

        Parameters
        ----------
        alpha : float
            koeficijen izbeljivanja
        slika : PIL.Image
            slika koja se obradjuje

        Returns
        -------
        PIL.Image
            sredjena slika

        '''
        if alpha == 0:
            return slika
        slika = np.array(slika)
        slika = np.int16(slika)
        belo = np.ones_like(slika)*255
        slika = (1-alpha)*slika + alpha*belo
        slika = np.where(slika<255,slika,255)
        slika = np.where(slika<0,0,slika)
        slika = np.uint8(slika)
        return Image.fromarray(slika)
    
    def tilt_shift(self, mode, slika):
        '''
        Imamo 3 grupe indeksa 0 -> pikseli se ne menjaju, 1 -> menjamo linearno
        u odnosu na udaljenost od centra, 2-> menjamo sa maksimalnim blurom

        Parameters
        ----------
        mode : str
            NISTA, LINEARNI ili RADIJALNI odredjuje koji tilt sift se radi
        slika : PIL.Image
            slika koja se sredjuje

        Returns
        -------
        PIL.Image
            sredjena slika

        '''
        if mode == "NISTA":
            return slika
        slika = np.array(slika)
        slika = np.int16(slika)
        uslov_idx = np.zeros((slika.shape[0],slika.shape[1]))
        kernel_vre = np.zeros((slika.shape[0],slika.shape[1]))
        if mode == "LINEARNI":
            def uslov(x,y):
                if abs(x-slika.shape[0]/2) > 2.0/6.0*slika.shape[0]:
                    return 2
                elif abs(x-slika.shape[0]/2) < 1.0/6.0*slika.shape[0]:
                    return 0
                else:
                    return 1
            
            for x in range(slika.shape[0]):
                for y in range(slika.shape[1]):
                    uslov_idx[x,y] = uslov(x,y)
                    kernel_vre[x,y] = max(0.01, ((abs(x-slika.shape[0]/2)-1.0/6.0*slika.shape[0])/(1.0/6.0*slika.shape[0])*9))
        
        if mode == "RADIJALNI":
            def uslov(x,y):
                if m.sqrt((x-slika.shape[0]/2)**2 + (y-slika.shape[1]/2)**2) > 2.0/6.0*min(slika.shape[0], slika.shape[1]):
                    return 2
                elif m.sqrt((x-slika.shape[0]/2)**2 + (y-slika.shape[1]/2)**2) < 1.0/6.0*min(slika.shape[0], slika.shape[1]):
                    return 0
                else:
                    return 1
                
            for x in range(slika.shape[0]):
                for y in range(slika.shape[1]):
                    uslov_idx[x][y] = uslov(x,y)
                    kernel_vre[x][y] = max(0.01, ((m.sqrt((x-slika.shape[0]/2)**2 +
                                                          (y-slika.shape[1]/2)**2)-1.0/6.0*slika.shape[0])
                                                  /(1.0/6.0*min(slika.shape[0], slika.shape[1]))*9))
            
            
        kernel = self.gauss_kernel((21,21),9)
        kernel_norm = np.zeros((21,21,3))
        kernel_norm[10,10] = np.array([1,1,1])
        nova_slika = np.zeros_like(slika)
        dimension = kernel.shape[0]
        if dimension%2==0:
            dimension-=1

        slika_padded = np.zeros((slika.shape[0] + dimension-1, slika.shape[1] + dimension-1,3))
        
        slika_padded[int(np.floor((dimension-1)/2)):-int(np.floor((dimension-1)/2)),
                     int(np.floor((dimension-1)/2)):-int(np.floor((dimension-1)/2))] = slika[:,:]
        for x in range(slika.shape[0]):
            for y in range(slika.shape[1]):
                print(x, uslov_idx[x,y])
                if uslov_idx[x,y] == 0:
                    kernel1 = kernel_norm
                elif uslov_idx[x,y] == 1:
                    kernel1 = self.gauss_kernel((21,21), kernel_vre[x,y])
                else:
                    kernel1 = kernel
                slika_padded[x: x+dimension, y: y+dimension] = np.where(slika_padded[x: x+dimension, y: y+dimension]<=0, 
                                                          slika_padded[x: x+dimension, y: y+dimension].mean(),
                                                          slika_padded[x: x+dimension, y: y+dimension])
                nova_slika[x, y]=(kernel1 * slika_padded[x: x+dimension, y: y+dimension]).sum(axis=(0,1))
                
                         
        nova_slika = np.where(nova_slika<255,nova_slika,255)
        nova_slika = np.where(nova_slika<0,0,nova_slika)
        nova_slika = np.uint8(nova_slika)
        return Image.fromarray(nova_slika)
    
    
    def vinjeta(self, alpha, slika):
        '''
        Koristeci gausov kernel odredjuemo maksimalnu vinjetu i menjamo linearno
        od originalne slike do maksimalne vinjete

        Parameters
        ----------
        alpha : float
            od 0 do 1 0 vraca originalnu sliku, 1 vraca maksimalnu vinjetu
        slika : PIL.Image
            slika koja se sredjuje

        Returns
        -------
        PIL.Image
            sredjena slika

        '''
        slika = np.array(slika)
        slika = np.int16(slika)
        kernel = self.gauss_kernel((slika.shape[:2]), 1.0/3.0*min(slika.shape[:2]))
        kernel *=2.0/float(kernel[kernel.shape[0]//2,kernel.shape[1]//2,0])
        kernel = np.where(kernel>1, 1, kernel)
        nova_slika = kernel * slika
        slika = (1-alpha)*slika + alpha*nova_slika
        slika = np.where(slika<255,slika,255)
        slika = np.where(slika<0,0,slika)
        slika = np.uint8(slika)
        return Image.fromarray(slika)
