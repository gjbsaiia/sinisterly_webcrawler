#!/usr/bin/python

# Griffin Saiia, Gjs64
# Computer Security
# Underground Market Research
# github: https://github.com/gjbsaiia

base_url = "https://sinister.ly/User-"

class Session:
	def __init__(self):
		self.user_manifest = {}
		self.gsheet_url = ""
		self.user_sheet = ""
		self.top_sheet = ""
		self.topUsers = []

class User: # object the encloses all your data
	def __init__(self, name):
		self.name = name # API Key to optional Google Sheet functionality
		self.profile_url = base_url+name
		self.threadCount = 0
		self.replyCount = 0
		self.totalScore = 0
		self.aveRating = 0
	def addThread(self):
		self.threadCount += 1
	def addReply(self):
		self.replyCount += 1
	def updateAveRating(self, rating):
		self.totalScore += int(rating)
		self.aveRating = self.totalScore / self.threadCount

class Post: # object to enclose all data concerning one post
	def __init__(self, me):
		self.user = me # profile this post belongs to
		self.threadUrl = "" # thread url
		self.threadRating = "" # Out of 5 stars
		self.replies = [] # usernames for all users who have replied on thread
		self.numReplies = 0 # number of replies
		self.views = 0 # number of thread views
		self.content = "" # content of original post
		self.date = "" # date post was posted
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
