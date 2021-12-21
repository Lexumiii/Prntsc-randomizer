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
from utility import JsonData, DirHandler
import base64
from io import BytesIO
from PIL import Image

user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"


class Database:
    def __init__(self):
        self.database_name = 'database'
        self.extension = 'json'

    def saveSuffix(self, suffix, lastKey):
        with open("suffixes.json") as json_file:
            json_data = json.load(json_file)

        highest = 0
        try:
            # loop over all keys and get highest
            keys = json_data.keys()
            for key in keys:
                highest = int(key)
        except ValueError:
            highest = 0

        # get new key
        newKey = highest + 1
        json_data[newKey] = suffix

        with open("suffixes.json", 'w') as json_file:
            json.dump(json_data, json_file)

        return


class Prntsc:
    def __init__(self):
        self.url_prefix = 'https://prnt.sc/'
        self.url_suffix = ''
        self.suffix_length = 6
        self.database = Database()
        self.json = JsonData()
        self.noLongerAvailable = "iVBORw0KGgoAAAANSUhEUgAAAKEAAABRAQMAAACADVTsAAAABlBMVEUiIiL///9ehyAxAAABrElEQVR4Xu3QL2/bQBgG8NdRlrnMNqxu1eVAahCQVAEF03STbsuBSFVZYEBBoJ2RjZ0Hljuy6IZaUlUlpfsKRUmZP4JTNJixkEm7nJu/Mxlot0l7JJOfXj06P/D3xvkBQH/lqoEC7WVvzqM0k/f4+Gat2nt7ppqeCjCbiJX6HmN7vnca4LLc0BljH/yZ0ZejDQXGlA9GmYSthoumVw1wZ6PByxjrpxmeZq0hbMcDXPCHGVB4hHCAkgUKrrNSulawelPRCH37mu4fR1EdZYPwnTA6UZoQfteoMSmPCFVcgYmUmmCuPMKkIAtNFjqS+hWyOo+MzmVsb12NS1aFazThe1Ztr2qYBklWvcPKCKG+TA/MGwjqDcI4n1Pko+1E5KM9TRz75fGB0qWv1Vlq/Bo9Gzqo3oqu7g991G1bVQmp8IQcdeRtEGpyxoVVB5eNLob0qS6xpaJc5+J7Wx+wkwct5SoSn2vCOORKrHZk0lC69tAbm4a2g0grEuknvd9tb61XhqK8hz+d/xG/cft5fD0dvxA7qsLrj+EXWqBugRbeHl6qcbCr4Ba+7Tn88/kJk4CIztd1IrIAAAAASUVORK5CYII="

        # Headers from a chrome web browser used to circumvent bot detection.
        self.userAgent = user_agent

    def getSoup(self):
        # create folder for images
        dirHandler = DirHandler()
        dirHandler.make_dir('downloads')

        # create list for suffixes
        suffixes = []

        # set max downloads
        for i in range(1000000000):
            # append random suffix
            suffixes.append(self.createSuffix())

            # send request to prnt.sc
            req = requests.get("https://prnt.sc/" + suffixes[i], headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"})

            # get curent tree
            tree = html.fromstring(req.content)

            # get url
            url = ''.join(tree.xpath('//img[@id="screenshot-image"]/@src'))

            # check if image was found
            if ("//st" not in url):
                if("/image/" not in url):
                    try:
                      # get image from url
                        req = requests.get(url, stream=True)

                        # check if request was successful
                        if req.status_code == 200:

                            # save as image
                            with open("downloads/" + suffixes[i] + ".png", "wb") as file:
                                # decode raw request
                                req.raw.decode_content = True
                                shutil.copyfileobj(req.raw, file)
                                try:
                                    # open the image file
                                    img = Image.open(
                                        './' + "downloads/" + suffixes[i] + ".png")
                                    img.verify()  # verify that it is, in fact an image
                                except (IOError, SyntaxError) as e:
                                    # print out the names of corrupt files
                                    print('Bad file:', "downloads/" +
                                          suffixes[i] + ".png")
                                print("Image added")

                                # TODO: add log message for found image
                    except Exception as e:
                        # TODO: add log message for error
                        pass

    def encode_image(image_url):

        buffered = BytesIO(requests.get(image_url).content)
        image_base64 = base64.b64encode(buffered.getvalue())

        return b'data:image/png;base64,'+image_base64

    def createSuffix(self, char=string.ascii_uppercase + string.digits + string.ascii_lowercase):

        # create random suffix
        self.url_suffix = ''.join(random.choice(char)
                                  for x in range(self.suffix_length))

        # check if the suffix was already used once
        exists = self.json.checkData(
            self.url_suffix, "suffixes.json")
        if(exists):
            print("Suffix was already used")
            # TODO: add log message

            # create new suffix
            self.createSuffix()

        else:
            database = Database()

            # save suffix
            database.saveSuffix(
                self.url_suffix, "prntsc.usedNumbers")
            # return created suffix
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
        with open('suffixes.json', 'w') as file:
            jsonData = json.load(file)


if __name__ == '__main__':
    prt = GUI()
    prt.create_gui()
