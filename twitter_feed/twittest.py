import twitter		# python-twitter package
from matplotlib.pyplot import pause
import re


############################################

# secret data kept in separate file
with open('twitdat.txt') as f:
    fromFile = {}
    for line in f:
        line = line.split() # to skip blank lines
        if len(line)==3 :			# 
			fromFile[line[0]] = line[2]			
f.close()

#print fromFile

api = twitter.Api(
	consumer_key = fromFile['consumer_key'], 
	consumer_secret = fromFile['consumer_secret'], 
	access_token_key = fromFile['access_token_key'], 
	access_token_secret = fromFile['access_token_secret']
	)



# https://twitter.com/gov/status/743263851366449152
tweetID = 743263851366449152

# https://twitter.com/BBCMOTD/status/744216695976255492
tweetID = 744216695976255492

# https://twitter.com/BBCMOTD/status/744281250924474368
tweetID = 744281250924474368


try:
	tweet = api.GetStatus(status_id = tweetID)
except ConnectionError :
	print "should have a backup here"

candidates = ['goodguy', 'evilguy']

tags = ['precinct','ballotbox']
tags.extend(candidates)
tags = set(tags)



def getVotes(tweet,tags):
	'''
	tweet is the Status object from the python-twitter api.
	tags is a set of strings

	currently returns correct data for well-formatted tweet text
	need to include checks for multiple numbers/candidates per line, give error
	'''

	data = {}
	lines = re.split('[,;\n]', tweet.text.lower())

	for line in lines:
		if '#' not in line:			# Ignore hashtags
			for tag in tags:
				if tag in line:
					data[tag] = int(re.search(r'\d+', line).group())
	return data


def testMsgs(tweet, msgs):
	for msg in msgs:
		tweet.text = msg
		


def subTweet(tweet,msgID=0):
	t1 = "Goodguy 57 votes!\nEvilguy 100\n#Hashtest"
	t2 = "57 Goodguy\n100 Evilguy\n#Hashtest"
	t3 = "goodguy 57 evilguy 100"

	msgs = [ [], t1, t2, t3 ]

	tweet.text = msgs[msgID]
	return tweet

tweet = subTweet(tweet, 3)
print getVotes(tweet, tags)

