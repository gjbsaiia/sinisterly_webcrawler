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

# My Libraries
from classDefinitions import Session
from sinisterly_dic import market_url
from sinisterly_dic import xpathDic

def start():
	sesh = Session()
	options = Options()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_argument("disable-infobars")
	options.add_argument("--disable-extensions")
	sesh.driver = webdriver.Chrome(chrome_options=options)
	sesh.driver.set_window_size(1120, 750)
	sesh.driver.get(market_url)
	return sesh

def stripThread(driver, i):
	data = []
	key = ""
	path = ""
	th = str(i)
	try:
		key = "th_title"
		path = xpathDic["th_title1"]+th+xpathDic["th_title2"]
		data.append(getTextFrom(driver, path))
		key = "th_user"
		path = xpathDic["th_user1"]+th+xpathDic["th_user2"]
		data.append(getTextFrom(driver, path))
		key = "th_time"
		path = xpathDic["th_time1"]+th+xpathDic["th_time2"]
		data.append(getTimeStamp(driver, path))
		key = "th_replies"
		path = xpathDic["th_replies1"]+th+xpathDic["th_replies2"]
		data.append(getTextFrom(driver, path))
		key = "th_views"
		path = xpathDic["th_views1"]+th+xpathDic["th_views2"]
		key = "th_title"
		data.append(getViewElement(driver, path))
		path = xpathDic["th_title1"]+th+xpathDic["th_title2"]
		getElementFrom(driver, path).click()
		key = "url"
		data.append((driver.current_url).encode("utf-8"))
		key = "th_content"
		data.append(getTextFrom(driver, xpathDic["th_content"]))
	except selenium.common.exceptions.NoSuchElementException:
		print("Failed on "+key+" with "+path+", on thread num "+th+"\n")
	driver.get(market_url)
	return data

def getTimeStamp(driver, xpath):
	elem = getElementFrom(driver, xpath)
	return (elem.get_attribute("title")).encode('utf-8')

def getViewElement(driver, xpath):
	text = getTextFrom(driver, xpath)
	return cleanNum(text.split("\n")[0])

def cleanNum(num):
	return int("".join(num.split(",")))

def getElementFrom(driver, xpath):
	return driver.find_element_by_xpath(xpath)

def getTextFrom(driver, xpath):
	element = driver.find_element_by_xpath(xpath)
	return (element.text).encode("utf-8")
