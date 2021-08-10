import cv2
from PIL import Image
import numpy
import PyFaceDet
import pathlib
import time
import pyautogui

PATH = str(pathlib.Path(__file__).parent.resolve())
START_TIME = time.time()
WINDOW_NAME = 'OpenCV'
cap = cv2.VideoCapture(0)
covered = cv2.imread(PATH + r"\poker_face.png", cv2.IMREAD_UNCHANGED)


def window_capture() -> None:
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(PATH+'\\'+r'%s.png' % str(time.time()-START_TIME))


while True:
    b, g, r, a = cv2.split(covered)
    foreground = cv2.merge((b, g, r))
    alpha = cv2.merge((a, a, a))
    ret, alpha = cv2.threshold(alpha, 254, 1, cv2.THRESH_BINARY)
    foreground = cv2.multiply(alpha, foreground)
    ret, background = cap.read()
    background = cv2.flip(background, 1)
    position = PyFaceDet.facedetectcnn.facedetect_cnn(background)
    if position != []:
        # background_temp = background[position[0][0]+10:position[0][0] +
        #                              foreground.shape[0]+10, position[0][1]:position[0][1]+foreground.shape[1], :]
        background_temp = background[position[0][0]:position[0][0] +
                                     foreground.shape[0], position[0][1]:position[0][1]+foreground.shape[1], :]
        background_temp = cv2.multiply(1-alpha, background_temp)
        outImage = foreground + background_temp
        image = Image.fromarray(cv2.cvtColor(outImage, cv2.COLOR_BGR2RGB))
        background = Image.fromarray(
            cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
        background.paste(image, (position[0][0], position[0][1]), None)
        background = cv2.cvtColor(numpy.asarray(background), cv2.COLOR_RGB2BGR)
    cv2.namedWindow('OpenCV', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        "OpenCV", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("OpenCV", background)
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == 26:
        window_capture()
