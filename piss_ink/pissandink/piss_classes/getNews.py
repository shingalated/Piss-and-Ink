#from django.shortcuts import render_to_response
#from django.http import HttpResponseRedirect, HttpResponse
#import pywapi
import string
import feedparser
import random

class rssParser():
	"diplays rss feeds in different ways"
	#def __init__(self):
		#self.rand = random.randint(0,4)
	def getRssTitle(self,rss,rand):
		rss_url = rss		
		feed = feedparser.parse(rss_url)				
		return feed['items'][rand]['title']
	
	def getRssLink(self,rss,rand):
		rss_url = rss
		feed = feedparser.parse(rss_url)
		return feed["items"][rand]["link"]
		
	def getRssDescription(self,rss):
		rss_url = rss
		feed = feedparser.parse(rss_url)
		return feed["channel"]["description"]
		
	
		
		