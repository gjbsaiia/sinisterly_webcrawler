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

def main():
    sesh = web.start()
    creds = g.configCreds("creds.json")
    sesh.gsheet_creds = creds
    startCrawl(sesh)

def startCrawl(sesh):
    i = 6 # hardcoded because thread indexing starts here
    thread = stripThread(sesh.driver, i)
    while(thread):
        addThread(thread, sesh)
        i += 1
        thread = stripThread(sesh.driver, i)

def populateFlags(sesh):
    list = g.readSheet(sesh.gsheet_creds, sesh.gsheet, sesh.flag_sheet, 1)
    for each in list:
        sesh.flags.append(each[0])
    return True

def populateManifest(sesh):
    list = g.readSheet(sesh.gsheet_creds, sesh.gsheet, sesh.user_sheet, 5)
    for each in list:
        entry = c.User(name=each[0], threads=each[1], replies=each[2], score=each[3], rating=each[4])
        sesh.addToManifest(entry)
    return True

def checkNewUser(sesh, name):
    try:
        sesh.user_manifest[name]
        return False
    except KeyError:
        return True

def checkContent(sesh, content):
    if any(flag in content for flag in sesh.flags):
        return True
    return False

def addThread(sesh, thread):
    g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.market_sheet, thread.dump())
    if(checkNewUser(thread.user)):
        newUser = c.User(name=thread.user, threads=1, score=thread.threadRating, rating=thread.threadRating)
        sesh.addToManifest(newUser)
    else:
        sesh.user_manifest[thread.user].addThread()
        sesh.user_manifest[thread.user].updateAveRating(thread.threadRating)
    for each in thread.replies:
        if(checkNewUser(each)):
            newUser = c.User(name=each, threads=0, replies=1)
            sesh.addToManifest(newUser)
        else:
            sesh.user_manifest[thread.user].addReply()
    return True

def updateManifest(sesh):
    manifest = sesh.dumpManifest()
    for each in manifest:
        g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.user_sheet, each, overwrite=True)
    return True

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
