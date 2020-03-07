#Checks that XML is well formed (does not validate)

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import glob, sys
from glob import iglob
import os

probPIDs = []
def parsefile(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)

def getPID(filename):
    name = os.path.basename(filename)
    return name

for filename in glob.iglob(r'C:\Users\sharo\Deskto\arms_cheerio\**.xml', recursive=True):
    try:
        parsefile(filename)
        
        #print(filename + " is well-formed.")
    except:
        #e = str(sys.exc_info()[0])
        filename = getPID(filename)
        probPIDs.append(filename)
if len(probPIDs) > 0:     
    print("Please review: the following files were not well formed.")
    print("-------------------------------------------------------")
    for pid in probPIDs:
        print(pid)
