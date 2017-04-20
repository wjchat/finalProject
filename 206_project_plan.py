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



def get_user_info(user):  #function to get information about a users timeline
	if type(user) == str:
		unique_identifier = '@'+ user 
	if type(user) == int:
		unique_identifier = str(user)

	if unique_identifier in CACHE_DICTION: #checks for the cached data
		print('using cached data for ' + unique_identifier)
		return CACHE_DICTION[unique_identifier]
	else:
		print('retrieving data from the web for ' + unique_identifier)
		search_results = api.get_user(unique_identifier)
		CACHE_DICTION[unique_identifier] = search_results

		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

		return(CACHE_DICTION[unique_identifier])



def get_tweets(keyword):
	unique_identifier = 'twitter-'+ keyword #creates flexible unique identifier depending on search query

	if unique_identifier in CACHE_DICTION:
		print('using cached data for tweets'+ unique_identifier)

	else:
		print('getting new data from the web for tweets'+ unique_identifier)

		search_results = api.search(q = keyword) #returns a list

		CACHE_DICTION[unique_identifier] = search_results

		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	searcher = CACHE_DICTION[unique_identifier] #puts returned list into variable searcher

	tweets = []
	
	for item in searcher['statuses']:
		if keyword.lower() in item['text'].lower():
			tweets.append(item)
	return tweets

#print(get_tweets('s')[0])

#write function which returns average number of favorites of top 10 tweets mentioning an actor, then appends this information as a dictionary item in user list of dictionaries 
#takes dictionary of actor_tweets and returns a dictionary where the key is the actors name and the value is the average amount of favs of tweets mentioning them

def average_favs(actor_and_tweets_dict): 
	dic_of_favs = {}

	for each in actor_and_tweets_dict:
		actor = each
		tweet_list = actor_and_tweets_dict[each]
		total_favs = 0

		for tweet in tweet_list:
			total_favs += tweet.favs


		dic_of_favs[actor] = total_favs/len(tweet_list)
		
	return dic_of_favs



def get_neighborhood(tweet_text):		#funciton from hw 7  ##returns neighborhood of users
	users = re.findall('@(\w+)', tweet_text)
	users_final = [(user) for user in users]
	return users_final #returns list of users



class Tweets(object): #defines tweet class to make accessing information about it a lot lot lot easier
	def __init__(self, tweet):
		self.text = tweet['text']
		self.id = tweet['id_str']
		self.user_id = tweet['user']['id_str']
		self.favs = tweet['favorite_count']
		self.rts = tweet['retweet_count']
		self.movie_derived = ''



class Movie(object): #define movie class with appropriate data
	def __init__(self, movie, year):
		movie = get_movie_info(movie, year)
		self.title = movie['Title']
		self.ID = movie['imdbID']
		self.imdb_rating = movie['imdbRating']
		self.actors = movie['Actors']
		self.languages = movie['Language']
		self.rating = movie['Rated']
		self.box_office = movie['BoxOffice']
		self.year = movie['Year']
		self.director = movie['Director']
		self.average_favs_lead = 0

	#define str method to print the name, year, and actors of a movie
	#should print "movie, year, staring lead_actor"

	def __str__(self):
		return '{}, {} staring {}'.format(self.title, self.year, self.actors)

	#define method which returns the number of languages the movie is in

	def num_languages(self):
		x = 0
		for each in self.languages.split():
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

movies = [] #list of movie objects
for each in movie_lst:
	movies.append(movie_lst[each])

#for each in movie_lst:
#	print(movie_lst[each].title)



#write a for loop which searches for the lead actor and returns a list of tweets mentioning aforementioned lead

tweets = [] #list of tweet objects
actor_tweets = {} #dictionary where key is actor and value is list of tweet objects associated with them 

#create dictionary where key is actor name and value is list of tweet objects associated with that actor


for movie in movie_lst:
	lead = movie_lst[movie].get_lead()

	movie_tweets = get_tweets(lead)
	#convert tweet list into tweet objects

	temp_list = []

	for tweet in movie_tweets:
		temp_list.append(Tweets(tweet))

	actor_tweets[lead] = temp_list


	for tweet in movie_tweets:
		tweets.append(Tweets(tweet))






###write loop which takes tweet as input and adds the instance variable of movie derived for each tweets by matching lead actor with tweet text

for movie in movies:
	for tweet in tweets:
		text = tweet.text.lower()
		if movie.get_lead().lower() in text:
			tweet.movie_derived = movie.title




#write code to get information about every user in the neighborhood and append that to a list of users

users_list = []

for tweet in tweets:
	users_list.append(get_neighborhood(tweet.text))
	

users_list = [user for lst in users_list for user in lst] #more lst comprehension

for tweet in tweets:
	users_list.append(int(tweet.user_id))

#print(users_list)

#get information from timeline of every mentioned user

user_info = []

user_list_uniques = []

for user in users_list:
	if user not in user_list_uniques:
		user_list_uniques.append(user)

