# Your functions go here!
import re
import json
import scipy.stats

"""Function to extract words from a tweet"""
def extract_words(sentence):
	word_list = re.split("[^\w\']", sentence['text']) #split sentences by word
	for word in word_list:
		if not word:
			word_list.remove(word) #Filter
	return word_list

"""Function to load sentiment data from csv file and create a dictionary of sentiments"""
def load_sentiments(file_name):
	dictionary = {}
	file = open(file_name)
	for row in file:
		row = row.strip().split(',') #remove the commas
		dictionary[row[0]] = row[1]
	return dictionary

"""Function to calculate sentiment of a string using a predefined dictionary of sentiments"""
def text_sentiment(string, dictionary):
	word_list = extract_words(string) 
	sum_of_sentiments = 0 #Var that'll hold the sum of sentiments
	for words in word_list:
		if words in dictionary:
			sum_of_sentiments = sum_of_sentiments + int(dictionary[words])
	return sum_of_sentiments

"""Function to load tweets from a file"""
def load_tweets(filename):
	tweet_dictionary = []
	dictionary = {}
	tweet = open(filename) #open tweet file to read
	for line in tweet:
	  json_line = json.loads(line) #get a json object from a string
	  dictionary['created_at'] = json_line['created_at']
	  dictionary['user.screen_name'] = json_line['user']['screen_name']
	  dictionary['text'] = json_line['text']
	  dictionary['retweet_count'] = json_line['retweet_count']
	  dictionary['favorite_count'] = json_line['favorite_count']
	  dictionary['hashtags'] = []
	  hash_tag_list = json_line['entities']['hashtags']
	  for value in hash_tag_list:
	   dictionary['hashtags'].append(value['text']) #picking out hashtag text to add to tweet_dictionary
	  tweet_dictionary.append(dictionary.copy())
	return tweet_dictionary

"""Function to calculate popularity of tweets"""
def popularity(filename):
  tweets = load_tweets(filename)
  retweets = 0
  favorites = 0
  for value in tweets:
    retweets += float(value['retweet_count'])
    favorites += float(value['favorite_count'])
  return (retweets / len(tweets), favorites / len(tweets)) #Return a tuple of Average number of retweets and average number of favorites

"""Function to return a hashtag count of tweets"""
def hashtag_counts(filename):
  tweets = load_tweets(filename)
  count = {}
  for counter in tweets:
    for j in counter['hashtags']:
      try:
        count[j] += 1
      except:
        count[j] = 1
  hashtags = count.items()
  hashtags_switched = [(val, key) for key, val in hashtags]
  hashtags_switched.sort(reverse = True)
  hashtags = [(val, key) for key, val in hashtags_switched]
  return hashtags

"""Creating a list of tweets with a sentiment key, value pair"""
def tweet_sentiments(Tweet_file,Sentiment_file):
  tweet_list = load_tweets(Tweet_file)
  new_tweet_list = []
  sentiment_dictionary = load_sentiments(Sentiment_file) #getting the sentiment dictionary object
  for tweet in tweet_list:
    tweet_sentiment = text_sentiment(tweet,sentiment_dictionary) #Finding the sentiment using tweet and dicitionary for reference
    tweet["sentiment"] = tweet_sentiment #assigning sentiment to a key in the tweet object
    new_tweet_list.append(tweet.copy()) 
  return new_tweet_list

"""Function to show the pearson correlation coefficient between sentiments and retweets"""
def popular_sentiment(Tweet_file,Sentiment_file):
  tweet_list = []
  corr_list = []
  retweet_list = []
  sentiment_list = []
  corr_tuple = ()
  tweet_list = tweet_sentiments(Tweet_file,Sentiment_file)
  for tweet in tweet_list:
    sentiment = float(tweet["sentiment"])
    retweet_count = float(tweet["retweet_count"])
    retweet_list.append(retweet_count)
    sentiment_list.append(sentiment)
  correlation_value = scipy.stats.pearsonr(sentiment_list,retweet_list)
  return correlation_value[0]

# Run the method specified by the command-line
if __name__ == '__main__':
  #for parsing and friendly command-line error messages
  import argparse 
  parser = argparse.ArgumentParser(description="Analyze Tweets")
  subparsers = parser.add_subparsers(description="commands", dest='cmd')
  subparsers.add_parser('load_tweets', help="load tweets from file").add_argument('filename')
  subparsers.add_parser('popularity', help="show average popularity of tweet file").add_argument('filename')
  subparsers.add_parser('extract_words', help="show list of words from text").add_argument(dest='text', nargs='+')
  subparsers.add_parser('load_sentiments', help="load word sentiment file").add_argument('filename')

  sentiment_parser = subparsers.add_parser('sentiment', help="show sentiment of data. Must include either -f (file) or -t (text) flags.")
  sentiment_parser.add_argument('-f', help="tweets file to analyze", dest='tweets')
  sentiment_parser.add_argument('-t', help="text to analyze", dest='text', nargs='+')
  sentiment_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)

  subparsers.add_parser('hashtag_counts', help="show frequency of hashtags in tweet file").add_argument('filename')

  hashtag_parser = subparsers.add_parser('hashtag', help="show sentiment of hashtags.")
  hashtag_parser.add_argument('-f', help="tweets file to analyze", dest='tweets', required=True)
  hashtag_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)
  hashtag_parser.add_argument('-q', help="hashtag to analyze", dest="query", default=None)

  correlation_parser = subparsers.add_parser('correlation', help="show correlation between popularity and sentiment of tweets")  
  correlation_parser.add_argument('-f', help="tweets file to analyze", dest='tweets', required=True)
  correlation_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)

  args = parser.parse_args()

  try:
    if args.text:
      args.text = ' '.join(args.text) #combine text args
  except:
    pass

  #print(args) #for debugging

  # call function based on command given
  if args.cmd == 'load_tweets':
    tweets = load_tweets(args.filename)
    for tweet in tweets:
      print(str(tweet).encode('utf8'))

  elif args.cmd == 'popularity':
    print(popularity(args.filename))

  elif args.cmd == 'hashtag_counts':
    for key,value in hashtag_counts(args.filename):
      print(str(key).encode('utf8'),":",value)

  elif args.cmd == 'extract_words':
    print(extract_words(args.text))

  elif args.cmd == 'load_sentiments':
    for key,value in sorted(load_sentiments(args.filename).items()):
      print(key,value)

  elif args.cmd == 'sentiment':
    if args.tweets == None: #no file, do text
      sentiment = text_sentiment(args.text, load_sentiments(args.sentiments))
      print('"'+args.text+'":', sentiment)
    elif args.text == None: #no text, do file
      rated_tweets = tweet_sentiments(args.tweets, args.sentiments)
      for tweet in rated_tweets:
        print(str(tweet['text']).encode('utf8')," -> Sentiment: ",str(tweet['sentiment'])) #encoding in utf-8 to include a large subset of characters
    else:
      print("Must include -f (tweet filename) or -t (text) flags to calculate sentiment.")

  elif args.cmd == 'correlation':
    print("Correlation between popularity and sentiment: r="+str(popular_sentiment(args.tweets, args.sentiments)))