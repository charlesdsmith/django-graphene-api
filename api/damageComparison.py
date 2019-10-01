# graphql call to retrieve all records from damage comparisons table

# first get all he records from the table
import json
import requests
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
import requests


def getAllDamageComparisons():

    headers = {
        'Authorization': 'Bearer jAL8mDIwpm7Pqk7BUtelsgW3jIFUkO',
        "Content-Type": "application/json",

    }

    data = {
        "query": """query getDamagedCars{
  allDamageComparisonObjects{
      vin
      id
         }
    }""",
    }

    data = json.dumps(data)

    #response = requests.post("http://localhost:3000/graphql", headers=headers, data=data)
    response2 = requests.post("https://gsm-django.herokuapp.com/graphqlui", headers=headers, data=data)

    allDamagedCars = [[car["vin"], car["id"]] for car in json.loads(response2.text)["data"]["allDamageComparisonObjects"]]
    return allDamagedCars

import codecs
def updateDamageComparisons(car_info=None):
    test1 = [['RGFtYWdlQ29tcGFyaXNvblR5cGU6Mw==', ['5UXFG2C53BLX09045', 'No Issues Reported, ', 'No Issues Reported, ', 'No Issues Reported, ', 'Mileage Inconsistency, ', 'No Issues Reported, ', 'No Recalls Reported, ', '\n \n Service Facility\n \n ,\n \n \n Mississauga, ON\n \n \n \n \n ']], ['RGFtYWdlQ29tcGFyaXNvblR5cGU6NA==', ['WDCGG8HB4AF472595', 'No Issues Reported, ', 'No Issues Reported, ', 'No Issues Reported, ', 'No Issues Indicated, ', 'No Issues Reported, ', 'No Recalls Reported, ', '\n \n Quebec\n \n ,\n \n \n Motor Vehicle Dept.\n \n ,\n \n \n Sainte-Anne-des-Lacs, QC\n \n \n \n \n ']]]

    test = [['RGFtYWdlQ29tcGFyaXNvblR5cGU6MA==', ['1FTFW1EG4HFA67794', 'No Issues Reported, No Issues Reported, ', 'No Issues Reported, No Issues Reported, ', 'No Issues Reported, No Issues Reported, ', 'No Issues Indicated, No Issues Indicated, ', 'No Issues Reported, No Issues Reported, ', 'No New Recalls Reported, Recall Reported, ', '\n \n Sherlock\n \n ,\n \n \n Antitheft Marking\n \n ,\n \n \n \n sherlock.ca\n \n \n \n ']]]
    for car in car_info:
        car[0] = codecs.encode(car[0], encoding='ascii', errors='strict')
        car[0] = str(codecs.decode(car[0], encoding='base64', errors='strict'))
        car[0] = car[0].replace('b', '').replace("DamageComparisonType:", '').replace("'", "")
        print("CAR", car)


    headers = {
        'Authorization': 'Bearer jAL8mDIwpm7Pqk7BUtelsgW3jIFUkO',
        "Content-Type": "application/json",

    }

    data = {
        "query": """mutation updateDamage($car_info:[[String]]){
  updateDamageComparison(args:{carInfo:$car_info}){
      ok
      response
         }
    }""",
        "variables": {"car_info": car_info},
    }

    data = json.dumps(data)
    response = requests.post("http://localhost:3000/graphqlui", headers=headers, data=data)
    #response2 = requests.post("https://gsm-django.herokuapp.com/graphqlui", headers=headers, data=data)

    print(response.content)
    return response


def get_carfax_infoMMC():
    chromedriver = 'C:/Users/User/Desktop/chromedriver.exe'

    #create a chrome object
    browser = webdriver.Chrome(executable_path=chromedriver)
    browser.get('https://www.carfaxonline.com/login')


    username = browser.find_element_by_css_selector("input[type='text']")
    password = browser.find_element_by_css_selector("input[type='password']")

    username.send_keys("sencoreent@gmail.com")
    password.send_keys("7102677Se")

    browser.find_element_by_id("login_button").click()
    wait = WebDriverWait(browser, 3)
    wait_for_dashboard = wait.until(EC.url_to_be("https://www.carfaxonline.com/"))

    # a list of lists that contain each car's id and vin
    id_list = [car[1] for car in getAllDamageComparisons()[:1]]
    # get list of vins of damaged cars
    vin_list = [car[0] for car in getAllDamageComparisons()[:1]]

    print("ID LIST", id_list)
    print("VIN LIST", vin_list)
    print("VIN LIST LENGTH:", len(vin_list))

    vin_location_txt = r"C:\Users\User\Documents\Heroku\gsm-django\carfax\vin_location.txt"

    current_vin_location = open(vin_location_txt, 'r').readlines()[0]
    print(current_vin_location)
    vin_counter = 0
    carfax_data = []  # this will store the 6 values and be returned by the function to use in api calls

    try:
        print("INDEX OF VIN BEING PROCESSED: %s " % current_vin_location)
        for i, vin in enumerate(vin_list[int(current_vin_location):]):  # range(curated_vin_list[current_vin_location], len(curated_vin_list) - 1):

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

            carfax_info = [vin, totalLossValues, frameDamageValues, airbagValues, odometerValues, accidentCheckValues, recallValues, countryOriginValues]

            print("carfax info", carfax_info)
            carfax_data.append([id_list[i], carfax_info])

            #carfax_data = carfax_info  # set carfax_data equal to carfax_info so it can be passed to outer function

            print("CARFAX DATA", carfax_data)

            time.sleep(1)
            browser.get('https://www.carfaxonline.com/')


            # current_vin_location = list(curated_vin_list).index(vin) # convert the vin ndarray to a list then retrieve index of current vin
            current_vin_location = list(vin_list).index(vin)
            vin_counter = current_vin_location

        updateDamageComparisons(carfax_data) # after the loop has ended send the array to be update function
        current_vin_location = 0  # if the try statement reaches the end of the list without fail, set the location back to 0

    except Exception as error:
        # if there is a problem update the dataframe with the values that have been found so far
        print(error)
        print('Exception has occurred, saving the current vins location to continue from next time')
        print("THE INDEX OF THE LAST SUCCESSFULLY PROCESSED VIN IS: %s " % current_vin_location)

        with open(vin_location_txt, 'w') as file:

            if vin_counter == len(list(vin_list)) - 1:  # if we reach the end of the list set the vin counter back to 0
                vin_counter = 0
                file.write(str(vin_counter))
                file.close()
            else:
                file.write(str(vin_counter))  # write the last position of the vin before the crash
                file.close()
                time.sleep(15)
                get_carfax_infoMMC()  # run the function again

        time.sleep(5)


if __name__ == '__main__':
    #getAllDamageComparisons()
    #updateDamageComparisons()
    get_carfax_infoMMC()