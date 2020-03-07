#Given a list of PIDs, downloads MODS XML from Arca

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
import urllib3
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


def download(pidlist):
    signIn() #sign into Arca    
    for i in range(len(pidlist), 0, -1):
        count = 0
        pid = pidlist[i-1]
        dirName = ""
        repNm = ""
        repNm = pid.split(":")[0]
        print(repNm)
        num = pid.split(":")[1]
   
        dirName = repNm
       
        #baseURL = r"https://doh.arcabc.ca/islandora/object" + '/' + repNm + "%3A" + collNm
        savePath = r'C:/Users/sharo/Desktop' + '/' + dirName + '/'       
        if not os.path.exists(savePath):    #if folder does not exist
            os.makedirs(savePath)           #create it
        #https://doh.arcabc.ca/islandora/object/sicamous%3A1139/datastream/MODS/view#overlay-context=islandora/object/sicamous%253A1247
        http = urllib3.PoolManager()
        #a href="https://doh.arcabc.ca/islandora/object/sicamous%3A1715/datastream/MODS/view"
        objU = r'https://doh.arcabc.ca/islandora/object' + '/' + repNm + '%3A' + num + '/' + r'datastream/MODS/view'
        r = http.request('get', objU)
        fname = savePath + repNm + "_" + num + ".xml"
        with open(fname, 'wb') as fid:
            fid.write(r.data)
            count += 1
    print(str(count) + " XML records were written to " + str(savePath) + ".")
        
download(['sicamous:818', 'sicamous:736', 'sicamous:736', 'sicamous:1120', 'sicamous:973', 'sicamous:958', 'sicamous:972', 'sicamous:971', 'sicamous:980', 'sicamous:974', 'sicamous:972', 'sicamous:971', 'sicamous:980', 'sicamous:1275', 'sicamous:1276', 'sicamous:1260', 'sicamous:1161', 'sicamous:1261', 'sicamous:1173', 'sicamous:1242', 'sicamous:1240', 'sicamous:1241', 'sicamous:1268', 'sicamous:1239', 'sicamous:1243', 'sicamous:1192', 'sicamous:1197', 'sicamous:1159', 'sicamous:1204', 'sicamous:1141', 'sicamous:1215', 'sicamous:1182', 'sicamous:1183', 'sicamous:1181', 'sicamous:1217', 'sicamous:1218', 'sicamous:1178', 'sicamous:1207', 'sicamous:1253', 'sicamous:1175', 'sicamous:1258', 'sicamous:1200', 'sicamous:1138', 'sicamous:1208', 'sicamous:1199', 'sicamous:1274', 'sicamous:1273', 'sicamous:1283', 'sicamous:1186', 'sicamous:1193', 'sicamous:1190', 'sicamous:1155', 'sicamous:1139', 'sicamous:1226', 'sicamous:1177', 'sicamous:1171', 'sicamous:1147', 'sicamous:1257', 'sicamous:1163', 'sicamous:1189', 'sicamous:1191', 'sicamous:1185', 'sicamous:1205', 'sicamous:1222', 'sicamous:1206', 'sicamous:1143', 'sicamous:1160', 'sicamous:1248', 'sicamous:1246', 'sicamous:1249', 'sicamous:1247', 'sicamous:1245', 'sicamous:1263', 'sicamous:1196', 'sicamous:1145', 'sicamous:1250', 'sicamous:1251', 'sicamous:1184', 'sicamous:1219', 'sicamous:1233', 'sicamous:1229', 'sicamous:1230', 'sicamous:1165', 'sicamous:1172', 'sicamous:1144', 'sicamous:1214', 'sicamous:1180', 'sicamous:1235', 'sicamous:1220', 'sicamous:1221', 'sicamous:1234', 'sicamous:1156', 'sicamous:1231', 'sicamous:1176', 'sicamous:1264', 'sicamous:1265', 'sicamous:1213', 'sicamous:1252', 'sicamous:1254', 'sicamous:1179', 'sicamous:1150', 'sicamous:1140', 'sicamous:1224', 'sicamous:1225', 'sicamous:1244', 'sicamous:1267', 'sicamous:1195', 'sicamous:1227', 'sicamous:1166', 'sicamous:1168', 'sicamous:1154', 'sicamous:1194', 'sicamous:1187', 'sicamous:1202', 'sicamous:1174', 'sicamous:1259', 'sicamous:1198', 'sicamous:1157', 'sicamous:1158', 'sicamous:1266', 'sicamous:1209', 'sicamous:1188', 'sicamous:1162', 'sicamous:1269', 'sicamous:1270', 'sicamous:1271', 'sicamous:1167', 'sicamous:1272', 'sicamous:1201', 'sicamous:1262', 'sicamous:1228', 'sicamous:1151', 'sicamous:1169', 'sicamous:1142', 'sicamous:1211', 'sicamous:1223', 'sicamous:1203', 'sicamous:1164', 'sicamous:1170', 'sicamous:1148', 'sicamous:1715'])
#, 'princeton:949', 'princeton:963', 'princeton:965', 'princeton:966', 'princeton:967', 'princeton:968', 'princeton:943', 'princeton:404', 'osoyoos:881', 'osoyoos:416', 'peach:1023', 'peach:754', 'greenwood:3387', 'greenwood:3945', 'greenwood:3663', 'greenwood:2938', 'greenwood:3249', 'greenwood:2894', 'greenwood:3446', 'greenwood:2929', 'greenwood:2929', 'greenwood:2915', 'greenwood:3496', 'greenwood:3495', 'greenwood:3411', 'greenwood:3027', 'greenwood:3112', 'greenwood:3060', 'greenwood:3407', 'greenwood:2928', 'greenwood:3323', 'greenwood:2920', 'greenwood:3051', 'greenwood:3651', 'greenwood:3649', 'greenwood:3932', 'greenwood:2922', 'greenwood:2921', 'greenwood:3279', 'greenwood:3032', 'greenwood:2895', 'fintry:2302', 'fintry:2408', 'fintry:2513', 'fintry:2618', 'fintry:2723', 'fintry:1014', 'fintry:1122', 'fintry:1227', 'fintry:3154', 'fintry:1441', 'fintry:1549', 'fintry:1659', 'fintry:1764', 'fintry:1869', 'fintry:1975', 'fintry:2082', 'fintry:2194', 'fintry:2300', 'boundary:81', 'boundary:77', 'boundary:74', 'boundary:78', 'boundary:72', 'boundary:84', 'boundary:75', 'boundary:79', 'boundary:82', 'boundary:76', 'boundary:67', 'boundary:68', 'boundary:70', 'boundary:71', 'boundary:69', 'boundary:73', 'boundary:80', 'boundary:83'])
