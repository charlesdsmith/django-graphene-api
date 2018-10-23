# will use beautifulsoup to scrape
import re

from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import requests
from inputToSheets import startRegistrationsFriday, startAuthorization
registrations_friday = startRegistrationsFriday(startAuthorization())

def get_carfax_info():
    chromedriver = 'C:/Users/User/Desktop/chromedriver.exe'

    #create a chrome object
    browser = webdriver.Chrome(executable_path=chromedriver)
    browser.get('https://www.carfaxonline.com/login')


    username = browser.find_element_by_css_selector("input[type='text']")
    password = browser.find_element_by_css_selector("input[type='password']")

    username.send_keys("info@germanstarsmotorllc.com")
    password.send_keys("Aastra57")

    browser.find_element_by_id("login_button").click()
    wait = WebDriverWait(browser, 3)
    wait_for_dashboard = wait.until(EC.url_to_be("https://www.carfaxonline.com/"))

    # get registrations as a dataframe
    registrations_friday_df = get_as_dataframe(registrations_friday)

    # get list of vins from dataframe
    vin_list = registrations_friday_df["VIN(17)"].values

    '''get_report_button = browser.find_element_by_id('run_vhr_button')
    get_report_button.click()
    time.sleep(2)

    browser.get("https://www.carfaxonline.com/api/report?vin={0}".format(vin))
    carfax_html = browser.page_source  # get all html from page

    soup = bs(carfax_html, features="lxml")

    additionalHistoryTable = soup.find(id='otherInformationTable')
    # table_body = additionalHistoryTable.find('tbody')
    #print(table_body)
    totalLossCells = additionalHistoryTable.find("div", id=re.compile("^totalLossCol")).text
    frameDamageCells = additionalHistoryTable.find("div", id=re.compile("^frameDamageCol")).text
    airbagCells = additionalHistoryTable.find("div", id=re.compile("^airbagCol")).text
    odometerCells = additionalHistoryTable.find("div", id=re.compile("^odometerCol")).text
    accidentCheckCells = additionalHistoryTable.find("div", id=re.compile("^accidentCheckCol")).text
    recallCells = additionalHistoryTable.find("div", id=re.compile("^recallCol")).text

    carfax_info = [totalLossCells, frameDamageCells, airbagCells, odometerCells, accidentCheckCells, recallCells]

    api_call(carfax_info)'''

    for vin in vin_list:
        #browser.get('https://www.carfaxonline.com/')
        vin_field = browser.find_element_by_id('vin')
        vin_field.send_keys(vin)  # make the url for that vin available

        get_report_button = browser.find_element_by_id('run_vhr_button')  # get report
        get_report_button.click()
        time.sleep(2)

        browser.switch_to.window(browser.window_handles[1])

        #browser.get("https://www.carfaxonline.com/api/report?vin={0}".format(vin))
        carfax_html = browser.page_source  # get all html from page

        soup = bs(carfax_html, features="lxml")

        additionalHistoryTable = soup.find(id='otherInformationTable')
        # table_body = additionalHistoryTable.find('tbody')
        #print(table_body)
        totalLossCells = additionalHistoryTable.find_all("div", id=re.compile("^totalLossCol"))
        frameDamageCells = additionalHistoryTable.find_all("div", id=re.compile("^frameDamageCol"))
        airbagCells = additionalHistoryTable.find_all("div", id=re.compile("^airbagCol"))
        odometerCells = additionalHistoryTable.find_all("div", id=re.compile("^odometerCol"))
        accidentCheckCells = additionalHistoryTable.find_all("div", id=re.compile("^accidentCheckCol"))
        recallCells = additionalHistoryTable.find_all("div", id=re.compile("^recallCol"))

        carfax_info = [vin, totalLossCells, frameDamageCells, airbagCells, odometerCells, accidentCheckCells, recallCells,
                       carfax_html]

        api_call(carfax_info)


def api_call(info):
    # example of info parameter
    # ['No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'No Recalls Reported']

    cookies = {
        'PGADMIN_LANGUAGE': 'en',
        'PGADMIN_KEY': '5edc9e0d-8f36-4e63-8e9e-694ae3d9f9a9',
        'csrftoken': 'iHH5pujGsroVpiwBR4qpKuhVovCyWRauddwiCZaxnxxHzANt7rNTGhc4fKbjaqEV',
        'pga4_session': 'b395d851-2905-4dd9-aa83-7d27af6f0557!3ovpR7+Zw4XwrrRD0A9Qg5NYExs=',
        'tabstyle': 'raw-tab',
    }

    headers = {
        'Origin': 'http://127.0.0.1:8000',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'text/html; q=1.0, */*',
        'Referer': 'http://127.0.0.1:8000/api/v1/carfax/',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'X-CSRFTOKEN': 'iHH5pujGsroVpiwBR4qpKuhVovCyWRauddwiCZaxnxxHzANt7rNTGhc4fKbjaqEV',
    }

    data = {
           "vin": info[0],
           "structural_damage": info[2],
           "total_loss": info[1],
           "accident": info[5],
           "airbags": info[3],
           "odometer": info[4],
           "recalls": info[6]
    }

    response = requests.post('http://127.0.0.1:8000/api/v1/carfax/', headers=headers, cookies=cookies, data=data)


if __name__ == "__main__":
    print(get_carfax_info())


