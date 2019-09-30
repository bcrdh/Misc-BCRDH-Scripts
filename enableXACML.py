from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

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
    
    
def selectMult(selecList):
    for item in selecList:
        ActionChains(browser).key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()

    
browser = webdriver.Chrome()
signIn(browser)
url = "https://doh.arcabc.ca/islandora/object/osoyoos%3Aofb/manage/xacml?render=overlay"
browser.get(url)

#Tick box
result = browser.find_element_by_id("edit-access-enabled").is_selected();
if result:
    print('Checkbox already selected')
else:
    browser.find_element_by_id("edit-access-enabled").click();
    print('Checkbox selected')

usrs = []
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='brandonw']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='Chris Hives']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='dgiadmin']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='dimnamkhao']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='eamonrs']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='ehomolka']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='paigeh']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='Sharon Hanna']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='sunnin']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='KaylaHilstob']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='Kayla Hilstob']"))
usrs.append(browser.find_element_by_xpath("//select[@name='access[users][]']/option[text()='Sharon Hanna']"))

# for usr in usrs:
#     ActionChains(browser).key_down(Keys.CONTROL).click(usr).key_up(Keys.CONTROL).perform

selectMult(usrs)

roles = [] 
roles.append(browser.find_element_by_xpath("//select[@name='access[roles][]']/option[text()='administrator']"))
roles.append(browser.find_element_by_xpath("//select[@name='access[roles][]']/option[text()='IR staff']"))
roles.append(browser.find_element_by_xpath("//select[@name='access[roles][]']/option[text()='Local administrator']"))
roles.append(browser.find_element_by_xpath("//select[@name='access[roles][]']/option[text()='repositories']"))

selectMult(roles)
# for role in roles:
#     ActionChains(browser).key_down(Keys.CONTROL).click(role).key_up(Keys.CONTROL).perform

#select = browser.find_element_by_id('edit-update-options')
# select = browser.find_element_by_xpath("//select[@name='update_options']/option[@value='newchildren']")
# select by visible text
#select.select_by_visible_text('Banana')

# select.click()

select = Select(browser.find_element_by_xpath("//select[@name='update_options']"))
select.select_by_value('all_children')
print("all children selected")
 
setPerm = browser.find_element_by_id('edit-submit')
setPerm.click()
print('permissions set')
 
print('XACML has been enabled')

