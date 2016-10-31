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
    return h,w,dif,data,int(mini),int(maxi)

#funkcja zamieniajaca tablice z danymi
#na tablice z trojkami RGB
def data2rgbtable(table,mini,maxi):
    rgbtable = []
    w = 0.05
    roznica = maxi - mini
    for i in range(0, 500):
        pomtable = []
        for j in range(0, 500):
            r = math.floor(float(table[i][j]))
            #kolor podstawowy
            rgb = hsv2rgb(120-(((r-40)/roznica)*120),1,0.9)
            #rozjasnianie albo zciemnianie
            if float(table[i][j-1]) > r:
                rgb = hsv2rgb(120-(((r-40)/roznica)*120),1,1)
            else:
                rgb = hsv2rgb(120-(((r-40)/roznica)*120),1,0.85)
            pomtable.append(rgb)
        rgbtable.append(pomtable)
    return rgbtable




def main():
    h, w, dif, data, mini, maxi = readdata('big.dem') #height, width, diff and data
    img = data2rgbtable(data,mini,maxi)

    fig = plt.figure()
    plt.imshow(img)
    plt.show()
    fig.savefig('map.png')
    fig.savefig('map.pdf')

if __name__ == '__main__':
    main()
