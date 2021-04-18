import os
import sys
import time
import requests
import urllib.request
from bs4 import BeautifulSoup


file = open("url.txt", "r")

for url in file:
    if url.startswith("http"):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        titleTag = soup.find_all('title')
        title = titleTag[0].text[0: -13]

        if '*' in title:
            title = title.replace("*", "")
        if ':' in title:
            title = title.replace(":", " ")
        if '`' in title:
            title = title.replace("`", "~")

        images = soup.find_all('img')

        if len(images) > 0:
            if not os.path.exists(title):
                os.makedirs(title)
                print("Creating dolder: ", title, " for ",str(len(images)), " images", end = "\r")
            i = 0
            for image in images:
                i = i + 1
                numberStr = str(i)
                if i < 10:
                    numberStr = "00" + numberStr
                elif i < 100:
                    numberStr = "0" + numberStr
                image_url = image['src']
                try:
                    fileFormat = image_url[image_url.rindex('.'):]
                    try:
                        filename = './' + title + '/' + numberStr + fileFormat
                        urllib.request.urlretrieve(image_url, filename)
                        j = i % 3
                        if j == 0:
                            starStr = "[*--]"
                        elif j == 1:
                            starStr = "[-*-]"
                        else:
                            starStr = "[--*]"
                        print(starStr, "Downloading :", filename, " /", len(images), end = "\r")
                    except:
                        print("Failed to download " + image_url + " as " + filename)
                except:
                    print("[*****]Failed to get file format for " + image_url + "[*****]")
        else:
            print("Unable to find any images for ", url)
    else:
        print("----------------------------------------------------------")
