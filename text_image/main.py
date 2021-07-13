from PIL import ImageDraw, Image, ImageFont
import numpy
import string
import random
import os

#getcurrentpath
current_path = os.getcwd()
# input path
origin_image_path = current_path+'\\text_image\\input\\input.jpg'
text_image = current_path+'\\text_image\\input\\input.txt'
#output path
save_path = current_path+'\\text_image\\something_out'
#scale of image
scale = 100

#generate a random file name
def random_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def pic():
    #text input
    text = open(text_image).read()
    #font
    font = ImageFont.truetype(
        current_path+'\\text_image\\font\\Arvo-Bold.ttf', scale, encoding="UTF-8")
    #open orginal image
    origin = Image.open(origin_image_path)
    #convert to a array of color
    array = numpy.array(origin)
    #blank image
    new_image = Image.new(
        "RGB", (len(array) * scale, len(array[0]) * scale), color=(255, 255, 255))
    #draw on blank image
    draw = ImageDraw.Draw(new_image)
    #location of the input text
    word_count = 0
    #scan over the image
    for x in range(0, len(array)):
        for y in range(0, len(array[0])):
            #skip when white
            if tuple(array[x][y]) == (255, 255, 255):
                continue
            #not white, write
            word_count += 1
            draw.text((scale * y, scale * x), text[word_count % len(text)], font=font,
                      fill=tuple(array[x][y]))
    #save
    new_image.save(save_path + '\\%s.jpg' % (random_generator(5)))

def main():
    if __name__ == "__main__":
        pic()
    else:
        pass

main()