import requests
import time
import ctypes

import pyautogui
import os




def ocr_space_file(filename, overlay=False, api_key='fc0d1ddf2788957', language='eng'):
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content



def getParsedText(file_name):
    fileSend = ocr_space_file(filename=file_name, language='pol').decode("utf-8")
    parsedText = fileSend[fileSend.find("ParsedText")+13:fileSend.find("ErrorMessage")-3].replace("\\r\\n"," ")
    return parsedText

def parseImage(filePath):
    myScreenshot = pyautogui.screenshot(region=(0,80,300,30))
    myScreenshot.save(filePath)
    parsedText = getParsedText(filePath)
    #os.remove(filePath)

    return parsedText

def DetectClick(button, watchtime = 5):
    '''Waits watchtime seconds. Returns True on click, False otherwise'''
    if button in (1, '1', 'l', 'L', 'left', 'Left', 'LEFT'):
        bnum = 0x01
    elif button in (2, '2', 'r', 'R', 'right', 'Right', 'RIGHT'):
        bnum = 0x02

    start = time.time()
    while 1:
        if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
            # ^ this returns either 0 or 1 when button is not being held down
            print(pyautogui.position())
            return True
        elif time.time() - start >= watchtime:
            break
        time.sleep(0.001)
    return False

filePath = os.getcwd()+"\\screen.jpg"

i=0
while i>=0:
    DetectClick('left')

""" for x in range(99):
    print(parseImage(filePath))
    time.sleep(1) """

