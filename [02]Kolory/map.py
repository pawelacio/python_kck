#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import math


#funkcja konwerujaca z modelu hsv do rgb
def hsv2rgb(h, s, v):

    g,r,b = 0,0,0

    c = s * v #chroma
    hdev = h / 60
    x = c * (1-math.fabs((hdev % 2) - 1))
    m = v - c

    if hdev < 1:
        r = c
        g = x
    elif hdev < 2:
        r = x
        g = c
    elif hdev < 3:
        g = c
        b = x
    elif hdev < 4:
        g = x
        b = c
    elif hdev < 5:
        r = x
        b = c
    elif hdev <= 6:
        r = c
        b = x

    return (r+m,g+m,b+m)

#funkcja czytajaca dane oraz szukajaca maksymalnego oraz minimalnego elementu w  pliku
#czyli najmniejszej i najwiekszej wysokosci
def readdata(plik):
    data = []
    h = 0
    w = 0
    dif = 0
    maxi = 0
    mini = 150
    with open(plik) as f:
        for j, line in enumerate(f):
            helparr = line.split()
            if j == 0:
                h = helparr[0]
                w = helparr[1]
                dif = helparr[2]
            else:
                for i in range(0,int(w)):
                    if maxi < float(helparr[i]):
                        maxi = float(helparr[i])
                    if mini > float(helparr[i]):
                        mini = float(helparr[i])
                data.append(helparr)
        print(int(maxi))
        print(int(mini))
    return h,w,int(dif),data,int(mini),int(maxi)

#funkcja zamieniajaca tablice z danymi
#na tablice z trojkami RGB
def data2rgbtable(table,mini,maxi,dif):
    s = np.array([10000,50,10000])#pozycja slonca
    rgbtable = []
    w = 0.05
    roznica = maxi - mini
    for i in range(1, 500):
        pomtable = []
        for j in range(1, 500):
            pcurr = np.array([j*dif,float(table[i][j]),i*dif])
            p2 = np.array([(j-1)*dif,float(table[i][j-1]),i*dif])
            p3 = np.array([(j-1)*dif,float(table[i-1][j-1]),(i-1)*dif])
            normal = np.cross(pcurr-p2,pcurr-p3)#wektor normalny do trojkata utworzonego z 3 punktow na mapie
            normal_unit = normal/np.linalg.norm(normal)
            sun = s-pcurr
            sun_unit = sun/np.linalg.norm(sun)
            pom = np.arccos(np.clip(np.dot(normal_unit, sun_unit), -1.0, 1.0))
            angle =  np.degrees(pom)
            #angle = (180/3.14)*np.arccos(np.clip(np.dot(normal,(s-pcurr))/np.linalg.norm(normal)/np.linalg.norm((s-pcurr)), -1, 1))
            v = 91 - angle
            v = v*10-9
            #print(v)
            if v > 1:
                v = 1
            if v < 0:
                v = v+1
            r = math.floor(float(table[i][j]))
            #kolor podstawowy
            rgb = hsv2rgb(120-(((r-40)/roznica)*120),1,v)
            #rozjasnianie albo zciemnianie1
            #if float(table[i][j-1]) > r:
            #    rgb = hsv2rgb(120-(((r-40)/roznica)*120),1,1)
            #else:
            #    rgb = hsv2rgb(120-(((r-40)/roznica)*120),1,0.85)
            pomtable.append(rgb)
        rgbtable.append(pomtable)
    return rgbtable




def main():
    h, w, dif, data, mini, maxi = readdata('big.dem') #height, width, diff and data
    img = data2rgbtable(data,mini,maxi,dif)

    fig = plt.figure()
    plt.imshow(img)
    plt.show()
    fig.savefig('map.png')
    fig.savefig('map.pdf')

if __name__ == '__main__':
    main()
