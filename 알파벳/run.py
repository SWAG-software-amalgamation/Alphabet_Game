from pynput.keyboard import Listener, Key, KeyCode
from threading import Thread
import check
import cv2
import sys

store = set()
input_setting_check = set([Key.ctrl_l, Key.alt_l, Key.cmd])
data_check = set([Key.alt_l, Key.cmd])
loop_check = 1

def program_run_while():
    while True:
        check.pose_alphabet_check_main_def()
        if cv2.waitKey(1) == 32:
            break

print("start")

def explain_input_while(N):
    N = str(N)[1].upper()
    if (N in check.alphabetlist):
        check.explain_input = N
        check.what_explain_input = 0

def handleKeyPress(key):
    global loop_check
    if (key == Key.ctrl_l) or (key == Key.alt_l) or (key == Key.cmd):
        store.add(key)
        if store == input_setting_check:
            loop_check = 1 if loop_check == 0 else 0
            if loop_check == 1:
                check.what_explain_input = 1
        if store == data_check:
            print("Input_check", check.image_upload_stop,loop_check )
            if check.image_upload_stop == 0 and loop_check == 0:
                check.image_upload_stop = 1
                print("stop_check", check.image_upload_stop)
            elif check.image_upload_stop == 1:
                check.image_upload_stop = 0
                print("restart_check", check.image_upload_stop)
    else:
        if loop_check == 1:
            explain_input_while(key)
            loop_check = 0

def handleKeyRelease(key):
    if key in store:
        store.remove(key)

def hotkey_def():
    with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
        listener.join()

t1 = Thread(target=hotkey_def)
t2 = Thread(target=program_run_while)
t1.start()
t2.start()
t1.join()
t2.join()