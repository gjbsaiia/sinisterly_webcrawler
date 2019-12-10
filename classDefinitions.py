#!/usr/bin/python

# Griffin Saiia, Gjs64
# Computer Security
# Underground Market Research
# github: https://github.com/gjbsaiia

class Session:
	def __init__(self):
		self.driver = None
		self.user_manifest = {}
		self.gsheet_creds = ""
		self.gsheet = "Sinister.ly Market Data"
		self.user_sheet = "User Manifest"
		self.top_sheet = "Top Ten"
		self.market_sheet= "Market"
		self.flag_sheet = "Flag Words"
		self.site_sheet = "Website Stats"
		self.threadCount = 0
		self.flaggedThreads = 0
		self.flagCount = {}
		self.numUsers = 0
		self.flags = []
		self.topUsers = []
		self.threadLib = {}
	def addUser(self, user):
		self.user_manifest.update({user.name: [user.calcValue(), user]})
	def addThread(self, thread):
		threads = self.threadLib.get(thread.user, False)
		if(threads):
			threads.append(thread)
		else:
			threads = []
			threads.append(thread)
		self.threadLib.update({thread.user: threads})
	def dumpManifest(self):
		list = []
		for key,value in self.user_manifest.items():
			list.append(value[1].dump())
		return list
	def buildTopUsers(self):
		values = list(self.user_manifest.values())
		values.sort(key = lambda values: values[0], reverse=True)
		i = 0
		while( i < 10 ):
			if(i >= len(values)):
				self.topUsers.append(["",""])
			else:
				self.topUsers.append([values[i][1].name, values[i][1].calcValue()])
			i += 1
		return self.topUsers
	def getTopForUser(self, user):
		threads = self.threadLib.get(user, False)
		if(threads):
			flagged_threads = list(filter(lambda threads: (threads.flag), threads))
			flagged_threads.sort(key = lambda flagged_threads: (flagged_threads.views + flagged_threads.numReplies), reverse=True)
			i = 0
			topfive = []
			while(i < 5):
				try:
					topfive.append(flagged_threads[i].threadUrl)
				except IndexError:
					topfive.append('')
				i += 1
		else:
			topfive = ['','','','','']
		return topfive
	def updateFlagCount(self, flag):
		count = self.flagCount.get(flag, False)
		if(count):
			count += 1
		else:
			count = 1
		self.flagCount.update({flag: count})
	def siteStats(self):
		percentFlagged = (float(self.flaggedThreads) / float(self.threadCount))
		sorted_flags = sorted(self.flagCount.items(), key=lambda kv: kv[1], reverse=True)
		return [percentFlagged, sorted_flags[0][0], self.numUsers]


class User: # object the encloses all your data
	def __init__(self, name, threads=0, flagged=0, replies=0, views=0, flags=0):
		self.name = name # API Key to optional Google Sheet functionality
		self.base_url = "https://sinister.ly/User-"
		self.profile_url = self.base_url+name
		self.threadCount = threads
		self.flaggedThread = flagged
		self.replyCount = replies
		self.views = views
		self.flagsTripped = flags
		self.buzzDesity = 0.0
		self.percentFlagged = 0.0
		self.comm_inter = 0.0
		self.user_value = 0.0
	def addThread_all(self, flth, replies, flags, views):
		self.addThread()
		if(flth):
			self.addFlagged()
		self.addReplies(replies)
		self.addFlags(flags)
		self.addViews(views)
	def addThread(self):
		self.threadCount += 1
	def addFlagged(self):
		self.flaggedThread += 1
	def addReplies(self, num):
		self.replyCount += num
	def addFlags(self, num):
		self.flagsTripped += num
	def addViews(self, num):
		self.views += num
	def calcBuzz(self):
		if(self.threadCount):
			self.buzzDesity = float(self.flagsTripped)/float(self.threadCount)
		else:
			self.buzzDesity = 0.0
		return self.buzzDesity
	def calcPercentFlagged(self):
		if(self.threadCount):
			self.percentFlagged = float(self.flaggedThread) / float(self.threadCount)
		else:
			self.buzzDesity = 0.0
		return self.percentFlagged
	def calcCommInter(self):
		if(self.views):
			self.comm_inter = float(self.views)*( float(self.replyCount) / float(self.views) )
		else:
			self.comm_inter = 0.0
		return self.comm_inter
	def calcValue(self):
		self.user_value = (self.calcBuzz() * self.calcPercentFlagged())*(self.threadCount) + (self.calcCommInter())
		return self.user_value
	def dump(self):
		self.calcValue()
		return [self.name,
				self.user_value,
				self.threadCount,
				self.flaggedThread,
				self.replyCount,
				self.views,
				self.flagsTripped,
				self.buzzDesity,
				self.percentFlagged,
				self.comm_inter,
				self.profile_url,]

class Thread: # object to enclose all data concerning one thread
	def __init__(self, me="", name="", url="", rating="", replies=[], numRep = 0, views = 0, content = "", date = "", numFlags=0, flag=False):
		self.user = me # profile this post belongs to
		self.threadName = name # name of thread
		self.numReplies = numRep # number of replies
		self.views = views # number of thread views
		self.content = content # content of original post
		self.date = date # date post was posted
		self.numFlags = numFlags
		self.flag = flag
		self.threadUrl = url
	def setUser(self, user):
		self.user = user
	def setName(self, name):
		self.threadName = name
	def setURL(self, url):
		self.threadUrl = url
	def setNumReplies(self, num):
		try:
			self.numReplies = int(num)
		except ValueError:
			print("ERROR: Reply number not recovered, "+str(num))
			self.numReplies=0
	def setNumViews(self, num):
		try:
			self.views = int(num)
		except ValueError:
			print("ERROR: Views number not recovered, "+str(num))
			self.views = 0
	def setTime(self, string):
		self.date = string
	def setContent(self, string):
		self.content = string.lower()
	def setNumFlags(self, num):
		self.numFlags = num
		self.setFlag()
	def setFlag(self):
		if(self.numFlags):
			self.flag = True
		else:
			self.flag = False
		return self.flag
	def dump(self):
		return [self.threadName,
				self.user,
				self.date,
				self.numReplies,
				self.views,
				self.numFlags,
				self.threadUrl,
				self.content,
				self.setFlag()]
