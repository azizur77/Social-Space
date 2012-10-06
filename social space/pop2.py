# We setup the enviroment variable here

from django.core.management import setup_environ
import settings
import feedparser

setup_environ(settings)
 
# From now you can use ay Django elements
import time
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import nltk
from nltk.stem.porter import *
stemmer = PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
	content = ''
	text = nltk.word_tokenize(text)
	for w in text: 
		if w.lower() not in stopwords:
			content = content + stemmer.stem(w.lower()) + ' '
	return content
	
def remove_junk(text,wordlist):
	#removes the words that are not in the feature vector
	content = ''
	text = nltk.word_tokenize(text)
	for w in text: 
		if w not in wordlist:
			content = content + w + ' '
	return content
def strip_ml_tags(in_text):
	"""Description: Removes all HTML/XML-like tags from the input text.
	Inputs: s --> string of text
	Outputs: text string without the tags
	
	# doctest unit testing framework

	>>> test_text = "Keep this Text <remove><me /> KEEP </remove> 123"
	>>> strip_ml_tags(test_text)
	'Keep this Text  KEEP  123'
	"""
	# convert in_text to a mutable object (e.g. list)
	s_list = list(in_text)
	i,j = 0,0
	
	while i < len(s_list):
		# iterate until a left-angle bracket is found
		if s_list[i] == '<':
			while s_list[i] != '>':
				# pop everything from the the left-angle bracket until the right-angle bracket
				s_list.pop(i)
				
			# pops the right-angle bracket, too
			s_list.pop(i)
		else:
			i=i+1
			
	# convert the list back into text
	join_char=''
	return join_char.join(s_list)


from socialspace.v1.models import TweeterFeed, TweetsTokenized, TweetsFeaturized
Tweeps = TweeterFeed.objects.all().filter(approvedStatud=1)
print Tweeps
MyLongString = ''
for i in Tweeps:
	print i.tweeterID
	print i.id
	print '-----------'
	# Replace USERNAME with your twitter username
	url = u'http://twitter.com/'+ i.tweeterID+'?page=%s'
	
	LongStringForThisProfile = ''
	for x in range(3): #getting only 3 pages
		f = urlopen(url % x)
		soup = BeautifulSoup(f.read())
		f.close()
		tweets = soup.findAll('span', {'class': 'entry-content'})
		if len(tweets) == 0:
			break
		for x in tweets:
			a = strip_ml_tags(x.renderContents())
			#print  nltk.word_tokenize(remove_stopwords(a)) 
			b=remove_stopwords(a)
			print  b
			MyLongString = MyLongString + b + ' ' 
			LongStringForThisProfile = LongStringForThisProfile + b + ' '
		# being nice to twitter's servers
		time.sleep(1)

	try:
		ThisTokenized = TweetsTokenized.objects.get(tweeterID=i.id)
		print ThisTokenized
		ThisTokenized.featureVector = LongStringForThisProfile
		ThisTokenized.save()
		
	except:
		# making a new entry in the database
		t1=TweetsTokenized(tweeterID=i, featureVector = LongStringForThisProfile)
		t1.save()
		print "Making a new row"
	
myltext = nltk.Text(nltk.word_tokenize(MyLongString)) 	
print myltext
fdist = nltk.FreqDist(myltext)
vocabulary = fdist.keys()
#print vocabulary[:50]
#print fdist

#getting top 200 words
numberOfTopWords = 200
print "--------------------------"
print vocabulary[:numberOfTopWords]
finalFeatureWords = vocabulary[:numberOfTopWords]
print "--------------------------"

for i in Tweeps:
	print i.tweeterID
	print i.id
	print '-----------'
	
	
	
	ThisTokenized = TweetsTokenized.objects.get(tweeterID=i.id)
	finaloutput = remove_junk(ThisTokenized.featureVector,finalFeatureWords)
	
	try:
		ThisFeaturized = TweetsFeaturized.objects.get(tweeterID=i.id)
		ThisFeaturized.featureVector = nltk.FreqDist(finaloutput)
		ThisFeaturized.save()
		
	except:
		# making a new entry in the database
		t1=TweetsFeaturized(tweeterID=i, featureVector = nltk.FreqDist(finaloutput))
		t1.save()
		print "Making a new row"
	

 
 
 
