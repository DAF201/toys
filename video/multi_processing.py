import winsound
from multiprocessing import Process
import cv2
import pyautogui
import time
import pathlib
import scan
import os


PATH = str(pathlib.Path(__file__).parent.resolve())
START_TIME = time.time()
WINDOW_NAME = 'man in mirror'


def window_capture() -> None:
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(PATH+'\\'+r'%s.png' % str(time.time()-START_TIME))


def video_cap() -> None:
    switch_counter = 0
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
            window_capture()
        elif k == 24:
            switch(switch_counter)
            switch_counter += 1


def covered() -> str:
    print('今天化身什么呢？')
    print('1:顶碗人,2:贝极星,3:皇珈骑士, 4:嘉心糖, 5.奶淇淋')
    user = input()

    if user == '1' or user == '顶碗人':
        covered = r".\source\bowl.png"
    elif user == '2' or user == '贝极星':
        covered = r".\source\star.png"
    elif user == '3' or user == '皇珈骑士':
        covered = r".\source\knight.png"
    elif user == '4' or user == '嘉心糖':
        covered = r".\source\candy.png"
    elif user == '5' or user == '奶淇淋':
        covered = r".\source\icecream.png"
    elif user == 'asoul' or user == '一个魂':
        covered = r".\source\A_soul.png"
    elif user == 'mouse' or user == 'mice' or user == 'rat' or '鼠' in user:
        covered = r".\source\mouse.png"
    elif user == '毒唯' or user == 'dw':
        covered = r".\source\joker.png"
    elif user == 'carol' or user == 'Carol' or user == '珈乐':
        covered = r".\source\Carol.png"
    elif user == 'cr':
        covered = r".\source\cr.png"
    elif user == 'alien':
        covered = r".\source\alien.png"
    elif user == 'redheel' or user == '高跟鞋':
        covered = r".\source\high_heel.png"
    elif user == '流汗黄豆' or user == '😅':
        covered = r".\source\sweating_soybean.png"
    elif user == 'hj' or user == '汉奸' or user == 'traitor':
        covered = r".\source\traitor.png"
    elif user == 'robot' or user == '机器人':
        covered = r".\source\robot.png"
    elif user == 'demon' or user == '恶魔':
        covered = r".\source\demon.png"
    elif user == 'microphone' or user == 'jb':
        covered = r".\source\microphone.png"
    elif user == 'lama' or user == '羊驼' or user == '阿草':
        if os.path.isfile(PATH+'\source\lama.png'):
            covered = r".\source\lama.png"
        else:
            print('file missing')
            covered = r".\source\ybb.png"
    else:
        covered = r".\source\ybb.png"
    return covered


def bgm() -> None:
    winsound.PlaySound(PATH+'\source\RHH.wav',
                       winsound.SND_ASYNC | winsound.SND_ALIAS)


def stop_bgm() -> None:
    winsound.PlaySound(None, winsound.SND_ASYNC)


def switch(switch_counter):
    if switch_counter % 2 == 0:
        bgm()
    else:
        stop_bgm()


def main() -> None:
    result = covered()
    p1 = Process(target=video_cap, args=())
    p2 = Process(target=scan.scan, args=(result,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':
    main()
