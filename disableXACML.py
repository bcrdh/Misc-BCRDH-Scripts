#NON-WORKING
#Purpose is to change XACML to disable or enable (i.e. toggle) viewing access for public to a file
#Originally used with a previous Downloader version

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

def signIn(browser):
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

def disableXACML(repo,coll):
    browser = webdriver.Chrome()
    signIn(browser)
    url = r"https://doh.arcabc.ca/islandora/object/" + repo + r"%3A" + coll + r"/manage/xacml?render=overlay"
    browser.get(url)

    #Deselect checkbox only when it is selected 
    result = browser.find_element_by_id("edit-access-enabled").is_selected();
    if result:
        browser.find_element_by_id("edit-access-enabled").click()
        browser.find_element_by_id("edit-submit").click()
        print('Checkbox deselected')
        select = Select(browser.find_element_by_id('edit_update_options'))
        select.select_by_value('all_children')
        print("all children selected")
    
        setPerm = browser.find_element_by_id('edit-submit')
        setPerm.click()
        print('permissions set')
        print('XACML has been disabled')
    else:
        print('Checkbox already deselected')

disableXACML("arms","photographs")
