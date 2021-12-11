import io
import json
from math import exp
import os
import random
import string
import tkinter as tk
import requests
import shutil
from lxml import html
from tkinter import *
from tkinter import ttk
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from utility import JsonData

user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"


class Database:
    def __init__(self):
        self.database_name = 'database'
        self.extension = 'json'

    def saveSuffix():
        print('not implemented')


class Prntsc:
    def __init__(self):
        self.url_prefix = 'https://prnt.sc/'
        self.url_suffix = ''
        self.suffix_length = 6
        self.database = Database()
        self.json = JsonData()

        # Headers from a chrome web browser used to circumvent bot detection.
        self.userAgent = user_agent

    def getSoup(self):

        suffixes = []
        # set max downloads
        for i in range(100):
            # append random suffix
            suffixes.append(self.createSuffix())
            req = requests.get("https://prnt.sc/" + suffixes[i], headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"})

            # get curent tree
            tree = html.fromstring(req.content)

            # get url
            url = ''.join(tree.xpath('//img[@id="screenshot-image"]/@src'))

            if ("//st" not in url):
                if("/image/" not in url):
                    if(url != ""):
                        try:
                            # get image from url
                            req = requests.get(url, stream=True)
                            if req.status_code == 200:
                                # save as image
                                with open("images/" + suffixes[i] + ".png", "wb") as file:
                                    # decode request
                                    req.raw.decode_content = True
                                    shutil.copyfileobj(req.raw, file)
                                    # TODO: add log message for found image
                        except Exception as e:
                            print(e)
                            # TODO: add log message
                            pass
                        else:
                            print('No Image was found in this link')
                            # TODO: add log message

    def createSuffix(self, char=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        self.url_suffix = ''.join(random.choice(char)
                                  for x in range(self.suffix_length))

        exists = self.json.checkData(
            self.url_suffix, "prntsc.usedNumbers", "database.json")
        if(exists):
            print("Suffix was already used")
            self.createSuffix()
        else:
            return self.url_suffix


class GUI:
    def __init__(self):
        self.database = Database()
        self.prntsc = Prntsc()
        self.imgurl = self.prntsc.getSoup()

    def create_gui(self):

        # initialize root object
        root = tk.Tk()

        # display img

        """
        print(req)
        
        webpage = urlopen(req).read()
        # raw_data = urllib.request.urlopen("https://image.prntscr.com/image/eK6nRdTLTQiAxxN1fY8Syw.png").read()
        im = Image.open(io.BytesIO(webpage))
        image = ImageTk.PhotoImage(im)
        label1 = Label(root, image=image)
        label1.grid(row=1, sticky=W)
        # create save Button
        saveButton = Button(
            text="Speichern", command=self.add_downloads("img.png"))
    	"""
        root.mainloop()

    def add_downloads(self, img):

        # get img name
        imagename = img.split(".")[0]

        # append to database
        with open('database.json', 'w') as file:
            jsonData = json.load(file)


if __name__ == '__main__':
    prt = GUI()
    prt.create_gui()
