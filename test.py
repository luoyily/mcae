import points
import numpy as np
from PIL import Image

# pu = points.Utils()
# # print(pu.rotate(0, 1, 0, 90, 10, 0, 10))
# print(pu.rotate_by_vec(10, 10, 10, 10, 11, 10, 90, 21, 10, 10))
im = Image.open(f'./images/1.jpg')
width, height = im.size[0], im.size[1]
for w in range(0, width):
    for h in range(0, height):
        imgdata = (im.getpixel((w, h)))
        if imgdata == (0, 0, 0):
            print(1)