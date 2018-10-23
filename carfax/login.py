# this code will use selenium to login to carfax

#will use scrapy to post ads to kijiji
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
from inputToSheets import startRegistrationsFriday, startAuthorization
from carfax_scraper import get_carfax_info
import pandas as pd

registrations_friday = startRegistrationsFriday(startAuthorization())

def get_carfax(vin=None):
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
    # vin_list = registrations_friday_df["VIN(17)"].values


    vin_field = browser.find_element_by_id('vin')
    vin_field.send_keys(vin)

    get_report_button = browser.find_element_by_id('run_vhr_button')
    get_report_button.click()
    time.sleep(2)

    browser.get("https://www.carfaxonline.com/api/report?vin={0}".format(vin))
    carfax_html = browser.page_source

    get_carfax_info(carfax_html)

    '''for vin in vin_list:
        vin_field.send_keys(vin) # make the url for that vin available
        get_carfax_info(vin)'''


    # open new tab to search vin in
    # browser.execute_script("window.open('');")
    # time.sleep(3)
    # Switch to the new window
    # browser.switch_to.window(browser.window_handles[1])



    # search_vin(vin)


if __name__ == '__main__':
    print(get_carfax('1FM5K8GT4GGA53716'))