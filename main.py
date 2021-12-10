import io
import json
import os
import random
import string
import tkinter as tk
import urllib
import requests

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

        # create random suffix
        self.createSuffix()

        # send request
        url = self.url_prefix + self.url_suffix
        # send request to website
        res = requests.get(
            url, headers={"User-Agent": self.userAgent}, allow_redirects=False)

        if(res.status_code == 200):
            soup = BeautifulSoup(res, "lxml")
        else:
            soup = ""

        ourimageurl = None

        try:
            # find img
            if(soup != None and soup != ""):
                ourimageurl = soup.find(id='screenshot-image')['src']
        except TypeError:
            pass

        return ourimageurl

    def createSuffix(self, char=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        self.url_suffix = ''.join(random.choice(char)
                                  for x in range(self.suffix_length))

        exists = self.json.checkData(
            self.url_suffix, "prntsc.usedNumbers", "database.json")
        if(exists):
            self.createSuffix()
        else:

            # check if img is available
            check = self.checkAvailable(self.url_prefix + self.url_suffix)
            print(check)
            if(check == False):
                self.createSuffix()
            else:
                return self

    def checkAvailable(self, url):

        # send request to website
        print(url)
        html_req = requests.get(
            url, headers={"User-Agent": self.userAgent}, allow_redirects=False)

        if html_req.status_code == 302:
            return 302

        # create soup from request
        soup = BeautifulSoup(html_req.content, "html.parser")
        images = soup.find_all("img", {"class": "no-click screenshot-image"})

        for tag in images:
            src_img_from_html = tag["src"]

            if not src_img_from_html.startswith("http"):
                return False
            else:
                return True


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
