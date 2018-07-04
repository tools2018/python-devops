#!/usr/bin/python
import difflib
import sys

try:
    textfile1 = sys.argv[1]
    textfile2 = sys.argv[2]
except Exception as e:
    print("Error:"+str(e))
    print("Usage: simple3.py filename1 filename2")
    sys.exit()

def readfile(filename):
    try:
        fileHandle = open(filename)
        text = fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as error:
       print('Read file Error:'+str(error))
       sys.exit()

if textfile1 == "" or textfile2 == "":
    print("Usage: simple3.py filename1 filename2")
    sys.exit()

diff = open("diff.html", 'w')
text1_lines = readfile(textfile1) 
text2_lines = readfile(textfile2) 

d = difflib.HtmlDiff()
diff.write(d.make_file(text1_lines, text2_lines))
diff.close()
