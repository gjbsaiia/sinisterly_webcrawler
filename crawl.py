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
    # thread = web.stripThread(sesh.driver, i)
    # thread.setFlag(checkContent(sesh, thread.content))
    # print(thread.dump())
    populateFlags(sesh)
    populateManifest(sesh)
    startCrawl(sesh)
    updateManifest(sesh)

def startCrawl(sesh, end=1000):
    i = 6 # hardcoded because thread indexing starts here
    thread = web.stripThread(sesh.driver, i)
    while(thread and i < end):
        thread.setFlag(checkContent(sesh, thread))
        addThread(sesh, thread)
        i += 1
        thread = web.stripThread(sesh.driver, i)

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

def checkContent(sesh, thread):
    if any(flag in thread.content for flag in sesh.flags):
        return True
    if any(flag in thread.threadName for flag in sesh.flags):
        return True
    return False

def addThread(sesh, thread):
    g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.market_sheet, [thread.dump()])
    if(checkNewUser(sesh, thread.user)):
        if(thread.threadRating):
            newUser = c.User(name=thread.user, threads=1, scored=1, score=int(thread.threadRating), rating=int(thread.threadRating))
        else:
            newUser = c.User(name=thread.user, threads=1, scored=0)
        sesh.addToManifest(newUser)
    else:
        if(thread.threadRating):
            sesh.user_manifest[thread.user].addScored()
            sesh.user_manifest[thread.user].updateAveRating(int(thread.threadRating))
        else:
            sesh.user_manifest[thread.user].addThread()
    for each in thread.replies:
        if(checkNewUser(each)):
            newUser = c.User(name=each, threads=0, replies=1)
            sesh.addToManifest(newUser)
        else:
            sesh.user_manifest[thread.user].addReply()
    return True

def updateManifest(sesh):
    manifest = sesh.dumpManifest()
    g.writeData(sesh.gsheet_creds, sesh.gsheet, sesh.user_sheet, manifest, overwrite=True)
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
