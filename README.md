## Synopsis

This tool conducts sentiment analysis on tweets obtained from twitter's public search API. Sentiment analysis determining the "attitude" of tweets (how "positive" or "negative") about a particular topic.
The analysis is carried out using AFINN data which is a list of words that have been manually labelled an integer rating between minus 5 (negative) and plus 5 (positive). This sentiment is then used along 
with the popularity of each tweet to generate a pearson coefficient that shows the correlation between sentiment and number of times retweeted.  