for user in user_list_uniques:
	user_info.append(get_user_info(user))

#print(user_info['blogTO'])
#print(type(actor_tweets['Ryan Gosling'][0]))


##########



average_favorites_dict = average_favs(actor_tweets) #creates dictionary invoking ^ function

for movie in movies:
	for lead in average_favorites_dict:
		if movie.get_lead() == lead:
			movie.average_favs_lead = average_favorites_dict[lead]
	#print(movie.average_favs_lead, movie.get_lead())     				WE GOOD
#print(average_favorites_dict)

#create database with three tables Tweets, Users, and Movies
conn = sqlite3.connect('final_project.db')
cur = conn.cursor()


#create tweet table including text, id, user who posted, movie search the tweet derived from, # of favorites, # of retweets

cur.execute("DROP TABLE IF EXISTS Tweets")
table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += 'Tweets(text TEXT, id TEXT, user_id TEXT, favs INTEGER, retweets INTEGER, movie_derived TEXT)'



cur.execute(table_spec)

#create user table representing user ID, screen name, number of favs the user has made, and average number of favorites for top 10 tweets

cur.execute('DROP TABLE IF EXISTS Users')
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Users(id TEXT, screen_name TEXT, user_favs INTEGER )'
cur.execute(table_spec)

#create movie table including movie ID, title, director,# of languages, IMDB rating, lead actor, and box office 

cur.execute('DROP TABLE IF EXISTS Movies')
table_spec = 'CREATE TABLE IF NOT EXISTS  '
table_spec += 'Movies(id TEXT, title TEXT, director TEXT, num_languages INTEGER, rating TEXT, lead TEXT, box_office INTEGER, average_favs_lead INTEGER, imdb_rating INTEGER)'

cur.execute(table_spec)

#write statements to load data into all three tables

statements = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
info = []


for tweet in tweets:
	info.append((tweet.text, tweet.id, tweet.user_id, tweet.favs, tweet.rts, tweet.movie_derived))
for each in info:
	cur.execute(statements, each)

statements = 'INSERT INTO Users VALUES (?, ?, ?)'
info = []

for user in user_info:
	info.append((user['id_str'], user['name'], user['favourites_count']))
for each in info:
	cur.execute(statements, each)

statements = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
info = []
for movie in movies:
	info.append((movie.ID, movie.title, movie.director, movie.num_languages(), movie.rating, movie.get_lead(), movie.box_office, movie.average_favs_lead, movie.imdb_rating))
for each in info:
	cur.execute(statements, each)


conn.commit()




#make query that returns list of tuples where first element is the # of favorites of a tweet the second element is the box office

query = 'SELECT Tweets.favs, Movies.box_office FROM Tweets INNER JOIN Movies on Tweets.movie_derived = Movies.title'
cur.execute(query)
num_favs_box_office = cur.fetchall()


#query that returns list of tuples where the first element is the # of languages, the second element is the average number of favorites regarding a movei, and the third element is the screenname of the lead actor in the movie where imdb rating >= 8

query = 'SELECT num_languages, average_favs_lead, lead FROM Movies WHERE imdb_rating >= 8'
cur.execute(query)
num_lan_av_favs_lead = cur.fetchall()
#print(num_lan_av_favs_lead)


#query that returns list of tuples where first element is number of favs of user and second is movie derived (to see if some movies have more active users)

query2 = ('SELECT Users.user_favs, Tweets.movie_derived FROM Tweets INNER JOIN Users on Users.id = Tweets.user_id')
cur.execute(query2)
user_favs_movie = cur.fetchall()
#print(user_favs_movie)


	
#query that returns list of tuples where first element is user screenname and second element is tweet text

query = 'SELECT Users.screen_name, Tweets.text FROM Users INNER JOIN Tweets on Users.id = Tweets.user_id'
cur.execute(query)
names_and_text = cur.fetchall()


#query that returns the screen name of every account with more than 500 retweets or 500 favorites
query = 'SELECT Users.screen_name from Users INNER JOIN Tweets on Users.id = Tweets.user_id WHERE Tweets.retweets >=500 or Tweets.favs >=500'
cur.execute(query)
big_names = cur.fetchall()
#print(big_names)



#print(names_and_text[0], names_and_text[-1])
#print(len(names_and_text))

#use dictionary comprehension to make dict where key is the name of a lead has made and the value is the box office of the film

#use list comprehension to make list of words used in tweets

#use counter to find most reccurring word in the list created above 

#use regex to find mention of movie title in tweets which mention the lead actor

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

#######ALSO test tweet class and movie class (aka be sure that lists are working)
	def test_tweetlst(self):
		self.assertTrue(type(tweets[0]) == Tweets)
	def test_movie_lst(self):
		self.assertTrue(type(movie_lst[0]) == Movie)
# Write your test cases here.


## Remember to invoke all your tests...
#if __name__ == "__main__":
#	unittest.main(verbosity=2)