import requests
import time
import ctypes

import pyautogui
import os

from PIL import Image
import pytesseract

class Ocr:
    def __init__(self, filePath, url,  api=False):
        self.filePath = filePath
        self.api = api
        self.url = url

        self.processImage()
        data = self.getDataFromImage()
        print(data)
        self.sendToAPI(data)

    #uses external API to parse image to text
    def ocrAPI(self, overlay=False, api_key='fc0d1ddf2788957', language='pol'):
        payload = {'isOverlayRequired': overlay,
                'apikey': api_key,
                'language': language,
                }
        with open(self.filePath, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                            files={self.filePath: f},
                            data=payload,
                            )
        text = r.content.decode("utf-8")
        parsedText = text[text.find("ParsedText")+13:text.find("ErrorMessage")-3].replace("\\r\\n"," ")
        return parsedText

    #uses internal program 'tesseract' to parse image to text
    def ocrTesseract(self):
        return pytesseract.image_to_string(Image.open(self.filePath), config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')


    def processImage(self):
        #makes screenshot
        myScreenshot = pyautogui.screenshot(region=(0,80,100,30))
        myScreenshot.save(self.filePath)

        #makes screenshot bw
        img = Image.open(self.filePath)
        thresh = 200
        fn = lambda x : 255 if x > thresh else 0
        r = img.convert('L').point(fn, mode='1')
        r.save(self.filePath)

    #determines way to get text from image
    def getDataFromImage(self):
        if(self.api == False):
            return self.ocrTesseract()
        else:
            return self.ocrAPI()
        
    def sendToAPI(self, data):
        requests.get(self.url, {'data':data})

    def callApi(self):
        return requests.get(self.url, {'data':'2137'})


filePath = os.getcwd()+"\\screen.png"
url = 'http://emsonlabels.site/python.php'


i=0
while i>=0:
    ocr = Ocr(filePath, url)
    time.sleep(0.5)





""" for x in range(99):
    print(parseImage(filePath))
     """

