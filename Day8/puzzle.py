#!/bin/python

WIDTH = 25
HEIGHT = 6
IMAGE_PIXELS = HEIGHT * WIDTH

image = input("Image $> ")

layers = []
layer_no = int(round(len(image)/(WIDTH * HEIGHT)))
min_zeros = None

for l in range(layer_no):
    layer = []
    zeros = 0
    ones = 0
    twos = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel = int(image[l * IMAGE_PIXELS + y * WIDTH + x])
            if pixel == 0:
                zeros += 1
            elif pixel == 1:
                ones += 1
            elif pixel == 2:
                twos += 1

            layer.append(pixel)

    if min_zeros:
        if min_zeros[1] > zeros:
            min_zeros = [l, zeros, ones * twos]
    else:
        min_zeros = [l, zeros, ones * twos]

    layers.append(layer.copy())


print("Result: {}".format(min_zeros))
