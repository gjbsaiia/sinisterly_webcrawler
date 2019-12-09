#!/usr/bin/python

# Griffin Saiia, Gjs64
# Computer Security
# Underground Market Research
# github: https://github.com/gjbsaiia

import os
import sys
import json
import gspread
import time
#from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.client import AssertionCredentials
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
import googleapiclient as gapi



SHEET_ID = "190fbfWoewEeNyZaJqAoi0erhY3W_DXTGG1UAQZPcHmM"

column_dict = {1:"A",
			   2:"B",
			   3:"C",
			   4:"D",
			   5:"E",
			   6:"F",
			   7:"G",
			   8:"H",
			   9:"I",
			   10:"J",
			   11:"K",
			   12:"L",
			   }


# config credentials
def configCreds(credPath):
	#json_key = json.load(open(credPath))
	scopeList = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_name(credPath, scopeList)
	return credentials

# reads sheet, returns list of lists
def readSheet(creds, sheet, subsheet, columns):
	list = []
	entry = []
	credss = creds
	sheeet = sheet
	subsheeet = subsheet
	columnss = columns
	try:
		# goog = gspread.authorize(creds)
		# sheet = goog.open(sheet).worksheet(subsheet)

		serv = discovery.build('sheets','v4',credentials=creds)

		request = serv.spreadsheets().values().batchGet(spreadsheetId=SHEET_ID,ranges=[str(subsheeet)+'!A2:'+column_dict[columnss]])
		response=request.execute()

	except gspread.exceptions.APIError:
		print("API Limit\n")
		time.sleep(110)
		return readSheet(credss, sheeet, subsheeet, columnss)
	if(response['valueRanges'][0].get('values', False)):
		return response['valueRanges'][0]['values']
	return []

# finds last occupied cell
def findLast(sheet):
	i = 1
	while(sheet.cell(i,1).value != ""):
		i += 1
	return i

def writeData(creds, sheet, subsheet, data, overwrite=False):
	credss = creds
	sheeet = sheet
	subsheeet = subsheet
	dataa = data
	overwritee = overwrite


	try:

		serv = discovery.build('sheets', 'v4', credentials=creds)

		body = {'range':str(subsheeet)+'!A2:I',
				'values':data,
				'majorDimension':'ROWS'}
		# print(data[0][1:])
		# print(json.dumps(body))
		request = serv.spreadsheets().values().append(spreadsheetId=SHEET_ID,
													  range=str(subsheeet)+'!A2:I',valueInputOption='RAW',
													  insertDataOption='INSERT_ROWS',
													  body=body)

		try:
			response = request.execute()
			#print(response)
			return True
		except gapi.errors.HttpError as err:
			print(err)
			return False


	except gspread.exceptions.APIError:
		print("API Limit\n")
		time.sleep(110)
		writeData(credss, sheeet, subsheeet, dataa, overwritee)
	return True

# def main():
# 	creds = configCreds("creds.json")
# 	print('writing')
# 	rite = [["Johnny Test",69,420,350,5],["EuroStep",68,421,439,4]]
# 	print(writeData(creds, "Sinister.ly Market Data","User Manifest",rite))
# 	#print(readSheet(creds, "Sinister.ly Market Data","Market",9))
# 	print('done')
#
# if __name__ == "__main__":
# 	main()
