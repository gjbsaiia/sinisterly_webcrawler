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
from oauth2client.client import SignedJwtAssertionCredentials

# config credentials
def configCreds(credPath):
	json_key = json.load(open(credPath))
	scopeList = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scopeList)
	return credentials

# reads sheet, returns list of lists
def readSheet(creds, sheet, subsheet, columns):
	list = []
	entry = []
	goog = gspread.authorize(creds)
	sheet = goog.open(sheet).worksheet(subsheet)
	i = 2
	j = 1
	while(sheet.cell(i,j).value != ""):
		while(j <= columns):
			entry.append(sheet.cell(i,j).value)
			j += 1
		j = 1
		list.append(entry)
		entry = []
		i += 1
	return list

# finds last occupied cell
def findLast(sheet):
	i = 1
	while(sheet.cell(i,1).value != ""):
		i += 1
	return i

def writeData(creds, sheet, subsheet, data, overwrite=False):
	goog = gspread.authorize(creds)
	sheet = goog.open(sheet).worksheet(subsheet)
	j = 1
	if(overwrite):
		i = 2
	else:
		i = findLast(sheet)
	for each in data:
		for datum in each:
			sheet.update_cell(i, j, datum)
			j+=1
		j = 0
		i += 1
	return True
