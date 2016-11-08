#!/usr/bin/env python
# -*- coding: utf-8 -*-
from skimage import data, io, filters, feature, morphology
from matplotlib import pyplot as plt
from skimage.morphology import disk

def read_images(images):
    img_tab = []
    for img in images:
        img_tab.append(data.imread(img, flatten=True))
    return img_tab

def imagination(image):
    edges =  filters.sobel(image)
    #edges2 = feature.canny(image, sigma=3)
    for i in range(len(edges)):
        for j in range(len(edges[0])):
            if edges[i][j] > 0.15:
                edges[i][j] = 1
            else:
                edges[i][j] = 0
    # edges =  morphology.erosion(edges)
    # edges =  morphology.dilation(edges)
    return edges

def main():
    planes = ["samolot01.jpg","samolot07.jpg","samolot08.jpg","samolot09.jpg","samolot10.jpg","samolot11.jpg"]
    images = read_images(planes)
    fig = plt.figure(facecolor='black')

    for i in range(0,6):
        plt.subplot(231+i)
        ax = plt.gca()
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        plt.imshow(imagination(images[i]),cmap=plt.cm.gray)

    plt.tight_layout()
    plt.show()
    fig.savefig('my_planes.pdf', facecolor=fig.get_facecolor())


if __name__ == '__main__':
    main()
