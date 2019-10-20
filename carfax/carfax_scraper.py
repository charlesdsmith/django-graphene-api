# will use beautifulsoup to scrape
import re

from bs4 import BeautifulSoup as bs
import requests
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
#from carfax.carfax_calls import
import requests
from inputToSheets import startRegistrationsFriday, startAuthorization,startCarfaxSheet
import numpy as np
import datetime

from api.damageComparison import getAllDamageComparisons

# options to make browser headless
'''options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') #
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")'''

sheets_auth = startAuthorization()
registrations_friday = startRegistrationsFriday(sheets_auth)
carfax_2_sheet = startCarfaxSheet(sheets_auth)
print(pd.__version__)

def get_carfax_infoMMC():
    chromedriver = 'C:/Users/User/Desktop/chromedriver.exe'

    #create a chrome object
    browser = webdriver.Chrome(executable_path=chromedriver)
    browser.get('https://www.carfaxonline.com/login')


    username = browser.find_element_by_css_selector("input[type='text']")
    password = browser.find_element_by_css_selector("input[type='password']")

    username.send_keys("***")
    password.send_keys("***")

    browser.find_element_by_id("login_button").click()
    wait = WebDriverWait(browser, 3)
    wait_for_dashboard = wait.until(EC.url_to_be("https://www.carfaxonline.com/"))

    # get registrations as a dataframe
    registrations_friday_df = get_as_dataframe(registrations_friday, evaluate_formulas=True)
    registrations_friday_df.dropna(subset=['VIN(17)'], inplace=True)

    # get list of vins from dataframe
    vin_list = registrations_friday_df["VIN(17)"].values

    # curated vin list that excludes vin that have been run already
    curated_vin_list = [row["VIN(17)"] for index, row in registrations_friday_df.iterrows() if pd.isna(row["Run"])]

    print("VIN LIST", vin_list)
    print("CURATED VIN LIST", curated_vin_list)
    print("VIN LIST LENGTH:", len(vin_list))
    print("CURATED VIN LIST LENGTH:", len(curated_vin_list))
    # get carfax2 as dataframe
    carfax_2_dataframe = get_as_dataframe(carfax_2_sheet)
    # carfax_2_dataframe = pd.DataFrame(carfax_2_dataframe)

    vin_location_txt = r"C:\Users\User\Documents\Heroku\gsm-django\carfax\vin_location.txt"

    # write each vin from vin_list to a text file
    # not be used right now
    '''for vin in vin_list:
        with open(reg_vin_list_txt, "a") as file:
            file.write(vin)'''

    current_vin_location = open(vin_location_txt, 'r').readlines()[0]
    print(current_vin_location)
    vin_counter = 0
    carfax_data = []  # this will store the 6 values and be returned by the function to use in api calls
    print(len(list(curated_vin_list)))

    try:
        print("INDEX OF VIN BEING PROCESSED: %s " % current_vin_location)
        for vin in curated_vin_list[int(current_vin_location):]:  # range(curated_vin_list[current_vin_location], len(curated_vin_list) - 1):
            print(vin)

            if type(vin) is not str or len(vin) < 17:

                continue

            wait = WebDriverWait(browser, 1.5)
            wait.until(EC.presence_of_element_located((By.ID, "vin-input")))

            vin_field = browser.find_element_by_id('vin-input')
            vin_field.send_keys(vin)  # make the url for that vin available

            get_report_button = browser.find_element_by_id('header_run_vhr_button')  # get report

            get_report_button.click()
            time.sleep(2)

            # browser.switch_to.window(browser.window_handles[1])
            # close the new tab
            browser.close()

            last_handle = browser.window_handles[0]
            browser.switch_to.window(last_handle)

            browser.get("https://www.carfaxonline.com/api/report?vin={0}".format(vin))
            carfax_html = browser.page_source  # get all html from page

            soup = bs(carfax_html, features="lxml")

            additionalHistoryTable = soup.find(id='otherInformationTable')
            # table_body = additionalHistoryTable.find('tbody')
            # print(table_body)
            totalLossValues=''
            frameDamageValues=''
            airbagValues=''
            odometerValues=''
            accidentCheckValues=''
            recallValues=''
            countryOriginValues=''

            totalLossCellsDivs = additionalHistoryTable.find_all("div", id=re.compile("^totalLossCol"))
            totalLossCellsAs = additionalHistoryTable.find_all("a", id=re.compile("^totalLossCol"))
            totalLossCells = totalLossCellsDivs + totalLossCellsAs

            frameDamageCellsDivs = additionalHistoryTable.find_all("div", id=re.compile("^frameDamageCol"))
            frameDamageCellsAs = additionalHistoryTable.find_all("a", id=re.compile("^frameDamageCol"))
            frameDamageCells = frameDamageCellsDivs + frameDamageCellsAs

            airbagCellsDivs = additionalHistoryTable.find_all("div", id=re.compile("^airbagCol"))
            airbagCellsAs = additionalHistoryTable.find_all("a", id=re.compile("^airbagCol"))
            airbagCells = airbagCellsDivs + airbagCellsAs

            odometerCellsDivs = additionalHistoryTable.find_all("div", id=re.compile("^odometerCol"))
            odometerCellsAs = additionalHistoryTable.find_all("a", id=re.compile("^odometerCol"))
            odometerCells = odometerCellsDivs + odometerCellsAs

            accidentCheckCellsDivs = additionalHistoryTable.find_all("div", id=re.compile("^accidentCheckCol"))
            accidentCheckCellsAs = additionalHistoryTable.find_all("a", id=re.compile("^accidentCheckCol"))
            accidentCheckCells = accidentCheckCellsDivs + accidentCheckCellsAs

            recallCellsDivs = additionalHistoryTable.find_all("div", id=re.compile("^recallCol"))
            recallCellsAs = additionalHistoryTable.find_all("a", id=re.compile("^recallCol"))
            recallCells = recallCellsDivs + recallCellsAs

            countryOriginCells = soup.find_all("span", class_="vehicleRecordSource")


            for cell in countryOriginCells:  #if 'NICB' is not in the contents of the 'source' column return just that value
                if 'NICB' not in cell.contents[0] and 'FCA' not in cell.contents[0] and 'OnStar' not in cell.contents[0] and "Dealer Inventory" not in cell.contents[0]:
                    print("TRUE")
                    print(cell.contents[0])
                    # create a list of items in the cell that are only of the type "NavigableString"
                    test = [i for i in cell.contents if 'bs4.element.NavigableString' in str(type(i))]
                    print(test)
                    countryOriginValues += ','.join(test)
                    break

            for cell in totalLossCells:
                # print(cell.contents)
                totalLossValues = totalLossValues + cell.contents[0] + ', '
            for cell in frameDamageCells:
                frameDamageValues = frameDamageValues + cell.contents[0] + ', '
            for cell in airbagCells:
                airbagValues = airbagValues + cell.contents[0] + ', '
            for cell in odometerCells:
                odometerValues = odometerValues + cell.contents[0] + ', '
            for cell in accidentCheckCells:
                accidentCheckValues = accidentCheckValues + cell.contents[0] + ', '
            for cell in recallCells:
                recallValues = recallValues + cell.contents[0] + ', '


            # totalLossCells = additionalHistoryTable.find("div", id=re.compile("^totalLossCol")).text
            # frameDamageCells = additionalHistoryTable.find("div", id=re.compile("^frameDamageCol")).text
            # airbagCells = additionalHistoryTable.find("div", id=re.compile("^airbagCol")).text
            # odometerCells = additionalHistoryTable.find("div", id=re.compile("^odometerCol")).text
            # accidentCheckCells = additionalHistoryTable.find("div", id=re.compile("^accidentCheckCol")).text
            # recallCells = additionalHistoryTable.find("div", id=re.compile("^recallCol")).text

            carfax_info = [vin, totalLossValues, frameDamageValues, airbagValues, odometerValues, accidentCheckValues, recallValues,
                           carfax_html, countryOriginValues]

            carfax_data = carfax_info  # set carfax_data equal to carfax_info so it can be passed to outer function

            time.sleep(1)
            browser.get('https://www.carfaxonline.com/')


            # current_vin_location = list(curated_vin_list).index(vin) # convert the vin ndarray to a list then retrieve index of current vin
            current_vin_location = list(curated_vin_list).index(vin)
            vin_counter = current_vin_location

            # just update the dataframe
            carfax_2_dataframe = modifyCarfaxDataframe(carfax_2_dataframe, carfax_info)

            '''with open(vin_location_txt, 'w') as file:

                if vin_counter == len(list(curated_vin_list)) - 1:  # if we reach the end of the list set the vin counter back to 0
                    vin_counter = 0
                    file.write(str(vin_counter))
                    file.close()
                else:
                    file.write(str(vin_counter))  # write the last position of the vin before the crash
                    file.close()
                    set_with_dataframe(carfax_2_sheet, carfax_2_dataframe)
                    time.sleep(15)
                    get_carfax_infoMMC()  # run the function again'''

        current_vin_location = 0  # if the try statement reaches the end of the list without fail, set the location back to 0

    except Exception as error:
        # if there is a problem update the dataframe with the values that have been found so far
        print(error)
        print('Exception has occurred, saving the current vins location to continue from next time')
        print("THE INDEX OF THE LAST SUCCESSFULLY PROCESSED VIN IS: %s " % current_vin_location)

        with open(vin_location_txt, 'w') as file:

            if vin_counter == len(list(curated_vin_list)) - 1:  # if we reach the end of the list set the vin counter back to 0
                vin_counter = 0
                file.write(str(vin_counter))
                file.close()
            else:
                file.write(str(vin_counter))  # write the last position of the vin before the crash
                file.close()
                set_with_dataframe(carfax_2_sheet, carfax_2_dataframe)
                time.sleep(15)
                get_carfax_infoMMC()  # run the function again

        set_with_dataframe(carfax_2_sheet, carfax_2_dataframe)
        time.sleep(5)

    set_with_dataframe(carfax_2_sheet, carfax_2_dataframe)


    #post_to_api = api_call(carfax_data)  # automatically POST the data we just scraped to the API
    #print(post_to_api.status_code)


