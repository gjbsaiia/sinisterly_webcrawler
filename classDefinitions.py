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
		self.flags = []
		self.topUsers = []
	def addToManifest(self, user):
		self.user_manifest.update({user.name: user})
	def dumpManifest(self):
		list = []
		for key,value in self.user_manifest.items():
			list.append(value.dump())
		return list

class User: # object the encloses all your data
	def __init__(self, name, threads=0, scored=0, replies=0, score=0, rating=0, flags=0):
		self.name = name # API Key to optional Google Sheet functionality
		self.base_url = "https://sinister.ly/User-"
		self.profile_url = self.base_url+name
		self.threadCount = threads
		self.scoredThread = scored
		self.replyCount = replies
		self.totalScore = score
		self.aveRating = rating
		self.flagsTripped = flags
	def addThread(self):
		self.threadCount += 1
	def addScored(self):
		self.threadCount += 1
		self.scoredThread += 1
	def addReply(self):
		self.replyCount += 1
	def updateAveRating(self, rating):
		self.totalScore += float(rating)
		self.aveRating = float(self.totalScore) / float(self.scoredThread)
	def addFlags(self, num):
		self.flagsTripped += num
	def dump(self):
		return [self.name, self.threadCount, self.scoredThread, self.replyCount, self.totalScore, self.aveRating, self.numFlags]

class Thread: # object to enclose all data concerning one thread
	def __init__(self, me="", name="", url="", rating="", replies=[], numRep = 0, views = 0, content = "", date = "", numFlags=0, flag=False):
		self.base_url = "https://sinister.ly/Thread-"
		self.user = me # profile this post belongs to
		self.threadName = name # name of thread
		self.url = url
		self.threadRating = rating # Out of 5 stars
		self.replies = replies # usernames for all users who have replied on thread
		self.numReplies = numRep # number of replies
		self.views = views # number of thread views
		self.content = content # content of original post
		self.date = date # date post was posted
		self.numFlags = numFlags
		self.flag = flag
	def setUser(self, user):
		self.user = user
	def setName(self, name):
		self.threadName = name
	def setURL(self, url):
		self.threadUrl = url
	def setRating(self, rating):
		self.threadRating = rating
	def addReplier(self, replier):
		self.commenters.append(commenter)
	def setNumReplies(self, num):
		self.numReplies = int(num)
	def setNumViews(self, num):
		self.views = int(num)
	def setTime(self, string):
		self.date = string
	def setContent(self, string):
		self.content = string.lower()
	def setNumFlags(self, num):
		self.numFlags = num
	def setFlag(self, flag):
		self.flag = flag
	def dump(self):
		return [self.threadName, self.user, self.date, self.numReplies, self.views, self.threadRating, self.threadUrl, self.content, self.flag]
