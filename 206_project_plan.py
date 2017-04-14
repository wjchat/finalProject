## Your name:
## The option you've chosen: Project 2

# Put import statements you expect to need here!
import re
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import sys #solves weird character problem i often get
import codecs
import twitter_info
import requests

sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

#twitter info for api
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#caching pattern
CACHE_FNAME = "SI206_project3_cache.json"
try:
	cache_file_object = open(CACHE_FNAME, 'r')
	cache_contents = cache_file_object.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file_object.close()
except:
	CACHE_DICTION = {}


class Movie(object):
	def __init__(self, title, year):
		base_url = "http://www.omdbapi.com/?"
		r = requests.get(base_url)




class Task1(unittest.TestCase):
	def test_movie_caching(self):
		fstr = open("SI206_final_project_cache.json","r").read()
		self.assertTrue("Elf" in fstr)
	def test_movie_tweets(self):
		self.assertEqual(type(elf_tweets),type([]))
	def test_lead_has_5_tweets(self):
		self.assertTrue(lead_tweets >= 5)
	def test_tweets_4(self):
		conn = sqlite3.connect('final_project_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT tweet_id FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(result[0][0] != result[19][0], "Testing part of what's expected such that tweets are not being added over and over (tweet id is a primary key properly)...")
		if len(result) > 20:
			self.assertTrue(result[0][0] != result[20][0])
		conn.close()
	def test_lead_actors_func(self):
		self.assertEqual(get_lead(Elf), 'Will Ferrell')
	def test_tweet_type(self):
		self.assertTrue(type(elf_tweets[0].text) == str)
	def test_fav_type(self):
		self.assertTrue(type(elf_tweets[0].favorites) == int)
	def test_average_favs_type(self):
		self.assertTrue(type(average_faves['Will Ferrell']) == int)
# Write your test cases here.


## Remember to invoke all your tests...