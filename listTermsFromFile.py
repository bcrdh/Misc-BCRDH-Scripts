from bs4 import BeautifulSoup
import sys
import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import time


topSubs = []
#authNms = []
count = 0

for filename in glob.iglob('C:\\Users\sharon\Desktop\AllDOHMods_Mar2419\**\*.xml', recursive=True):
    print(filename)
    fnms = filename.split('\\')
    objIDpts = fnms[6].split("_")
    repo = objIDpts[0]
    num = objIDpts[1]
    print("repo: " + repo + "; num: " + num)
    infile = open(filename,"r",encoding="utf8")
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')

    topics = soup.find_all('topic')
    if topics:
        for topic in topics:
            topStr = topic.getText().rstrip().strip()
            if topStr not in topSubs:
                topSubs.append(topStr)
topSubs.sort()
#authNms.sort()
for top in topSubs:
    print(top)
#for nm in authNms:
#    print(nm.encode(sys.stdout.encoding, errors='replace'))
#print("name count is " + str(count))


 
