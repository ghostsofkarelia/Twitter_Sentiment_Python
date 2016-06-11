from TwitterAPI import TwitterAPI #https://github.com/geduldig/TwitterAPI
import json

# Your access information goes here
CONSUMER_KEY = "BwFbjmRLYY8HLiUWbfkx0CYul"
CONSUMER_SECRET = "BXoT2yPg1xO4XSc0x0BCNmTMrscizKM7yPwB6ILb3IVFreReNA"
ACCESS_TOKEN_KEY = "261453877-KGlzRZtoKeAM6tSWyqPMLT1SssjWMQgTtRgs4yxZ"
ACCESS_TOKEN_SECRET = "HABI0N2BK7yBHlyxERtpmUNVHpnDo545OlCOuFcWJgcwOs"

api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
print(api)

SEARCH_TERM = "dog"

## "raw" stream
#r = api.request('statuses/sample')

## stream filtering by search term
#r = api.request('statuses/filter', {'track': SEARCH_TERM})

## search by search term
r = api.request('search/tweets', {'q': SEARCH_TERM, 'count':100})

for item in r:
  if 'text' in item:
    #print(json.dumps(item))
    print(json.dumps(item).encode('utf8')) #replace above line with this for windows

