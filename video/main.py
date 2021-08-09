from multiprocessing import Process
from PIL import ImageGrab
import cv2
import win32con
import win32gui
import pyautogui
import time
import pathlib
import scan

PATH = str(pathlib.Path(__file__).parent.resolve())
START_TIME = time.time()
WINDOW_NAME = 'man in mirror'


def window_capture() -> None:
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(PATH+'\\'+r'%s.png' % str(time.time()-START_TIME))


def video_cap() -> None:
    cap = cv2.VideoCapture(0)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.imshow(WINDOW_NAME, img)
        pyautogui.click(100, 100)
        k = cv2.waitKey(1)
        if k == 27:
            exit()
        elif k == 26:
            fetch_image()
        elif k == 24:
            window_capture()


def get_window_pos(name) -> None:
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
    print('1:顶碗人,2:贝极星,3:皇珈骑士, 4:嘉心糖, 5.奶淇淋')
    user = input()
    if user == '1':
        covered = r".\source\bowl.png"
    elif user == '2':
        covered = r".\source\star.png"
    elif user == '3':
        covered = r".\source\knight.png"
    elif user == '4':
        covered = r".\source\candy.png"
    elif user == '5':
        covered = r".\source\icecream.png"
    elif user == 'asoul':
        covered = r".\source\A_soul.png"
    elif user == 'mouse' or user == 'mice' or user == 'rat' or '鼠' in user:
        covered = r".\source\mouse.png"
    elif user == '毒唯' or user == 'dw':
        covered = r".\source\joker.png"
    elif user == 'carol' or user == 'Carol' or user == '珈乐':
        covered = r".\source\Carol.png"
    elif user == 'cr':
        covered = r".\source\cr.png"
    else:
        covered = r".\source\ybb.png"
    return covered


if __name__ == '__main__':
    result = covered()
    p1 = Process(target=video_cap, args=())
    p2 = Process(target=scan.scan, args=(result,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
