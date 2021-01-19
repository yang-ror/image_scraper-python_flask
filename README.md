# Image Scraper

Scrap all the images from the target url, and let the user select the images to be downloaded. Once selected, the backend will download all the selected images and compress them into one zip file, then send the file's url to the frontend for download.

Key features:
  - Hide images smaller than a certain number of pixels(50px on default, compare to width or height, whichever is smaller).
  - User can select specific image formats to display(png, jpg, jpeg, gif)
  - The user can use the left click to single select and right-click to multi-select in the image pool.
  

### Build based on:
  - Python 3.9 \ pipenv
  - BeautifulSoup4 \ lxml \ requests \ wget
  - Flask
  - HTML \ CSS \ Javascript
  - JQuery \ Bootstrap


**Live demo:**

**Dockerhub:**

### Things to know:
  - In the backend, images are download by wget and stored in ./downloads/[a subdirectory named by current time]
  - Zip files are stored in ./status/
  - Auto-delete of above files is not implementated yet
  - to run the project:
    1. cd into the imageScraper
    2. run the command: export FLASK_APP=app.py (on Windows: set FLASK_APP=app.py)
    3. run: flask run
