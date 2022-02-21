import numpy as np

def RGBtoHSV(slika):
    '''
    Sa RGB sistema prelazi na HSV sistem boja

    Parameters
    ----------
    slika : 0<np.ndarray[x,y,3]<255 

    Returns
    -------
    TYPE
        0<np.ndarray[x,y,3]<1

    '''
    slika /= 255.0
    in_shape = slika.shape
    slika = np.array(slika, copy = False, dtype = np.promote_types(slika.dtype, np.float32),ndmin=2)
    rez = np.zeros_like(slika)
    slika_max = slika.max(-1)
    ipos = slika_max > 0
    delta = slika.ptp(-1)
    s = np.zeros_like(delta)
    s[ipos] = delta[ipos]/slika_max[ipos]
    ipos = delta > 0
    rez = np.zeros_like(slika)
    idx = (slika[..., 0] == slika_max) & ipos
    rez[idx, 0] = (slika[idx, 1] - slika[idx, 2])/delta[idx]
    idx = (slika[..., 1] == slika_max) & ipos
    rez[idx, 0] = 2.0 + (slika[idx, 2] - slika[idx, 0])/delta[idx]
    idx = (slika[..., 2] == slika_max) & ipos
    rez[idx, 0] = 4.0 + (slika[idx, 0] - slika[idx, 1])/delta[idx]
    
    rez[..., 0] = (rez[...,0]/6.0) % 1
    rez[..., 1] = s
    rez[..., 2] = slika_max
    return rez.reshape(in_shape)
                
def HSVtoRGB(slika):
    '''
    Sa HSV sistema prelazi na RGB sistem boja

    Parameters
    ----------
    slika : 0<np.ndarray[x,y,3]<1

    Returns
    -------
    TYPE
        0<np.ndarray[x,y,3]<255 

    '''
    in_shape = slika.shape
    slika = np.array(slika, copy = False, dtype = np.promote_types(slika.dtype, np.float32),ndmin=2)
    h = slika[..., 0]
    s = slika[..., 1]
    v = slika[..., 2]
    
    r = np.empty_like(h)
    g = np.empty_like(h)
    b = np.empty_like(h)

    i = (h * 6.0).astype(int)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    
    idx = i % 6 == 0
    r[idx] = v[idx]
    g[idx] = t[idx]
    b[idx] = p[idx]

    idx = i == 1
    r[idx] = q[idx]
    g[idx] = v[idx]
    b[idx] = p[idx]

    idx = i == 2
    r[idx] = p[idx]
    g[idx] = v[idx]
    b[idx] = t[idx]

    idx = i == 3
    r[idx] = p[idx]
    g[idx] = q[idx]
    b[idx] = v[idx]

    idx = i == 4
    r[idx] = t[idx]
    g[idx] = p[idx]
    b[idx] = v[idx]

    idx = i == 5
    r[idx] = v[idx]
    g[idx] = p[idx]
    b[idx] = q[idx]

    idx = s == 0
    r[idx] = v[idx]
    g[idx] = v[idx]
    b[idx] = v[idx]
    
    r = np.int16(r*255)
    g = np.int16(g*255)
    b = np.int16(b*255)
    rgb = np.stack([r, g, b], axis=-1)
    return rgb.reshape(in_shape)
                
                
                
                
                
                
                
                
                
                
                
                
                
                