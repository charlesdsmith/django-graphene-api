import json
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from gspread import exceptions
import os
import pandas as pd

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def startAuthorization():
    # json_key = json.load(open('client_secret.json')) # json credentials you downloaded earlier
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('sheets_credentials.json', scope)
    gc = gspread.authorize(credentials)
    return gc

def startWorksheet(gc):

    sh = gc.open_by_key("1TYzzMvKJ5aO0dK_0ereV-0iC_qQTI_3fXFWyPdrr5Zk")
    #sh = gc.open("ECI" + year + 'TESTING')      ###TEST SANDBOX DEVELOPER

    wksh = sh.worksheet("AdesaLivePurchaseList")

    return wksh

def startDetailsWorksheet(gc):
    try:
        today = datetime.date.today()
        year = today.strftime("%Y")
        mnthYear = today.strftime("%b %Y")

        sh = gc.open("EXPORTED CAR INFO IN DETAILS 2017")  ###PRODUCTION

        wksh = sh.worksheet('Purchase 2017')
    except exceptions.APIError:
        startDetailsWorksheet(startAuthorization())
    return wksh

def startTradeRevWorksheet(gc,sheetName):
    try:

        # sh = gc.open("TradeRev master")  ###PRODUCTION
        sh = gc.open_by_key("1ogulqanvyvCGwlhQWlPH3ZkL5lctvq-aR-k_sgCGAEk")

        wksh = sh.worksheet(sheetName)
        print('starting gc traderev ' + sheetName)
    except exceptions.APIError as err:
        print(err)
        startTradeRevWorksheet(startAuthorization(), sheetName)
    return wksh

def createNewWorksheet(gc, wksh_name):
    #use the key for the spreadsheet in the URL
    sh = gc.open_by_key("1thFN6-GHziJ2uDK6-zgULZQ_0kMYRsfz2ES0bOfZbro")

    wksh = sh.add_worksheet(wksh_name)

    return wksh


def startShortWorksheet(gc, carSaleDate=None):
    #use the key for the spreadsheet in the URL
    sh = gc.open_by_key("1thFN6-GHziJ2uDK6-zgULZQ_0kMYRsfz2ES0bOfZbro")
    #sh = gc.open("ECI" + year + 'TESTING')      ###TEST SANDBOX DEVELOPER

    #for testing
    carSaleDate='Aug2018Test'
    #reformatteddate = date.today().strftime('%h') + str(date.today().year) + 'Test'
    wksh = sh.worksheet(carSaleDate)


    return wksh

def startRegistrationsFriday(gc):
    sh = gc.open_by_key("1hsza_XgUcmVRJ5a2IWG01l69iKEDddr2kPdAQALcUyc")

    wksh = sh.worksheet('Registrations Friday')

    return wksh

def startCarfaxSheet(gc):
    sh = gc.open_by_key("1hsza_XgUcmVRJ5a2IWG01l69iKEDddr2kPdAQALcUyc")

    wksh = sh.worksheet("CARFAX2")

    return wksh