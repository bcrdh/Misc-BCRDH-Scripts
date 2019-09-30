from bs4 import BeautifulSoup
import sys
import glob
from bs4 import BeautifulSoup 
import time





noKD = []
#authNms = []
count = 0
for filename in glob.iglob(r'C:\\Users\sharo\Desktop\AllDOHMods_Mar2419\**\*.xml', recursive=True):
    fnms = filename.split('\\')
    objIDpts = fnms[7].split(".")
    name = objIDpts[0].replace("_MODS","")
    name = name.replace("_",":")
    #print("repo: " + repo + "; num: " + num)
    infile = open(filename,"r",encoding="utf8")
    contents = infile.read()
    soup = str(BeautifulSoup(contents,'xml'))
    if (soup.find('keyDate="yes"')==-1):
        noKD.append(name)
        count = count + 1
        
noKD.sort()
#authNms.sort()
for n in noKD:
    print(n)
print(str(count) + "records have no keydate")