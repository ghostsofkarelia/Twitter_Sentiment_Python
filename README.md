## Synopsis

This application conducts sentiment analysis on tweets obtained from twitter's public search API stored in a text file. Sentiment analysis determining the "attitude" of tweets (how "positive" or "negative") about a particular topic.
The analysis is carried out using AFINN data which is a list of words that have been manually labelled an integer rating between minus 5 (negative) and plus 5 (positive). This sentiment is then used along 
with the popularity of each tweet to generate a pearson coefficient that shows the correlation between sentiment and number of times retweeted.  

##Requirements
1.) Latest version of python

2.) Scipy module installed 

Get Anaconda. It's quite useful

[Anaconda](https://www.continuum.io/downloads) 

##Installation

1.) Clone this project on your local machine

2.) Navigate to the directory

3.) Run the following commands in command prompt to try out each aspect of the tool 
	
	a.) python tweet_sentiments-win.py load_tweets data/dog.txt 
	
	b.) python tweet_sentiments-win.py popularity data/dog.txt
	
	c.) python tweet_sentiments-win.py hashtag_counts data/dog.txt

	d.) python tweet_sentiments-win.py sentiment -f data/dog.txt -s AFINN-111.csv
	
	e.) python tweet_sentiments-win.py correlation -f data/dog.txt -s AFINN-111.csv

4.) Command line doesn't display certain unicode characters properly. To make them work use the command to change the code page:
	
	chcp 1250
	
##Future Work

To integrate Twitter's search API into the project. Started work on twitter_stream.py. 

Also to integrate the stream API.