def modifyCarfaxDataframe(dataframe, info_array):
    pandas_df = dataframe
    vin = info_array[0]
    totalloss = info_array[1]
    structural = info_array[2]
    airbag = info_array[3]
    odometer = info_array[4]
    accident = info_array[5]
    recall = info_array[6]
    origin = info_array[8]

    if np.sum(pandas_df["UNIV KEY"] == vin) >= 1:  # if the VIN is found
        print('found')
        print(vin)

        pandas_df.loc[pandas_df['UNIV KEY'] == vin, ['carfax StructuralDamage', "carfax Totalloss",	"carfax accident",	"carfax airbags",	"carfax odometer",	"carfax recall"	,"last updated", "origin"]] = [structural,totalloss,accident,airbag,odometer,recall,datetime.datetime.now(), origin]
        # print(pandas_df.loc[pandas_df['UNIV KEY'] == vin, ['carfax StructuralDamage', "carfax Totalloss",	"carfax accident",	"carfax airbags",	"carfax odometer",	"carfax recall"	,"last updated"]])
    else:
        print('append')
        print(vin)
        # pandas_df = pandas_df.append([' ',vin,' ', structural,totalloss,accident,airbag,odometer,recall,datetime.datetime.now()], ignore_index=True)  # ignore index so it appends at bottom

        pandas_df2 = pd.DataFrame([[' ', vin, ' ', structural, totalloss, accident, airbag, odometer, recall, datetime.datetime.now(), origin]], columns=['RUN #', 'UNIV KEY', 'YEAR', 'carfax StructuralDamage',  'carfax Totalloss', 'carfax accident', 'carfax airbags', 'carfax odometer', 'carfax recall', 'last updated', 'origin'])
        pandas_df = pandas_df.append(pandas_df2, ignore_index=True)  # ignore index so it appends at bottom

        if vin in pandas_df['UNIV KEY'].values:
            print("NEW VIN: %s APPENDED" % vin)

    return pandas_df


if __name__ == "__main__":
    print(get_carfax_infoMMC())







