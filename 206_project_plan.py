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



#twitter info for api, should be in twitter_info file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#caching pattern
CACHE_FNAME = "SI206_final_cache.json"
try:
	cache_file_object = open(CACHE_FNAME, 'r')
	cache_contents = cache_file_object.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file_object.close()
except:
	CACHE_DICTION = {}


def get_movie_info(title, year):
	unique_identifier = title + str(year) + 'movie'

	if unique_identifier in CACHE_DICTION:

		print('Using cached data for', unique_identifier)
		return CACHE_DICTION[unique_identifier]

	else:
		print('retrieving data from the web for', unique_identifier)
		base_url = "http://www.omdbapi.com/?" #base url
		params = {'t': title, 'y': year} #search parameters

		r = requests.get(base_url, params = params)
		CACHE_DICTION[unique_identifier] = json.loads(r.text)

		f = open(CACHE_FNAME, 'w') #writes movie api results to the cache file
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		
		return CACHE_DICTION[unique_identifier] #returns dictionary of movie information

def get_user_tweets(user):  #function to get information about a users timeline
	unique_identifier = user 
	if unique_identifier in CACHE_DICTION: #checks for the cached data
		print('using cached data for ' + unique_identifier)
		return CACHE_DICTION[unique_identifier]
	else:
		print('retrieving data from the web for ' + unique_identifier)
		search_results = api.user_timeline(unique_identifier)
		CACHE_DICTION[unique_identifier] = search_results

		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

		return(CACHE_DICTION[unique_identifier])


class Movie(object): #define movie class with appropriate data
	def __init__(self, movie, year):
		movie = get_movie_info(movie, year)
		self.title = movie['Title']
		self.ID = movie['imdbID']
		self.rating = movie['imdbRating']
		self.actors = movie['Actors']
		self.languages = movie['Language']
		self.rating = movie['Rated']
		self.box_office = movie['BoxOffice']
		self.year = movie['Year']
		self.director = movie['Director']

	#define str method to print the name, year, and actors of a movie
	#should print "movie, year, staring lead_actor"

	def __str__(self):
		return '{}, {} staring {}'.format(self.title, self.year, self.actors)

	#define method which returns the number of languages the movie is in

	def num_languages(self):
		x = 0
		for each in self.languages:
			x += 1
		return x

	#method which returns the name of the lead (highest paid) actor 

	def get_lead(self):
		words = self.actors.split()
		lead = words[0] + ' ' + words[1]
		lead = lead[:-1]
		return lead


#define list of tuples of movies and years to use for later search

searchable_movies = [('La La Land', 2016), ('Moonlight', 2016), ('Arrival', 2016), ('Jackie', 2016), ('Deadpool', 2016)]

#write for loop which creates an instance of class movie for each movie in above list and iterates those movies to a list

movie_lst = {}

for each in searchable_movies:
	mov = Movie(each[0], each[1])
	movie_lst.update({mov.title: mov})

#for each in movie_lst:
#	print(movie_lst[each].get_lead())



#write a for loop which uses get_user_tweets to return information about each leads timeline and then saves this information in a list of dictionaries

user_info = []

for each in movie_lst:
	user_info.append(get_user_tweets(movie_lst[each].get_lead()))


#write code to get information about every user in the neighborhood and append that to the list mentioned above

def get_twitter_users(tweet):		#funciton from hw 7
	users = re.findall('@(\w+)', tweet)
	users_final = [(user) for user in users]
	return users_final


#write function which returns average number of favorites of users top 10 tweets, then appends this information as a dictionary item in user list of dictionaries 

#create database with three tables Tweets, Users, and Movies
conn = sqlite3.connect('final_project.db')
cur = conn.cursor()


#create tweet table including text, id, user who posted, movie search the tweet derived from, # of favorites, # of retweets

cur.execute("DROP TABLE IF EXISTS Tweets")
table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += 'Tweets(text TEXT, id TEXT, user TEXT, movie_derived TEXT, favs INTEGER, retweets INTEGER)'
cur.execute(table_spec)

#create user table representing user ID, screen name, number of favs the user has made, and average number of favorites for top 10 tweets

cur.execute('DROP TABLE IF EXISTS Users')
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Users(id TEXT, screen_name TEXT, user_favs INTEGER, average_favs INTEGER)'
cur.execute(table_spec)

#create movie table including movie ID, title, director,# of languages, IMDB rating, lead actor, and box office 

cur.execute('DROP TABLE IF EXISTS Movies')
table_spec = 'CREATE TABLE IF NOT EXISTS  '
table_spec += 'Movies(id TEXT, title TEXT, director TEXT, num_languages INTEGER, rating TEXT, lead TEXT, box_office INTEGER)'
cur.execute(table_spec)

#write statements to load data into all three tables

#make query that returns list of tuples where first element is the # of favorites of a tweet the second element is the box office, and the third element is the movie it derived from

#query that returns list of tuples where the first element is the # of languages, the second element is the average number of favorites for top 10 tweets, and the third element is the screenname of the lead actor in the movie

#query that returns list of tuples where first element is number of favs lead has made and the second element is the box office 

#query that returns list of tuples where first element is user screenname and second element is tweet text

#use dictionary comprehension to make dict where key is the name of a lead has made and the value is the box office of the film

#use list comprehension to make list of words used in tweets

#use counter to find most reccurring word in the list created above 

#map average of favorites and box office number and saves this information in a list of tuples

#writes information^ to a text file in normal english which presents insight into the relationship of social media and box office among other things


class Task1(unittest.TestCase):
	def test_movie_caching(self):
		fstr = open("SI206_final_cache.json","r").read()
		self.assertTrue("La La Land2016movie" in fstr)
	def test_movie_tweets(self):
		self.assertEqual(type(elf_tweets),type([]))
	def test_lead_has_5_tweets(self):
		self.assertTrue(lead_tweets >= 5)
	def test_tweets_4(self):
		conn = sqlite3.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT id FROM Tweets');
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
#if __name__ == "__main__":
#	unittest.main(verbosity=2)