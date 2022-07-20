import os
import sys
import subprocess
import time
import pandas as pd


def htmlParser(questionNumber, questionStage, questionContent, questionAssetURL):
	if int(questionNumber) >= 10:
		f = open('/Users/rubis/Desktop/Sample Problem/subquestions/math/'+'0'+ questionNumber +'_' + questionStage+'.html', 'w')
	else:
		f = open('/Users/rubis/Desktop/Sample Problem/subquestions/math/'+'00'+ questionNumber +'_' + questionStage+'.html', 'w') 	
	f.write("<!DOCTYPE html>\n")
	f.write("<html>\n")
	f.write("<head>")
	f.write(" <meta charset=\"utf-8\"> \n")
	f.write("<link href='https://fonts.googleapis.com/css?family=Noto Sans' rel='stylesheet'>\n")
	f.write("<style>\n")
	f.write("body {\n")
	f.write("\t font-family: \'Noto Sans\'; font-size: 14px;\n")
	f.write("}\n")
	f.write("</style>\n")
	f.write("</head>\n")
	f.write("<body>\n")
	f.write("<div style= \"text-align: center;\">\n")
	f.write("<p>")
	f.write(questionContent)
	f.write("</p>\n")
	if questionAssetURL == "nan":
		f.write("</div>\n")
	else:
		f.write("<img src=")
		f.write("\"")
		f.write(questionAssetURL)
		f.write("\"")
		f.write(" />\n")
		f.write("</div>\n")

	f.write("</body>\n")
	f.write("</html>\n")
	f.close()

def getAttribute():
	df = pd.read_excel("mathSubquestion.xlsx", engine = "openpyxl")

	new_header = df.iloc[1]
	df = df[0:]
	df.columns = new_header

	for i in range(2,len(df)): 
		questionNumber = str(df.loc[i,'Number'])
		questionStage = str(df.iloc[i]['Stage'])
		questionContent = str(df.iloc[i]['Content'])
		questionAssetURL = str(df.iloc[i]['assetURL'])

		htmlParser(questionNumber, questionStage, questionContent, questionAssetURL)


if __name__ == "__main__":
	getAttribute()		










