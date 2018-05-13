import datetime
from time import sleep, time

import os

import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from selenium.common.exceptions import TimeoutException

from gos_checker.settings import DOCS
from support import create_webdriver


#Вкладка залогодатель
def navigate_to_pledgor_tab():
    webdriver = create_webdriver('http://www.reestr-zalogov.ru/search')
    webdriver.get('https://www.reestr-zalogov.ru/search/index#search-by-pledgor')
    webdriver.get_screenshot_as_file("capture.png")
    lnk = webdriver.find_element_by_xpath("//a[contains(text(), 'По информации о залогодателе')]")
    lnk.click()
    return webdriver


def get_links(webdriver):
    res=[]
    a_tags = webdriver.find_elements_by_xpath("//a[contains(@href,'notificationData')]")
    for a in a_tags:
        res += [a.get_attribute("href")]
    return res


def download_document(link, inn, webdriver):
    print("Downloading started")
    cookies = webdriver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    r = s.get(link, stream=True, verify=False)
    dir = os.path.join(DOCS, inn)
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = os.path.join(dir, '{}.pdf'.format(datetime.datetime.now().strftime("%d%m%Y|%H%M%S")))
    with open(path, 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)
    if os.path.exists(path):
        print("SAVED")
        return path
    return None


def get_info_from_site(webdriver):
    inner_table = webdriver.find_element_by_class_name("table-search")
    table = BeautifulSoup(inner_table.get_attribute('innerHTML'))
    headers = [header.string() for header in table.findAll("thead tr th")]
    results = [{headers[i]: cell.text_content() for i, cell in enumerate(row.findAll("td"))} for row in table.findAll("tbody tr")]
    return results

def get_documents_for_organization(inn=None):
    inn = str(inn)
    if inn is None or len(inn) < 8:
        return None
    webdriver = navigate_to_pledgor_tab()
    # element = WebDriverWait(webdriver, 20).until(expected_conditions.presence_of_element_located((By.ID, "search-params")))
    organization_tab = webdriver.find_element_by_xpath("//*[contains(text(), 'Юридическое лицо')]")
    organization_tab.click()

    inn_field = webdriver.find_element_by_id("INN")
    inn_field.click()
    inn_field.send_keys(inn)

    find = webdriver.find_element_by_id("find-btn")
    find.click()
    if captcha_is_visible(webdriver):
        return None
        resolve_captcha(webdriver)
    # sleep(1)

    doc_lnks = get_links(webdriver)

    # info = get_info_from_site(webdriver)
    # return info
    info={}
    for l in doc_lnks:
        d = download_document(l, inn, webdriver)
        r = plan_b_parse_docs(d)
        print("RESULT:", r)
        info['objects'] = r
    webdriver.quit()
    return info
        # print(info)


def get_documents_for_person(firstname=None, lastname=None):
    webdriver = navigate_to_pledgor_tab()
    person_tab = webdriver.find_element_by_xpath("//*[contains(text(), 'Физическое лицо')]")
    person_tab.click()

    lastname_field = webdriver.find_element_by_id("Last")
    lastname_field.click()
    lastname_field.send_keys(lastname)
    firstname_field = webdriver.find_element_by_id("First")
    firstname_field.click()
    firstname_field.send_keys(firstname)

    find = webdriver.find_element_by_id("find-btn")
    find.click()
    if captcha_is_visible(webdriver):
        resolve_captcha(webdriver)
    sleep(7)

    doc_lnks = get_links(webdriver)
    for l in doc_lnks:
        d = download_document(l, firstname + '_' + lastname, webdriver)
        info = get_info_from_site(webdriver)
        print(d)
        print(info)


if __name__ == '__main__':
    get_documents_for_organization(inn='2455030482')
    # get_documents_for_person('Владимир', 'Микрюков')

    dicts = parse_documents(os.path.join(DOCS, '2455030482'))
    print(dicts)
    '''    
    #Есть
    2455030482
    0909000840
    6382045403

    
    #Нет
    Ярославцева любвь сергеевна 28.04.87
    4826109256
    381104649224
    '''
