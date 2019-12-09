#!/usr/bin/python

# Griffin Saiia, Gjs64
# Computer Security
# Underground Market Research
# github: https://github.com/gjbsaiia
import os
import sys

# My Libraries
import webcrawler_api as web
import gsheet_api as g
import classDefinitions as c
from sinisterly_dic import market_url

def main():
    freshLog()
    sesh = web.start()
    try:
        creds = g.configCreds("creds.json")
        sesh.gsheet_creds = creds
        populateFlags(sesh)
        populateManifest(sesh)
        web.login(sesh.driver,'admin_config.txt')
        startCrawl(sesh)
        writeTopTen(sesh)
        updateManifest(sesh)
        writeToLog("**************************************************\n")
        writeToLog("Finished Updating GSheet")
        sesh.driver.quit()
    except Exception as e:
        writeToLog("User Manifest:\n")
        writeToLog(sesh.user_manifest)
        writeToLog("***************************************\n")
        writeToLog("Thread Library:\n")
        writeToLog(sesh.threadLib)
        writeToLog("***************************************\n")
        writeToLog("Top Users:\n")
        writeToLog(sesh.topUsers)
        writeToLog("***************************************\n")
        writeToLog("ERROR:\n")
        writeToLog(type(e))
        writeToLog(e)
        sesh.driver.quit()


def startCrawl(sesh, end=1000):
    j = 0
    i = 6 # hardcoded because thread indexing starts here
    page_num = 1
    writeToLog('Starting to Crawl!')
    writeToLog("**************************************************\n")
    writeToLog("Page number: "+str(page_num))
    writeToLog("**************************************************\n")
    current_page = market_url
    thread = web.stripThread(sesh.driver, current_page, i)
    next_flag = False
    while(j < end):
        if(thread):
            thread.setNumFlags(checkContent(sesh, thread))
            addThread(sesh, thread)
            i += 1
            j += 1
        else:
            page_num += 1
            writeToLog("**************************************************\n")
            writeToLog("Page number: "+str(page_num))
            writeToLog("**************************************************\n")
            web.nextPage(sesh.driver,next_flag)
            next_flag=True
            current_page = sesh.driver.current_url
            i = 3
            j += 1
        writeToLog("Stripping Thread Number "+str(j)+"...")
        thread = web.stripThread(sesh.driver, current_page, i)
    writeToLog("**************************************************\n")
    writeToLog("Finished Crawling. Stripped "+str(end)+" values.")

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
            flags += 1
        if each in thread.threadName:
            flags += 1
    return flags

def addThread(sesh, thread):
    sesh.addThread(thread)
    if(checkNewUser(sesh, thread.user)):
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

def writeTopTen(sesh):
    users = sesh.buildTopUsers()
    topten = []
    for user in users:
        entry = [user[0], user[1]]
        topthreads = sesh.getTopForUser(user[0])
        for each in topthreads:
            entry.append(each)
        topten.append(entry)
    g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.top_sheet, topten, overwrite=True)

def writeToLog(string):
    with open("log.txt", "a") as f:
        f.write(string)
        f.write("\n")
    f.close()
    print(string)

def freshLog():
    with open("log.txt", "w+") as f:
        f.write("Webcrawler Log:\n")
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
