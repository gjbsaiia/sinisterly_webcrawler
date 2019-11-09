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
	# options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_argument("disable-infobars")
	options.add_argument("--disable-extensions")
	sesh.driver = webdriver.Chrome(chrome_options=options)
	sesh.driver.set_window_size(1120, 750)
	sesh.driver.get(market_url)
	return sesh
