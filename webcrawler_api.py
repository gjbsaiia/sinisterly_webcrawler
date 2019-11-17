#!/usr/bin/python

# Griffin Saiia, Gjs64
# Computer Security
# Underground Market Research
# github: https://github.com/gjbsaiia


import os
import sys
import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager

# My Libraries
from classDefinitions import Session
from classDefinitions import Thread
from sinisterly_dic import login_url
from sinisterly_dic import market_url
from sinisterly_dic import xpathDic

def start():
	sesh = Session()
	options = Options()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_argument("disable-infobars")
	options.add_argument("--disable-extensions")

	sesh.driver = webdriver.Chrome(chrome_options=options, executable_path='chromedriver')

	#sesh.driver = webdriver.Chrome(ChromeDriverManager().install())
	sesh.driver.set_window_size(1120, 750)
	sesh.driver.get(market_url)
	return sesh

def login(driver, path):
	driver.get(login_url)
	login_info =[]
	with open(path) as file:
		login_info = file.readlines()
	user = login_info[0].split(",")[0]
	password = login_info[0].split(",")[1].split("\n")[0]
	elem = driver.find_element_by_xpath(xpathDic["login"])
	elem.click()
	elem = driver.find_element_by_xpath(xpathDic["user"])
	elem.send_keys(user)
	elem = driver.find_element_by_xpath(xpathDic["password"])
	elem.send_keys(password)
	elem = driver.find_element_by_xpath(xpathDic["submit"])
	elem.click()
	driver.get(market_url)

def stripThread(driver, i):
	th = str(i)
	path = xpathDic["th_title1"]+th+xpathDic["th_title2"]
	if(checkExists(driver, path)):
		key = ""
		thread = Thread()
		try:
			key = "th_title"
			path = xpathDic["th_title1"]+th+xpathDic["th_title2"]
			thread.setName(getTextFrom(driver, path))
			key = "th_user"
			path = xpathDic["th_user1"]+th+xpathDic["th_user2"]
			thread.setUser(getTextFrom(driver, path))

			key = "th_replies"
			path = xpathDic["th_replies1"]+th+xpathDic["th_replies2"]
			thread.setNumReplies(getTextFrom(driver, path))
			key = "th_views"
			path = xpathDic["th_views1"]+th+xpathDic["th_views2"]
			thread.setNumViews(getViewElement(driver, path))
			key = "th_rating"
			path = xpathDic["th_rating1"]+th+xpathDic["th_rating2"]
			thread.setRating(getRating(driver, path))
			# inside thread
			path = xpathDic["th_title1"]+th+xpathDic["th_title2"]
			getElementFrom(driver, path).click()
			key = "url"
			print(driver.current_url)
			thread.setURL((driver.current_url))
			key = "th_content"
			thread.setContent(getContent(driver, xpathDic["th_content"]))
			key = "th_time"
			path = xpathDic["th_time1"]+th+xpathDic["th_time2"]
			thread.setTime(getTimeStamp(driver, path))
		except selenium.common.exceptions.NoSuchElementException:
			print("Failed on "+key+" with "+path+", on thread num "+th+"\n")
		driver.get(market_url)
		return thread
	else:
		return None

def checkExists(driver, path):
	try:
		getElementFrom(driver, path)
		return True
	except selenium.common.exceptions.NoSuchElementException:
		return False

def getContent(driver, path):
	text = getTextFrom(driver, path)
	#text = text.decode('utf-8')
	return "/n ".join(text.split("\n"))

def get_text_excluding_children(driver, element):
	return driver.execute_script("""
	var parent = arguments[0];
	var child = parent.firstChild;
	var ret = "";
	while(child) {
	    if (child.nodeType === Node.TEXT_NODE)
	        ret += child.textContent;
	    child = child.nextSibling;
	}
	return ret;
	""", element)

def getRating(driver, path):
	elem = getElementFrom(driver, path)
	text = get_text_excluding_children(driver, elem)
	split = text.split(" - ")
	try:
		if(int(split[0].split(" ")[0]) > 0):
			return split[1].split(" ")[0]
	except ValueError:
		print("Path: "+path+", value: "+split[0].split(" ")[0]+"\n")
	return ""

def getTimeStamp(driver, xpath):
	elem = getElementFrom(driver, xpath)
	return (elem.get_attribute("title"))#.encode('utf-8')

def getViewElement(driver, xpath):
	text = getTextFrom(driver, xpath)

	# text = text.decode('utf-8')
	temp1 = text.split("\n")[0]
	return cleanNum(temp1)

def cleanNum(num):

	return int("".join(num.split(",")))

def getElementFrom(driver, xpath):
	return driver.find_element_by_xpath(xpath)

def getTextFrom(driver, xpath):
	element = driver.find_element_by_xpath(xpath)
	return (element.text)
