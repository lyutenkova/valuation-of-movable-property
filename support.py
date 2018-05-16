from time import sleep

import os
from django.core.files.storage import FileSystemStorage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

def save_file_to_disk(request):
    myfile = request.FILES['myfile']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    full_path = os.path.join(fs.location, filename)
    print("UPLOADED", filename)
    return full_path
