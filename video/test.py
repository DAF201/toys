from multiprocessing import Process
from PIL import ImageGrab
import cv2
import win32con
import win32gui
import pyautogui
import os
import time
import scan

THIS_PATH = os.getcwd()
START_TIME = time.time()
WINDOW_NAME = 'man in mirror'

def window_capture() -> None:
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(THIS_PATH+'\\'+r'%s.png' % str(time.time()-START_TIME))


def video_cap() -> None:
    cap = cv2.VideoCapture(0)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.imshow(WINDOW_NAME, img)
        k = cv2.waitKey(1)
        if k == 27:
            exit()
        elif k == 26:
            fetch_image()
        elif k == 24:
            window_capture()


def get_window_pos(name):
    handle = win32gui.FindWindow(0, name)
    if handle == 0:
        return None
    else:
        return win32gui.GetWindowRect(handle), handle


def fetch_image() -> None:
    (x1, y1, x2, y2), handle = get_window_pos(
        WINDOW_NAME)
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,
                         win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(handle)
    grab_image = ImageGrab.grab((x1, y1, x2, y2))
    grab_image.save(THIS_PATH+'\\'+r'%s.png' % str(time.time()-START_TIME))

if __name__ == '__main__':
    p1=Process(target=video_cap,args=())
    p2=Process(target=scan.scan,args=())
    p1.start()
    p2.start()
    p1.join()
    p2.join()