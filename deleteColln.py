#deletes entire specified Arca collection
#use with care!

import requests
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


def deleteCollection():
    
    repolist = ['boundary:oralhistory','arms:oralhistory']
    
    def my_filter(tag):
            return(tag.name=="a" and
                   tag.parent.name=="dt" and
                   "islandora-object-thumb" in tag.parent["class"])

    def getObjNums():
            for a in bs.find_all(my_filter):
                objURLlist.append(str(a))
    
    signIn() #sign into Arca    
    for i in range(len(repolist), 0, -1):
        rep = repolist[i-1]
        objURLlist = []
        objNums = []
        collNm = ""
        repNm = ""
        repNm = rep.split(":")[0]
        print(repNm)
        collNm = rep.split(":")[1]
        print(collNm)
        baseURL = r"https://doh.arcabc.ca/islandora/object" + '/' + repNm + "%3A" + collNm
        browser.get(baseURL)
        source = browser.page_source
        bs = BeautifulSoup(source, "html.parser")
        lstPgLnk = bs.find('li',class_="pager-last last")
        print(lstPgLnk)
        if lstPgLnk is None:    #if collection has only 1 page
            last = 0
        else:
            lstPgStr = str(lstPgLnk)
            print(lstPgStr.find("page="))
            beg = lstPgStr.find("page=") + 5
            end = lstPgStr.find("title=") - 2
            lastP = lstPgStr[beg:end]
            print("last page is" + lastP)
            last = int(lastP)
            
        for i in range(0, last + 1):
            if i == 0:          #if on first page of collection
                getObjNums()
            else:
                currURL = baseURL + "?page=" + str(i)
                browser.get(currURL)
                source = browser.page_source
                bs = BeautifulSoup(source, "html.parser") 
                getObjNums()    
        begStr = '<a href="/islandora/object/' +  repNm + r'%3A'
        beg = len(begStr)
    # **********************************************   
        for u in objURLlist:
            end = int(u.find("title=") - 2) 
            num = u[beg:end]
            print("Num is " + num)
            if (num.isdigit()):
                objNums.append(num)
        print(objNums)
    # *************************************************** 
        for num in objNums:
            try: 
                url=r'https://doh.arcabc.ca/islandora/object' + '/' + repNm + '%3A616#overlay=islandora/object/' + repNm + '%253A' + num
                url += '/manage/datastreams/locking/lock%3Fdestination%3Dislandora/object' + "/" + repNm + '%253A' + num + '/' + 'manage/properties'
                browser.get(url)
                #browser.find_element_by_css_selector(css_selector)('#edit-submit')
                confirm = browser.find_element_by_css_selector('div#input#edit-submit.form-submit')
                confirm.click()
                remove = browser.find_element_by_id('edit-delete')
                remove.click()
                delete = browser.find_element_by_id('edit-submit')
                delete.click()
                
            except NoSuchElementException:
                print("Broke at " + repNm + ":" + num)
                continue    
    print("All records have been deleted!")
        
deleteCollection()
