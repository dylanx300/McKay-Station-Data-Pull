# McKay Station Penobscot River Pull
#imports modules: Requests, MySQL Connector, BeautifulSoup, Datetime
from bs4 import BeautifulSoup
import datetime
import mysql.connector
import unicodedata
import logging
#import re
#import csv
#from tabulate import tabulate
#import smtplib, ssl
#import sys

### DELETE BEFORE UPLOAD TO GITHUB ###
ipAddr = 'xxx'
uName = 'xxx'
psWd = 'xxx'
### ------------------------------ ###

logging.basicConfig(filename='/home/pi/Desktop/Logs/SystemdPython/McKay.log',filemode='a',level=logging.DEBUG)
logging.info("Starting notifier service at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
siteURL = ('https://safewaters.com/facility/mckay-ripogenus')

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
driver.get(siteURL)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

tstStr = soup.find("div",class_="singlefacleftdetails")
str2 = tstStr.li.h1.text
flowVal = int(''.join(filter(str.isdigit, str2)))
print (flowVal)
driver.close()

tstList2 = soup.find("div",class_="mt-4").find_all("div")
clnList2 = []
clnStr = ""
for i in tstList2:
    clnStr += unicodedata.normalize('NFKD',i.text)

schList = soup.find("table",class_="tbSchedule").find_all("td")
fSch = int(schList[2].text)

def runSQL_insert():
    mydb = mysql.connector.connect(
      host=ipAddr, #192.168.1.54 / 66 / 11
      user=uName,
      passwd=psWd,
      database="McKayStationData")

    mycursor = mydb.cursor()

    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cleanList = [dt,flowVal,fSch,clnStr]

    inssql = """
    INSERT INTO HistoricalFlows
    VALUES (%s, %s, %s, %s)"""
    val = cleanList
    mycursor.execute(inssql, val)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
    mycursor.close()
    mydb.close()

if type(flowVal) == int or float:
    runSQL_insert()
else:
    pass

