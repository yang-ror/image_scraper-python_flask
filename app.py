# =============================================================================
#  app.js
#  project: Image Scraper
#  author: Zifan Yang
#  date created: 2021-01-05
#  last modified: 2021-01-15
# =============================================================================

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import requests
import zipfile
import wget
import sys
import os


#use requests to make request to url and use BeautifulSoup4 to decode the return, then use lxml to read <img> tags.
def requestURL(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    titleTag = soup.find_all('title')
    title = titleTag[0].text

    images = soup.find_all('img')
    image_urls = []

    if len(images) > 0:
        for image in images:
            if image['src'].startswith("http"):
                image_urls.append(image['src'])
            else:
                image_url = image['src']
                if image_url.startswith('.'):
                    image_url = removingDotsAtBeginning(image_url)

                indexOfSlashes = findAllIndexOfCharacter(url[7:len(url)], '/')
                for indexOfSlash in range(len(indexOfSlashes)-1, 0, -1):
                    temp_url = url[0: indexOfSlashes[indexOfSlash] + 7] + image_url[0: len(image_url)]
                    image_urls.append(temp_url)
                    # if UrlIsValid(temp_url):
                    #     image_urls.append(temp_url)
                    #     break

    else:
        print("Unable to find any images")
    
    # print(title)
    # for image_url in image_urls:
    #     print(image_url)
    
    return title, image_urls


def removingDotsAtBeginning(string):
    temp = string[1:len(string)]
    if temp.startswith('.'):
        temp = removingDotsAtBeginning(temp)
    return temp


# def UrlIsValid(url):
#     try:
#         requests.get(url)
#     except:
#         return False
#     return True


def findAllIndexOfCharacter(string, character):
    indexes = []
    for index in range(len(string)):
        if character == string[index]:
            indexes.append(index)
    return indexes


def findLastIndexOfCharacter(string, character):
    lastIndex = 0
    for index in range(len(string)):
        if character == string[index]:
            lastIndex = index
    return lastIndex


#use wget to download the images to ./downloads/ and a folder named by time
def downloadFile(i, title, url):
    indexOfFileName = findLastIndexOfCharacter(url, '/')
    filenameFromUrl = url[indexOfFileName+1:len(url)]
    path = './' + 'downloads' + '/' + title + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    filenameFromUrl = str(i) + '_' + filenameFromUrl
    filename = path + filenameFromUrl
    try:
        wget.download(url, filename)
    except:
        print("Failed to download: ", url, ' ', sys.exc_info()[0])


#compress the images to a zip file to ./statics/ for static file hosting
def compressToZip(path, compressedFile):
    for root, dirs, files in os.walk(path):
        for file in files:
            compressedFile.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))


app = Flask(__name__, static_url_path='/', static_folder='./static')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scrapImg', methods=['POST'])
def scrapImg():
    url = request.form['url']
    try:
        title, image_urls = requestURL(url)
        return render_template('scrapImg.html', title = title, image_urls=image_urls)
    except:
        return redirect(url_for('home'))


@app.route('/static/<path:path>')
def downloadZip(path):
    return send_from_directory('static', path)


@app.route('/downloadImg', methods=['POST'])
def downloadImg():
    urls = request.get_json()
    title = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    threads = []
    i = 0
    for url in urls:
        i = i + 1
        threads.append(threading.Thread(target=downloadFile, args=(i, title, url)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    compressedFile = zipfile.ZipFile('./static/' + title + '.zip', 'w', zipfile.ZIP_DEFLATED)
    compressToZip('./downloads/' + title, compressedFile)
    compressedFile.close()
    fileUrl = '/' + title + '.zip'
    # print('\n[Download Completed]returned:', fileUrl)
    return fileUrl


if __name__ == "__main__":
    app.run(debug=True)