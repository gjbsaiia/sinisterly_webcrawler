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
	credss = creds
	sheeet = sheet
	subsheeet = subsheet
	columnss = columns
	try:
		goog = gspread.authorize(creds)
		sheet = goog.open(sheet).worksheet(subsheet)
		i = 2
		j = 1
		flag = (sheet.cell(i,j).value != "")
		while(flag):
			try:
				while(j <= columns):
					entry.append((sheet.cell(i,j).value).encode("utf-8"))
					j += 1
				j = 1
				list.append(entry)
				entry = []
				i += 1
				flag = (sheet.cell(i,j).value != "")
			except gspread.exceptions.APIError:
				print("API Limit\n")
				time.sleep(110)
				flag = (sheet.cell(i,j).value != "")
	except gspread.exceptions.APIError:
		print("API Limit\n")
		time.sleep(110)
		readSheet(credss, sheeet, subsheeet, columnss)
	return list

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
		goog = gspread.authorize(creds)
		sheet = goog.open(sheet).worksheet(subsheet)
		j = 1
		if(overwrite):
			i = 2
		else:
			i = findLast(sheet)
		for each in data:
			for datum in each:
				try:
					sheet.update_cell(i, j, datum)
				except gspread.exceptions.APIError:
					print("API Limit\n")
					time.sleep(110)
					sheet.update_cell(i, j, datum)
				j+=1
			j = 1
			i += 1
	except gspread.exceptions.APIError:
		print("API Limit\n")
		time.sleep(110)
		writeData(credss, sheeet, subsheeet, dataa, overwritee)
	return True
