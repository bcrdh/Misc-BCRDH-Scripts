#Convert DI (DC) metadata to MODS
import pandas as pd
import re
import glob
import openpyxl
from datetime import datetime

modsCols =  ['Filename','Title', 'AlternativeTitle', 'Creator1_Given','Creator1_Family', 'Creator2_Given','Creator2_Family', 'Creator3_Given','Creator3_Family']
modsCols += ['CorporateCreator','Contributor1_Given','Contributor1_Family','CorporateContributor','Publisher_Original','DateCreated','Description','Extent','Subject1_Topic','Subject2_Topic','Subject3_Topic','Subject4_Topic','Subject5_Topic']
modsCols += ['Subject_Geographic','Coordinates','Subject1_Given','Subject1_Family','Subject2_Given','Subject2_Family','Subject3_Given','Subject3_Family','CorporateSubject_1','CorporateSubject_2']
modsCols += ['Genre','Type','internetMediaType','Language','Notes','AccessIdentifier','LocalIdentifier','Classification','URI']
modsCols += ['Source','Rights','CreativeCommons_URI','RightsStatement','relatedItem_1','relatedItem_2']

def multiHdgMkr(pt1, num, pt2):
            return(pt1 + str(num) + '_' + pt2)

def toMODS(filename):
    #read DC spreadsheets in and replace spaces in hdgs w/ underscore
    df = pd.read_csv(filename, dtype=str)
    print("pre-conv column names: " + str(df.columns.values.tolist()))
    df.columns = df.columns.str.replace(' ', '')
    df.columns = df.columns.str.replace('-','_')
    print(df.columns.values.tolist())
    modsDF = pd.DataFrame(columns = modsCols)
    modsDF.append(pd.Series(), ignore_index=True)
   
    df = df.where((pd.notnull(df)), None) #convert Pandas NaNs to None
    i = 0 #row count
    for item in df.itertuples():
        fn = item.Filename
        if fn != None:
            modsDF.at[i,'Filename'] = fn.strip()
        else:
            ti = item.Title
            if ti == None:
                ti = "No Title"
            print("Stopped at " + ti)
            break
        modsDF.at[i, 'Title'] = item.Title.strip()
        #alt title
        altTi = item.AlternativeTitle
        if altTi != None:
            modsDF.at[i, 'AlternativeTitle'] = altTi.strip()
        pub = item.Publisher_Original
        if pub != None:
            modsDF.at[i, 'Publisher_Original'] = pub.strip()
            
        #Description    
        descr = item.Description
        if descr != None:
            descr = descr.strip()
        else:
            descr = ''
        if 'Transcript' in df.columns:
            transcr = item.Transcript
        else:
            transcr = None
        if transcr != None:
            if len(descr) > 0:
                descr += " " + transcr.strip()
            else:
                descr = transcr.strip()
        notes = item.Notes
        if notes != None:
            if len(descr) > 0:
                descr += " " + notes.strip()
            else:
                descr = notes.strip()
        modsDF.at[i, 'Description'] = descr
        subGeo = item.Subject_Geographic
        if subGeo != None:
            modsDF.at[i,'Subject_Geographic'] = subGeo.strip()
        modsDF.at[i,'Extent'] = item.Extent.strip()
        modsDF.at[i, 'Genre'] = item.Genre.strip().lower()
        modsDF.at[i,'Type'] = item.Type.strip().lower()
        iMF = item.Format
        if iMF == None:
            iMF = ""
        else:
            iMF = iMF.strip()
        iMF = item.Format.strip()
        if iMF == 'image/jpeg':
            iMF = 'image/jp2'
        modsDF.at[i,'internetMediaType'] = iMF
        if item.Language == None:
            lang = ""
        else:
            lang = item.Language.strip()
        
        modsDF.at[i,'Language'] = lang
        ai = item.DigitalIdentifier
        if ai != None:
            modsDF.at[i, 'AccessIdentifier'] = ai.strip()
        li = item.AccessIdentifier
        if li != None:
            modsDF.at[i,'LocalIdentifier'] = li.strip()
        modsDF.at[i,'relatedItem_1'] = item.IsPartOf.strip()
        modsDF.at[i,'Rights'] = item.Rights.strip()
        modsDF.at[i,'RightsStatement'] = 'Copyright Not Evaluated: http://rightsstatements.org/vocab/CNE/1.0/'
        uri = item.CatalogueRecord
        if uri != None:
            modsDF.at[i,'URI'] = uri.strip()     
        su = item.Subject
        if su != None:
            su = su.strip()
            if su.find(";") == -1:
                subs = [su]
            else:
                subs = su.split(";")
            count = 1
            for sub in subs:
                fieldname = multiHdgMkr('Subject', count, 'Topic')
                modsDF.at[i, fieldname] = sub.strip()
                count += 1
        sortDt = item.SortDate
        if sortDt == None:
            sortDt = "n.d."
        modsDF.at[i, "DateCreated"] = sortDt.strip()
        dateRange = False
        dCr = item.DateCreated
        if dCr == None:
            dCr = "n.d."
        if dCr.find("[") > -1 or dCr.find("?") > -1 or dCr.find("or") > -1 or dCr.find("Between") > -1:
            dateRange = True
        ti = item.Title.strip()
        if not dateRange:
            modsDF.at[i, "Title"] = ti
        else:
            yrInTi = re.search(r'[12][890]\d\d', ti)
            if not yrInTi:
                ti = ti + ", ca. " + sortDt.strip()
                modsDF.at[i,'Title'] = ti
            else:
                modsDF.at[i, "Title"] = ti
       
        #Personal Names (personal subjects)
        persNm = item.PersonalNames
        if persNm != None:
            print('Personal Names: ' + persNm)
            if persNm.find(";") == -1:
                persNames = [persNm]
            else:
                persNames = persNm.split(";")
            count = 1
            for nm in persNames:
                fieldname = multiHdgMkr('Subject', count, 'Family')
                if nm.find(",") == -1:
                    modsDF.at[i,'fieldname'] = nm.strip()
                else:
                    nms = nm.split(",")
                    family = multiHdgMkr('Subject', count, 'Family')
                    modsDF.at[i, family] = nms[0].strip()
                    given = multiHdgMkr('Subject', count, 'Given')
                    modsDF.at[i, given] = nms[1].strip()
                count += 1  
        
        #Corporate Creator   
        corpCr = item.CorporateCreator
        if corpCr != None:
            modsDF.at[i, 'CorporateCreator'] = corpCr.strip()
        
             
        #Personal Creators    
        count = 1    
        cr = item.Creator
        creators = []
        if cr != None:
            print("Creator(s): " + cr)
            if cr.find(";") == -1:
                creators = [cr]
            else:
                creators = cr.split(";")
            count = 1
            for c in creators:
                fieldname = multiHdgMkr('Creator', count, 'Family')
                print("Creator: " + c)
                if c.find(",") == -1:
                    modsDF.at[i,fieldname] = nm.strip()
                else:
                    c = c.split(",")
                    family = multiHdgMkr('Creator', count, 'Family')
                    modsDF.at[i, family] = c[0].strip()
                    given = multiHdgMkr('Creator', count, 'Given')
                    modsDF.at[i, given] = c[1].strip()      
                count += 1
        i = i + 1    
    #file_name = repCol + ".csv"
    #output_fname = filename.replace("RevA","RevB")
    output_fname = filename.replace("simpson_basic_md_OSC_ARC_","UBC_01_")
    output_fname = output_fname.replace(".csv", "_RevB.csv")
    modsDF.to_csv(output_fname, encoding='utf-8', index=False)
    print("Wrote " + output_fname +".")
               
for filename in glob.iglob(r'C:\\Users\sharo\Desktop\UBCO_01\**.csv', recursive=True):
#    csvpath = r'simpson_basic_md_OSC_ARC_02_001_010e.csv'
    toMODS(filename)