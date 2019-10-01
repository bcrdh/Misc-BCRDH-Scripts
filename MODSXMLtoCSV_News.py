import os
import pandas as pd
from bs4 import BeautifulSoup
import glob

df = None
col_names = None
genCols =  ['PID','Title','DateRange','Frequency','Abstract','Publisher_Original','Publisher_Location']
genCols += ['Genre','Type','internetMediaType','Subject1_Topic','Subject_Geographic']
genCols += ['Language','AccessIdentifier','LocalIdentifier','Rights']
genCols += ['CreativeCommons_URI','RightsStatement','relatedItem_1','relatedItem_2']

issCols = ['PID','Identifier','IssueTitle','DateCreated','Volume','Issue']

def multiHdgMkr(pt1, num, pt2):
    return(pt1 + str(num) + '_' + pt2)

def convertIss(topDir):
    repo = "news"
    df  = pd.DataFrame(columns = issCols)
    df.append(pd.Series(), ignore_index=True)
    i = 0#counter
    for filename in glob.iglob(os.path.join(topDir, '*.xml')):        
        fnames = filename.split('\\')
        infile = open(filename,"r",encoding="utf8")
        contents = infile.read()
        soup = BeautifulSoup(contents,'xml')
        
        #Arca PID
        pid = fnames[6].replace(".xml","")
        objNum = pid.split("_")[1]
        pid = repo + ":" + objNum
        df.at[i, 'PID'] = pid.strip()

        #Identifier/DateCreated
        
        dateCreated = soup.find('dateIssued').get_text()
        df.at[i,'Identifier']=dateCreated
        df.at[i,'DateCreated']=dateCreated

        #Issue Title
        title=soup.find('title').get_text().strip()
        title = title.replace('Catholic','Canadian')
        print(title)
        df.at[i, 'IssueTitle']=title
        
        #Volume and Issue
        nos = soup.findAll('number')
        vol = nos[0].get_text().strip()
        df.at[i,'Volume']=vol
        iss = nos[1].get_text().strip()
        iss.replace('.0','')
        df.at[i,'Issue']=iss
        i = i + 1
        
    file_name = "Prospector_AllIssues" + ".csv"
    savePath = r'C:/Users/sharo/Desktop/DOH_Collections_CSVs' + '/'
    dest = os.path.join(savePath,file_name)
    df = df.sort_values(by='DateCreated')
    df.to_csv(dest, encoding='utf-8', index=False)
    print("Wrote " + file_name +".")
        
def convertGen(topDir):
    repo = "news"
    df  = pd.DataFrame(columns = genCols)
    df.append(pd.Series(), ignore_index=True)
    i = 0 #counter
    for filename in glob.iglob(os.path.join(topDir, '*.xml')):
        
        fnames = filename.split('\\')

        infile = open(filename,"r",encoding="utf8")
        contents = infile.read()
        soup = BeautifulSoup(contents,'xml')

        #Arca PID
        pid = fnames[7].replace(".xml","")
        objNum = pid.split("_")[1]
        pid = repo + ":" + objNum
        df.at[i, 'PID'] = pid.strip()
    
        title=soup.find('title').get_text().strip()
        df.at[i, 'Title']=title
            
        #abstract    
        abst = soup.find('abstract')
        if abst:
            df.at[i, 'Abstract'] = abst.getText().strip()
        
        #temporal subject
        tsub = soup.find('subject, ')
        
        #topical subject
        toptags = soup.find_all('topic')
        tsc = 0 #topical subject count
        if len(toptags) > 0:
            for top in toptags:
                tsc += 1
                fieldname = multiHdgMkr('Subject', tsc, 'Topic')
                df.at[i, fieldname] = top.getText().strip()

        #geographic subject
        geogSub = soup.find('geographic')
        if geogSub != None:    
            df.at[i, 'Subject_Geographic'] = geogSub.getText().strip()
        
        #genre    
        genre = soup.find('genre')
        if genre != None:
            gen = genre.getText().strip()
        df.at[i, 'Genre'] = gen
        
        #type
        typ = soup.find('typeOfResource')
        if typ != None:
            df.at[i, 'Type'] = typ.get_text().strip()
    
        #internetMediaType
        frmat = soup.find('internetMediaType')
        if frmat != None:
            df.at[i, 'internetMediaType'] = frmat.getText().strip()
        
        #language
        lang = soup.find('languageTerm')
        if lang != None:
            df.at[i, 'Language'] = lang.getText().strip()
    
        #identifiers
        ai = soup.find('identifier',{'type':'access'})
        if ai !=None:
            df.at[i, 'AccessIdentifier'] = ai.getText().strip()
        li = soup.find('identifier',{'type':'local'})
        if li != None:
            df.at[i, 'LocalIdentifier'] = li.getText().strip()

        #rights
        rights = soup.find('accessCondition',{'displayLabel':'Restricted'})
        if rights != None:
            df.at[i, 'Rights'] = rights.getText().strip()
        rightsStmt = soup.find('accessCondition',{'displayLabel':'Rights Statement'})
        if rightsStmt != None:
            df.at[i, 'RightsStatement'] = rightsStmt.getText().strip()
        ccl = soup.find('accessCondition',{'displayLabel':'Creative Commons license'})
        if ccl != None:
            df.at[i, 'CreativeCommons_URI'] = ccl.getText().strip() 
        
        #relatedItem
        df.at[i, 'relatedItem_1'] = "Newspapers"
        df.at[i, 'relatedItem_2'] = "news:root"
        i = i + 1
        
    file_name = "Prospector_General" + ".csv"
    savePath = r'C:/Users/sharo/Desktop/DOH_Collections_CSVs' + '/'
    dest = os.path.join(savePath,file_name)
    df.to_csv(dest, encoding='utf-8', index=False)
    print("Wrote " + file_name +".")        

def convert(general):
    path = r"C:\\Users\Sharo\Desktop\ProspectorXML"
    if general:
        convertGen(path)
    else:
        convertIss(path)
       
       
convert(False)      
    