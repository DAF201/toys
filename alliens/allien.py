from PIL import Image, ImageFilter, ImageDraw
import numpy as np
from random import randrange
number = 50
path1 = "python/toys/alliens/IMG_8603.PNG"  # 输入图一路径
path2 = "python/toys/alliens/allien.jpg"  # 输入外星人头路径
maskpath = 'python/toys/alliens/alliensmask_circle.jpg'  # mask存储路径
savepath = 'python/toys/alliens/target.jpg'  # 输出存储路径
scale = 10
img1 = Image.open(path1)
img1 = img1.resize((600, 600))
img1_array = np.array(img1)
img2 = Image.open(path2)
mask_im = Image.new("L", img2.size, 0)
draw = ImageDraw.Draw(mask_im)
draw.ellipse((15, 15, 45, 45), fill=255)
mask_im.save(maskpath, quality=100)
lx = []
ly = []
nl = []
rd = []
mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))
back_im = img1.copy()


def change():
    for x in range(60, img1.height):
        for y in range(60, img1.width):
            if list(img1_array[x][y]) == [255, 255, 255]:
                lx.append(x)
                ly.append(y)
    for x in range(0, len(lx)-1):
        nl.append((lx[x], ly[x]))
    for x in range(0, number):
        y = randrange(0, len(nl))
        rd.append(y)
    for x in range(0, number):
        printsomething(back_im, nl[rd[x]])
    back_im.save(savepath, quality=95)


def printsomething(pic, x):
    pic.paste(img2, x, mask_im_blur)


change()
