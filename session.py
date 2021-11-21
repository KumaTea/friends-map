import json
import base64
import tweepy


def read_file(filename, encrypt=False):
    if encrypt:
        with open(filename, 'rb') as f:
            return base64.b64decode(f.read()).decode('utf-8')
    else:
        with open(filename, 'r') as f:
            return f.read()


def query_token(token_id):
    return read_file(f'token_{token_id}', True)


twitter_token = json.loads(query_token('twitter'))
auth = tweepy.OAuthHandler(twitter_token['consumer_key'], twitter_token['consumer_secret'])
auth.set_access_token(twitter_token['access_token'], twitter_token['access_token_secret'])

try:  # v3
    kuma = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
except:
    kuma = tweepy.API(auth, wait_on_rate_limit=True)
