from PIL import Image, ImageFilter, ImageDraw
import PyFaceDet


def print_face():
    path1 = "python/toys/alliens/7434.png"
    path2 = "python/toys/alliens/allien.jpg"
    maskpath = 'python/toys/alliens/alliensmask_circle.jpg'
    img1 = Image.open(path1)
    img1=img1.resize((200,300))
    img2 = Image.open(path2)
    mask_im = Image.new("L", img2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((15, 15, 45, 45), fill=255)
    mask_im.save(maskpath, quality=100)
    mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))

    position=PyFaceDet.facedetectcnn.facedetect_cnn(img1)
    if position!=[]:
        x=position[0][0]+position[0][3]
        x=int(x/2)
        y=position[0][1]+position[0][2]
        y=int(y/2)
        img1.paste(img2,(x,y), mask_im_blur)
        print('识别可信度：%s'%position[0][4])
        img1.show()
    else:
        print('未找到面部')
print_face()