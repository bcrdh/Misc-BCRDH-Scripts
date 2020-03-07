#Updates object label in Arca
#Used when putting a new photo into the slideshow carousel on BCRDH home page or taking it out
#Edits (putting date issued into title for slideshow photo) are done in XML manually, not by this script 
#Input = folder of MODS XML

import glob
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webelement import FirefoxWebElement
#browser = webdriver.Chrome()
browser = webdriver.Firefox()
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

def updateLabel(filepath, browser, repo, num):
    #import time
    from bs4 import BeautifulSoup
    
    #get title from XML file
    infile = open(filepath,"r",encoding="utf8")
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')
    title=soup.find('title').get_text().strip()
    
    per3A = r'%3A'
    updateProp = r'https://doh.arcabc.ca/islandora/object/' + repo + per3A + num + r'#overlay=islandora/object/' + repo + per3A + num + '/manage/properties'

    #get the lock
    modsEdit = "https://doh.arcabc.ca/islandora/edit_form/" + repo + per3A + num + "/MODS"
    browser.get(modsEdit)
    browser.get(updateProp)
    #iframe = browser.find_element_by_css_selector("iframe")
    #iframe.click()
#     size = len(browser.find_elements_by_tag_name("iframe"))
#     print("There are " + str(size) + " iframes.")
    browser.switch_to.frame(2)  
    label = browser.find_element_by_css_selector("input#edit-object-label") 
    label.clear() #delete current label
    label.send_keys(title) #insert title into label field
    subm = browser.find_element_by_id("edit-submit")
    subm.click()

# adjust to accommodate source XML folder
for filename in glob.iglob(r'C:\\Users\sharo\Desktop\WAH_1819\RepoCorrections\**.xml', recursive=True):
    fnms = filename.split('\\')
    objIDpts = fnms[7].split("_")
    repo = objIDpts[0]
    num = objIDpts[1].split(".")[0]
    updateLabel(filename, browser, repo, num)
