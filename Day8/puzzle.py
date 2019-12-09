#!/bin/python

WIDTH = 25
HEIGHT = 6
IMAGE_PIXELS = HEIGHT * WIDTH

image = input("Image $> ")

layers = []
layer_no = int(round(len(image)/(WIDTH * HEIGHT)))

for l in range(layer_no):
    layer = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            pixel = int(image[l * IMAGE_PIXELS + y * WIDTH + x])

            row.append(pixel)
        layer.append(row.copy())

    layers.append(layer.copy())

final_image = layers[0]

for layer in layers[1:]:
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if final_image[y][x] == 2:
                final_image[y][x] = layer[y][x]

for y in range(HEIGHT):
    for x in range(WIDTH):
        i = final_image[y][x]
        if i == 2:
            final_image[y][x] = " "
        elif i == 1:
            final_image[y][x] = '■'
        elif i == 0:
            final_image[y][x] = '□'

print("")
print("")
print("")

for row in final_image:
    outp = ''.join(str(e) for e in row)
    print("{}".format(outp))
