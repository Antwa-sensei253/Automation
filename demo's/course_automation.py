"""
import os
import pyautogui as gui
res=gui.size()
x=res[0]
y=res[1]
os.system("c:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe")
gui.hotkey('alt','tab')
gui.typewrite(["https://www.coursera.org/learn/advanced-learning-algorithms",'Enter'])

"""
import os
import pyautogui
import time

def open_brave_and_navigate(url):
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    os.startfile(brave_path)

    time.sleep(1)
    n=pyautogui.position(x=1211, y=480)
    pyautogui.moveTo(1211,480)
    pyautogui.click()

    pyautogui.hotkey('ctrl', 't')
    pyautogui.write(url)
    pyautogui.press('enter')

if __name__ == "__main__":
    url_to_open = "https://www.coursera.org/learn/advanced-learning-algorithms/home/week/1"
    open_brave_and_navigate(url_to_open)
