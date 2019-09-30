import requests
import urllib3
import os
from urllib.request import urlopen 
from bs4 import BeautifulSoup
import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
from pywebcopy import save_webpage
browser = webdriver.Firefox()

def signIn():
    usernameStr = 'Sharon Hanna'
    passwordStr = '0re02oo2'  
    browser.get('https://doh.arcabc.ca/user/login')
    # fill in username and hit the next button
    username = browser.find_element_by_id('edit-name')
    username.send_keys(usernameStr)
    password = browser.find_element_by_id('edit-pass')
    password.send_keys(passwordStr)
    signInButton = browser.find_element_by_id('edit-submit')
    signInButton.click()
    print("signed in!")



startPage = "https://doh.arcabc.ca/islandora/object/news%3A1255"
signIn() #sign into Arca    
#count = 0
objURLs = []
dirName = "ProspectorXML"
savePath = r'C:/Users/sharo/Desktop' + '/' + dirName + '/'       
if not os.path.exists(savePath):    #if folder does not exist
    os.makedirs(savePath)           #create it
browser.get(startPage) 
source = browser.page_source
bs = BeautifulSoup(source, "html.parser")

links = bs.select("div.islandora-newspaper-object a")
for ou in links:
    if 'class' not in ou.attrs:
        lnk = str(ou)[34:]
        print(lnk)
        end = lnk.find(">") - 1
        num = lnk[:end]
        if (num.isdigit()):
            objU = r"https://doh.arcabc.ca/islandora/object/news%3A" + num + "/" + r"datastream/MODS/view#overlay-context=islandora/object/news%253A" + num
            objURLs.append([objU, num])
for u in objURLs:
    print(u)   
    http = urllib3.PoolManager()
    r = http.request('get', u[0])
    fname = savePath + "news_" + u[1] + ".xml"
    with open(fname, 'wb') as fid:
        fid.write(r.data)      

#for lnk in bs.select("div.islandora-newspaper-object  a"):
    #if "fieldset" not in lnk.text:
    #print(repr(lnk))
# print(objURLlist)
# begStr = '<a href="/islandora/object/news%3A'
# beg = len(begStr)
# # **********************************************   
# for u in objURLlist:
#     end = len(u) - 1
#     num = u[beg:end]
#     print("Num is " + num)
#     if (num.isdigit()):
#         objNums.append(num)
#     print(objNums)
    # *************************************************** check for Robinson #s coming out as A25, etc. (instead of 25)
#         for num in objNums:
#             try: 
#                 url = r'https://doh.arcabc.ca/islandora/object' + '/' + repNm + '%3A'
#                 addr = url + num + r'/datastream/MODS/version/0/view'
#                 filename = repNm + '_' + num + '_MODS.xml'
#                 completeNm = savePath + r'/' + filename
#                 print(completeNm)
#                 browser.get(addr)
#                 source = browser.page_source
#                 bs = BeautifulSoup(source, "xml") 
#                 print(bs.encode('utf8'))
#                 with open(completeNm, 'w') as file:
#                     file.write(str(bs.encode('utf8')))
#                 count += 1
#             except NoSuchElementException:
#                 print("Broke at " + repNm + ":" + num)
#                 continue    
#     print(str(count) + " XML records were written to " + str(savePath) + ".")
        