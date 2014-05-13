# This file does the actual sentiment analysis on a per paragraph basis
import nltk
import re
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from random import randint
import collections, itertools
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

def getImportance(word, tfidfArray):
	for elem in tfidfArray:
		if word == elem["word"]:
			return elem["imp"]
	return 0

def returnPureWord(word):
	retVal = word.replace(",", "")
	retVal = word.replace("\'", "")
	retVal = word.replace("\"", "")
	retVal = word.replace(".", "")
	retVal = word.replace("\n", "")
	return retVal

def sentimentTag(paragraph):
	sentences = nltk.sent_tokenize(paragraph)
	pos = 0
	neg = 0
	for sentence in sentences:
		wordList = [sentence]
		ret = classifier.classify(word_feats(sentence))
		if(ret == 'neg'):
			neg = neg + 1
		elif(ret == 'pos'):
			pos = pos + 1
	return (float(pos-neg)/len(sentences)) * 100

def word_feats(words):
    return dict([(word, True) for word in words])

# Train from blankTrain.txt
train=[('He no longer was afraid of anything.', 'pos'), ('It was lean with long-standing hunger.', 'neg'), ('This served as a relish, and his hunger increased mightily; but he was too old in the world to forget his caution.', 'neg'), ('There were hisses from the crowd and cries of protest, but that was all.', 'neg'), ('Something was impending.', 'neg'), ('Grey Beaver never petted nor caressed.', 'neg'), ('With his one eye the elder saw the opportunity.', 'pos'), ('Or at least White Fang thought he was deserted, until he smelled out the master\'s canvas clothes-bags alongside of him, and proceeded to mount guard over them.', 'pos'), ('They made their bread with baking-powder.', 'pos'), ('White Fang was too helpless to defend himself, and it would have gone hard with him had not Grey Beaver\'s foot shot out, lifting Lip-lip into the air with its violence so that he smashed down to earth a dozen feet away.', 'pos'), ('The roar of it no longer dinned upon his ears.', 'pos'), ('Then a huge dog was thrust inside, and the door was slammed shut behind him.', 'neg'), ('This was repeated a number of times.', 'pos'), ('Then she sprang away, up the trail, squalling with every leap she made.', 'pos'), ('\"An\' I\'ll bet it ain\'t far from five feet long.', 'pos'), ('One chance in a thousand is really optimistic.', 'neg'), ('Bitter experiences these, which, perforce, he swallowed, calling upon all his wisdom to cope with them.', 'neg'), ('There was a leap, swifter than his unpractised sight, and the lean, yellow body disappeared for a moment out of the field of his vision.', 'pos'), ('But this was only when the master was not around.', 'neg'), ('Five minutes later the landscape was covered with fleeing boys, many of whom dripped blood upon the snow in token that White Fang\'s teeth had not been idle.', 'neg') ]
all_words = set(word.lower() for passage in train for word in nltk.word_tokenize(passage[0]))
t = [({word: (word in nltk.word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]

classifier = nltk.NaiveBayesClassifier.train(t)

toWrite = open('../web/data/para.tsv', 'wr+')
toWrite.write("pos\tsentiment\n")
toWrite.close()
currPara = 1
toAppend = open('../web/data/para.tsv', 'a')
text = open('WhiteFang.txt', 'r').read()
tokens = re.split('\n\n\n|\n\n', text)
size = len(tokens)
currIter = 0
p = [1,1,1,1,1]
# p will hold the starting paragraph number for that section

myDict = [dict(num=0, para="", sentiment=0)]
for i in range(0,size):
	sentiment = sentimentTag(tokens[i])
	myDict.append(dict(num=currPara, para=tokens[i], sentiment=sentiment))
	if("PART" in tokens[i]):
		p[currIter] = currPara
		currIter = currIter + 1
	if currPara == 1095:
		toAppend.write(str(currPara) + "\t" + str(sentiment))
	else:			
		toAppend.write(str(currPara) + "\t" + str(sentiment) + "\n")
	currPara=currPara+1
p.append(currPara)
tfidf_text = open("tfidf.txt")
lines = tfidf_text.readlines()
tfidf = [dict(word="", imp=0)]
for line in lines:
	split = line.split("\t")
	tfidf.append(dict(word=split[0], imp=float(split[1][:len(split[1])-1])))
tfidf = tfidf[1:]	
color = "all" #Can be "all", "both", "green", or "red"
if(color == "all" or "both"):
	for i in range(0,5):
		color = open("../web/part" + str(i+1) + ".html", "wr+")
		color.write("<!DOCTYPE html>\n")
		color.write("<link rel=\"stylesheet\" href=\"css/part.css\" type=\"text/css\" media=\"screen\" />\n")
		color.write("<body><div class=\"backButton\" onClick=\"location.href='index.html'\"> Back to Visualization </div>")
		color.write("<br><div class=\"gButton\" onclick=\"location.href='greenPart" + str(i+1) + ".html';\"> &nbsp;Positive&nbsp; </div><div class=\"rButton\" onclick=\"location.href='redPart" + str(i+1) + ".html';\"> &nbsp;Negative&nbsp; </div><br><br>")
		start = p[i]
		end = p[i+1]-1
		while start <= end:
			green = False
			textColor = 255*(float(myDict[start]["sentiment"])/100)
			if(textColor > 0):
				textColor = hex(int(textColor))
				green = True
			elif(textColor < 0):
				textColor = hex(-int(textColor))
			else:
				textColor = hex(0)
			words = myDict[start]["para"].split(" ")
			if(green):
				placeholderlinesopythondoesntcomplain = 0
				color.write("<p style=\"color:#00" + str(textColor)[2:] + "00;\">") #Comment this out for red
			else:
				color.write("<p style=\"color:#" + str(textColor)[2:] + "0000;\">")
			for word in words:
				importance = getImportance(returnPureWord(word), tfidf)
				opacity = importance/tfidf[0]["imp"]
				opacity = opacity/2 + 0.5
				color.write("<span style=\"opacity:" + str(opacity) + ";\">" + str(word) + "</span> ")
			color.write("</p>\n\n")
			start = start + 1
if(color == "all" or "green"):
	for i in range(0,5):
		color = open("../web/greenPart" + str(i+1) + ".html", "wr+") #Green
		color.write("<!DOCTYPE html>\n")
		color.write("<link rel=\"stylesheet\" href=\"css/part.css\" type=\"text/css\" media=\"screen\" />\n")
		color.write("<body><div class=\"backButton\" onClick=\"location.href='index.html'\"> Back to Visualization </div>")
		color.write("<br><div class=\"bButtonL\" onclick=\"location.href='part" + str(i+1) + ".html';\"> &nbsp;Positive and Negative&nbsp; </div><div class=\"rButton\" onclick=\"location.href='redPart" + str(i+1) + ".html';\"> &nbsp;Negative&nbsp; </div><br><br>")
		start = p[i]
		end = p[i+1]-1
		while start <= end:
			green = False
			textColor = 255*(float(myDict[start]["sentiment"])/100)
			if(textColor > 0):
				textColor = hex(int(textColor))
				green = True
			elif(textColor < 0):
				textColor = hex(-int(textColor))
			else:
				textColor = hex(0)
			words = myDict[start]["para"].split(" ")
			if(green):
				color.write("<p style=\"color:#00" + str(textColor)[2:] + "00;\">")
			for word in words:
				if green: 
					importance = getImportance(returnPureWord(word), tfidf)
					opacity = importance/tfidf[0]["imp"]
					opacity = opacity/2 + 0.5
					color.write("<span style=\"opacity:" + str(opacity) + ";\">" + str(word) + "</span> ")
			if(green):
				color.write("</p>\n\n")
			start = start + 1
if(color == "all" or "red"):
	for i in range(0,5):
		color = open("../web/redPart" + str(i+1) + ".html", "wr+") #Red
		color.write("<!DOCTYPE html>\n")
		color.write("<link rel=\"stylesheet\" href=\"css/part.css\" type=\"text/css\" media=\"screen\" />\n")
		color.write("<body><div class=\"backButton\" onClick=\"location.href='index.html'\"> Back to Visualization </div>")
		color.write("<br><div class=\"gButton\" onclick=\"location.href='greenPart" + str(i+1) + ".html';\"> &nbsp;Positive&nbsp; </div><div class=\"bButton\" onclick=\"location.href='part" + str(i+1) + ".html';\"> &nbsp;Positive and Negative&nbsp; </div><br><br>")
		start = p[i]
		end = p[i+1]-1
		while start <= end:
			green = False
			textColor = 255*(float(myDict[start]["sentiment"])/100)
			if(textColor > 0):
				textColor = hex(int(textColor))
				green = True
			elif(textColor < 0):
				textColor = hex(-int(textColor))
			else:
				textColor = hex(0)
			words = myDict[start]["para"].split(" ")
			if not green:
				color.write("<p style=\"color:#" + str(textColor)[2:] + "0000;\">")
			for word in words:
				if not green: 
					importance = getImportance(returnPureWord(word), tfidf)
					opacity = importance/tfidf[0]["imp"]
					opacity = opacity/2 + 0.5
					color.write("<span style=\"opacity:" + str(opacity) + ";\">" + str(word) + "</span> ")
			if not green:
				color.write("</p>\n\n")
			start = start + 1