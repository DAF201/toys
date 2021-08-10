from PIL import ImageGrab
import cv2
import threading
import win32con
import win32gui
import pyautogui
import time
import scan
import pathlib

PATH = str(pathlib.Path(__file__).parent.resolve())
START_TIME = time.time()
WINDOW_NAME = '镜中人'


def window_capture() -> None:
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(PATH+'\\'+r'%s.png' % str(time.time()-START_TIME))


def video_cap() -> None:
    lock = threading.Lock()
    lock.acquire()
    cap = cv2.VideoCapture(0)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    lock.release()
    while True:
        lock.acquire()
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.setWindowProperty(
            WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(WINDOW_NAME, img)
        pyautogui.click(100, 100)
        k = cv2.waitKey(1)
        if k == 27:
            exit()
        elif k == 26:
            fetch_image()
        elif k == 24:
            window_capture()
        lock.release()


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
    grab_image.save(PATH+'\\'+r'%s.png' % str(time.time()-START_TIME))


def covered() -> str:
    print('今天化身什么呢？')
    print('1:流汗黄豆,2:小丑,3:高跟鞋')
    user = input()
    if user == '1':
        covered = "\sweating_soybean.png"
    elif user == '2':
        covered = "\poker_face.png"
    elif user == '3':
        covered = "\high_heel.png"
    else:
        covered = "\A_soul.png"
    return covered


if __name__ == '__main__':
    result = covered()
    joker = threading.Thread(target=scan.scan, args=(result,))
    video = threading.Thread(target=video_cap, args=())
    video.start()
    joker.start()
    joker.join()
    video.join()
