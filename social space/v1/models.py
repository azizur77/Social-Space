from django.db import models

class TweeterFeed(models.Model):
	tweeterID = models.CharField(max_length=140)
	approvedStatud = models.BooleanField()
	def __unicode__(self):
		return self.tweeterID
	
class TweetContent(models.Model):
	author = models.ForeignKey(TweeterFeed)
	textContent = models.CharField(max_length = 200) # tweets are only 140 characters
	publication_date = models.DateField()
	location = models.CharField(max_length = 200)
	inReplyTo = models.CharField(max_length = 200)

class TweetsTokenized(models.Model):
	tweeterID = models.ForeignKey(TweeterFeed)
	featureVector = models.TextField()

class TweetsFeaturized(models.Model):
	tweeterID = models.ForeignKey(TweeterFeed)
	featureVector = models.TextField()

# Create your models here.
