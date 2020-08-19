import requests
import time

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


filePath = os.getcwd()+"\\screen.jpg"

for x in range(99):
    print(parseImage(filePath))
    time.sleep(1)





