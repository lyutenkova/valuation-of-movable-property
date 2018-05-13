from time import sleep

import os
from django.core.files.storage import FileSystemStorage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def create_webdriver(link):
    # profile = webdriver.FirefoxProfile()
    # profile.accept_untrusted_certs = True
    # profile.assume_untrusted_cert_issuer=True
    # profile.accept_next_alert = True
    # binary = FirefoxBinary('./libs/firefox_46/firefox')
    # binary = FirefoxBinary('./libs/firefox_58/firefox')
    chrome_options = Options()

    # profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
    #            "download.default_directory": './docs'}
    # chrome_options.add_experimental_option("prefs", profile)
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-extensions")

    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./libs/chromedriver')
    # driver = webdriver.Firefox(firefox_profile=profile, executable_path='./libs/geckodriver', firefox_binary=binary)
    driver.get(link)
    # driver.get_screenshot_as_file("capture.png")
    return driver




def page_has_loaded(driver):
    # self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

def save_file_to_disk(request):
    myfile = request.FILES['myfile']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    full_path = os.path.join(fs.location, filename)
    print("UPLOADED", filename)
    return full_path

def save_files_to_disk(request):
    paths = []
    fs = FileSystemStorage()
    for f in request.FILES.getlist('myfile'):
        filename = fs.save(f.name, f)
        full_path = os.path.join(fs.location, filename)
        paths += [full_path]
        print("UPLOADED", filename)
    return paths


if __name__ == '__main__':
    create_webdriver('https://www.reestr-zalogov.ru/')
    sleep(7)