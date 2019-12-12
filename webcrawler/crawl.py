#!/usr/bin/python

# Griffin Saiia, Gjs64
# Computer Security
# Underground Market Research
# github: https://github.com/gjbsaiia
import os
import sys

# My Libraries
import selenium
from datetime import datetime as dt
import webcrawler_api as web
import gsheet_api as g
import classDefinitions as c
from sinisterly_dic import market_url

def main():
    sesh = web.start()
    freshLog(sesh)
    try:
        creds = g.configCreds("creds.json")
        sesh.gsheet_creds = creds
        populateFlags(sesh)
        populateManifest(sesh)
        web.login(sesh.driver,'admin_config.txt')
        startCrawl(sesh, end=2)#237)
        writeTopTen(sesh)
        updateManifest(sesh)
        writeWebStats(sesh)
        writeToLog("**************************************************\n")
        writeToLog("Finished Updating GSheet")
        sesh.driver.quit()
    except Exception as e:
        updateManifest(sesh)
        writeWebStats(sesh)
        writeToLog("User Manifest:\n")
        writeToLog(str(sesh.user_manifest))
        writeToLog("***************************************\n")
        writeToLog("Thread Library:\n")
        writeToLog(str(sesh.threadLib))
        writeToLog("***************************************\n")
        writeToLog("Top Users:\n")
        writeToLog(str(sesh.topUsers))
        writeToLog("***************************************\n")
        writeToLog("ERROR:\n")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        writeToLog(exc_type, fname, exc_tb.tb_lineno)
        sesh.driver.quit()


def startCrawl(sesh, end=200):
    j = 0
    i = 6 # hardcoded because thread indexing starts here
    quarters = 4
    page_num = 1
    writeToLog('Starting to Crawl!')
    writeToLog("**************************************************\n")
    writeToLog("Page number: "+str(page_num))
    writeToLog(str(sesh.driver.current_url))
    writeToLog("**************************************************\n")
    current_page = market_url+"1"
    thread = web.stripThread(sesh.driver, current_page, i)
    try:
        while(page_num < end):
            if(thread):
                thread.setNumFlags(checkContent(sesh, thread))
                addThread(sesh, thread)
                sesh.threadCount += 1
                i += 1
                j += 1
            else:
                page_num += 1
                if(page_num * quarters > end):
                    prog = str(4-quarters)+"/4"
                    sesh.stopTime = dt.now()
                    sesh.crawlDuration = sesh.stopTime - sesh.startTime
                    if(4-quarters):
                        prog="1/4"
                    writeTopTen(sesh, prog)
                    writeWebStats(sesh, prog)
                    quarters -= 1
                writeToLog("**************************************************\n")
                writeToLog("Page number: "+str(page_num))
                web.nextPage(sesh.driver, str(page_num))
                current_page = sesh.driver.current_url
                writeToLog(current_page)
                writeToLog("**************************************************\n")
                i = 3
                j += 1
            writeToLog("Stripping Thread Number "+str(j)+"...")
            thread = web.stripThread(sesh.driver, current_page, i)
    except selenium.common.exceptions.NoSuchElementException:
        writeToLog("ERROR:\n")
        writeToLog(str(type(e)))
        writeToLog(str(e))
        end = j
    sesh.stopTime = dt.now()
    sesh.crawlDuration = sesh.stopTime - sesh.startTime
    writeToLog("**************************************************\n")
    writeToLog("Finished Crawling. Stripped "+str(end)+" values. Took "+str(sesh.crawlDuration)+".\n")

def populateFlags(sesh):
    list = g.readSheet(sesh.gsheet_creds, sesh.gsheet, sesh.flag_sheet, 2)
    for each in list:
        sesh.flags.append(each[0])
    return True

def populateManifest(sesh):
    list = g.readSheet(sesh.gsheet_creds, sesh.gsheet, sesh.user_sheet, 7)
    for each in list:
        entry = c.User(name=each[0], threads=int(each[2]), flagged=int(each[3]), replies=int(each[4]), views=int(each[5]), flags=int(each[6]))
        entry.calcValue()
        sesh.addUser(entry)
    return True

def checkNewUser(sesh, name):
    try:
        sesh.user_manifest[name]
        return False
    except KeyError:
        return True

def checkContent(sesh, thread):
    flags = 0
    for each in sesh.flags:
        if each in thread.content:
            sesh.updateFlagCount(each)
            flags += 1
        if each in thread.threadName:
            sesh.updateFlagCount(each)
            flags += 1
    if(flags):
        sesh.flaggedThreads += 1
    return flags

def addThread(sesh, thread):
    sesh.addThread(thread)
    if(checkNewUser(sesh, thread.user)):
        sesh.numVendors += 1
        if(thread.numFlags):
            sesh.numDirtyVendors += 1
        user = c.User(name= thread.user)
    else:
        user = sesh.user_manifest[thread.user][1]
    user.addThread_all(thread.setFlag(), thread.numReplies, thread.numFlags, thread.views)
    sesh.addUser(user)
    g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.market_sheet, [thread.dump()])
    return True

def updateManifest(sesh):
    manifest = sesh.dumpManifest()
    g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.user_sheet, manifest, overwrite=True)
    return True

def writeTopTen(sesh, prog):
    users = sesh.buildTopUsers()
    topten = []
    for user in users:
        entry = [user[0], user[1]]
        topthreads = sesh.getTopForUser(user[0])
        for each in topthreads:
            entry.append(each)
        entry.append("")
        topten.append(entry)
    topten.append(["","","","","","","", prog)])
    g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.top_sheet, topten, overwrite=True)

def writeWebStats(sesh, prog):
    stats = sesh.siteStats()
    stats.append(prog)
    g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.site_sheet, [stats], overwrite=True)

def writeToLog(string):
    if "*" not in string:
        timestamp = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        string = "["+timestamp+"]  "+string
    with open("log.txt", "a") as f:
        f.write(string)
        f.write("\n")
    f.close()
    print(string)

def freshLog(sesh):
    sesh.startTime = dt.now()
    with open("log.txt", "w+") as f:
        f.write("Webcrawler Log:\n")
        f.write("\n")
        f.write("Starting at "+sesh.startTime.strftime("%d/%m/%Y %H:%M:%S")+"...\n")
        f.write("\n")
        f.write("**************************************************\n")
        f.write("\n")
    f.close()


# to run it from command line
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
