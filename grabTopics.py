 import sys
from urllib.request import urlopen 
from bs4 import BeautifulSoup
topSubs = []
#repolist = ['arms:armsmin','arms:photographs', 'arms:spallmin','enderby:inland', 'enderby:photographs','ssm:keremeos']
#repolist2 = ['lake:goulding','lake:photographs','lumby:photographs','okeefe:lantern','okeefe:photographs','osoyoos:photographs']
#repolist3 = ['peach:photographs','sicamous:photographs','ssm:keremeos','summer:photographs']

#allRepos = repolist + repolist2 + repolist3
#allRepos = ['naramata:photographs', 'peach:buildings', 'peach:assessment']

allRepos = ['okfalls:photographs']

def my_filter(tag):
        return(tag.name=="a" and
               tag.parent.name=="dt" and
               "islandora-object-thumb" in tag.parent["class"])

def getObjNums():
        for a in bs.find_all(my_filter):
            objURLlist.append(str(a))

for i in range(len(allRepos), 0, -1):
    count = 0
    rep = allRepos[i-1]
#    print(rep)
    objURLlist = []
    objNums = []
    collNm = ""
    repNm = ""
    
    repNm = rep.split(":")[0]
#    print(repNm)
    collNm = rep.split(":")[1]
#    print(collNm)

    baseURL = r"https://doh.arcabc.ca/islandora/object" + '/' + repNm + "%3A" + collNm
   
    html = urlopen(baseURL) 
    bs = BeautifulSoup(html.read(), "lxml") 
    
    lstPgLnk = bs.find('li',class_="pager-last last")
#    print(lstPgLnk)
    if lstPgLnk is None:
        last = 0
    else:
        lstPgStr = str(lstPgLnk)
#        print(lstPgStr.find("page="))
        beg = lstPgStr.find("page=") + 5
        end = lstPgStr.find("title=") - 2
        lastP = lstPgStr[beg:end]
        last = int(lastP)
        
    for i in range(0, last + 1):
        if i == 0:
            getObjNums()
        else:
            currURL = baseURL + "?page=" + str(i)
#            print(currURL)
            htm = urlopen(currURL) 
            bs = BeautifulSoup(htm.read(), "lxml") 
            getObjNums()
#    print("length of obj url list is " + str(len(objURLlist)))
    begStr = '<a href="/islandora/object/' +  repNm + r'%3A'
    beg = len(begStr)
#    print("beginning is " + str(beg))
#    print("end is " + str(end))
    for u in objURLlist:
#        print("orig url is " + u)
        end = int(u.find("title=") - 2) 
        num = u[beg:end]
        objNums.append(num)
#    print(objNums)
        
    for num in objNums:
        if collNm == 'robinson':
            repNm = 'islandora'
        url = r'https://doh.arcabc.ca/islandora/object' + '/' + repNm + '%3A'
        addr = url + num + r'/datastream/MODS/view#overlay-context=islandora/object' + '/' + repNm + '%253A' + num + '.xml'
        html2 = urlopen(addr) 
        bs2 = BeautifulSoup(html2.read(), "lxml")
        topics = bs2.find_all('topic')
        if topics:
            for topic in topics:
                topStr = topic.getText().rstrip().strip()
                if topStr not in topSubs:
                    topSubs.append(topStr)
    
topSubs.sort()
#authNms.sort()
for top in topSubs:
    print(top)

