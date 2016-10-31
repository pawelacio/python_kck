#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.png') #zmienic na pdf

# def hsv2rgb(h, s, v):# dane wejsciowe hue, saturation i value
#     if v == 0:
#         return (0,0,0)
#     else:
#         r, g, b = 0, 0, 0
#         h = h/60
#         i = math.floor(h)
#         f = h - i
#         p = v * (1 - s)
#         q = v * (1 - (s*f))
#         t = v * (1 - (s*(1-f)))
#         if i == 0:
#             r,g,b = v,t,p
#         elif i == 1:
#             r,g,b = q,v,p
#         elif i == 2:
#             r,g,b = p,v,t
#         elif i == 3:
#             r,g,b = p,q,v
#         elif i == 4:
#             r,g,b = t,p,v
#         elif i == 5:
#             r,g,b = v,p,q
#         return (r,g,b)

def hsv2rgb2(h, s, v):

    g,r,b = 0,0,0
    # while v < 0:
    #     v+=360
    # while v > 0:
    #     v-=360

    c = s * v #Chroma
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

def gradient_rgb_bw(v):
    return (v, v, v)


def gradient_rgb_gbr(v):
    if v < 0.5:
        return (0, 1-v/0.5, v/0.5)
    else:
        return ((v - 0.5)/0.5, 0, (1-v)/0.5)


def gradient_rgb_gbr_full(v):
    if v < 0.25:
        return (0, 1, v/0.25)
    elif v < 0.50:
        return (0, (0.50-v)/0.25, 1)
    elif v < 0.75:
        return ((v-0.5)/0.25,0,1)
    else:
        return (1,0,(1-v)/0.25)



def gradient_rgb_wb_custom(v):
    pom = 1/7
    if v < pom:
        return (1, (pom-v)/pom, 1)
    elif v < 2*pom:
        return ((2*pom-v)/pom,0,1)
    elif v < 3*pom:
        return (0,(v-2*pom)/pom,1)
    elif v < 4*pom:
        return (0,1,(4*pom-v)/pom)
    elif v < 5*pom:
        return ((v-4*pom)/pom,1,0)
    elif v < 6*pom:
        return (1,(6*pom-v)/pom,0)
    else:
        return ((7*pom-v)/pom,0,0)


def gradient_hsv_bw(v):
    return hsv2rgb2(0,0,v)


def gradient_hsv_gbr(v):
    if v < 0.5:
        return hsv2rgb2(120+120*v/0.5,1,1)
    else:
        return hsv2rgb2(240+120*(v-0.5)/0.5,1,1)

def gradient_hsv_unknown(v):
    return hsv2rgb2(120-120*v,0.502,1)


def gradient_hsv_custom(v):
    if v < 0.5:
        return hsv2rgb2(360*v, 1, 1)
    else:
        return hsv2rgb2(360*v,(1-(v-0.5)),(1-(v-0.5)))


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
