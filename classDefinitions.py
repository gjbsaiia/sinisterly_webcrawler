#!/usr/bin/python

# Griffin Saiia, Gjs64
# Computer Security
# Underground Market Research
# github: https://github.com/gjbsaiia

class Session:
	def __init__(self):
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
	def __init__(self, name, threads=0, replies=0, score=0, rating=0):
		self.name = name # API Key to optional Google Sheet functionality
		self.base_url = "https://sinister.ly/User-"
		self.profile_url = self.base_url+name
		self.threadCount = threads
		self.replyCount = replies
		self.totalScore = score
		self.aveRating = rating
	def addThread(self):
		self.threadCount += 1
	def addReply(self):
		self.replyCount += 1
	def updateAveRating(self, rating):
		self.totalScore += int(rating)
		self.aveRating = self.totalScore / self.threadCount
	def dump(self):
		return [self.name, self.threadCount, self.replyCount, self.totalScore, self.aveRating]

class Thread: # object to enclose all data concerning one thread
	def __init__(self, me, url="", rating="", replies=[], numRep = 0, views = 0, content = "", date = ""):
		self.base_url = "https://sinister.ly/Thread-"
		self.user = me # profile this post belongs to
		self.threadUrl = "" # thread url
		self.threadName = "" # name of thread
		self.setURL(url)
		self.threadRating = rating # Out of 5 stars
		self.replies = replies # usernames for all users who have replied on thread
		self.numReplies = numRep # number of replies
		self.views = views # number of thread views
		self.content = content # content of original post
		self.date = date # date post was posted
	def setURL(self, url):
		if(url):
			self.threadUrl = url
			self.threadName = self.threadURL.split(self.base_url)[1]
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
		self.content = string
	def dump(self):
		return [self.threadName, self.threadUrl, thread.user, thread.date, thread.numReplies, thread.views, thread.content]
