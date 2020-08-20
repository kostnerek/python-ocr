import requests
import time
import ctypes

import pyautogui
import os

from PIL import Image
from PIL import ImageFilter
import pytesseract
import cv2

class Ocr:
    def __init__(self, filePath, url,  api=False):
        self.filePath = filePath
        self.api = api
        self.url = url

        self.findReference()

        self.offsetX = 0
        self.offsetY = 0

    def action(self):
        self.processImage()
        data = self.getDataFromImage()

        if self.api == True:
            if data == "":
                self.findReference()
        else:
            if len(data) == 1:
                self.findReference()
        
        print(data)
        self.sendToAPI(data)

    def findReference(self):
        print("SEARCHING FOR HP...")
        self.findHp = pyautogui.locateOnScreen('reference.png', confidence=0.5)
        
        print(self.findHp)
        if self.findHp is None:
            self.findHp = [0,80,100,35]
            self.offsetX = 0
            self.offsetY = 0
        else:
            print("FOUND")
    
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
        time.sleep(0.5)
        return parsedText

    #uses internal program 'tesseract' to parse image to text
    def ocrTesseract(self):
        return pytesseract.image_to_string(Image.open(self.filePath), config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

    #makes screenshot and makes it bw
    def processImage(self):
        #makes screenshot
        #myScreenshot = pyautogui.screenshot(region=(0,80,100,35))
       
        """ myScreenshot = pyautogui.screenshot(region=(self.findHp[0] - self.offsetX, self.findHp[1] + self.offsetY,
                                                    self.findHp[2] - self.offsetX, self.findHp[3] - self.offsetY)) """

        myScreenshot = pyautogui.screenshot(region=(self.findHp[0], self.findHp[1], self.findHp[2], self.findHp[3]))
        myScreenshot.save(self.filePath)

        #makes screenshot bw
        img = Image.open(self.filePath)
        img.filter(ImageFilter.SHARPEN)
        

        thresh = 170
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

#class end =============================================================




filePath = os.getcwd()+"\\screen.png"
url = 'http://emsonlabels.site/python.php'

i=0
ocr = Ocr(filePath, url)


while i>=0:
    #start_time = time.time()
    ocr.action()
    #print("--- %s seconds ---" % (time.time() - start_time))

