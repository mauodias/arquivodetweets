#!/usr/bin/env python3
import sys

import tweepy
import requests
import json
import archiveis

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

def archive(url):
    archived = {}
    endpoint = 'https://pragma.archivelab.org/'
    data = {'url': url}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(endpoint, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        wayback_url = json.loads(response.text)['wayback_id']
        archived['wayback'] = f'https://web.archive.org{wayback_url}'
    archived['archiveis'] = archiveis.capture(url)
    return archived

class Listener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)

        tweet_id = tweet.get('id_str')
        tweet_user = tweet.get('screen_name')
        tweet_id_to_archive = tweet.get('in_reply_to_status_id_str')
        tweet_user_to_archive = tweet.get('in_reply_to_screen_name')

        tweet_url = f'https://twitter.com/{tweet_user_to_archive}/status/{tweet_id_to_archive}'
        urls = archive(tweet_url)

        message = 'Links: \n- {urls["archiveis"]}\n- {urls["wayback"]}'
        print(message)

def run(auth_info):
    listener = Listener()
    auth = OAuthHandler(auth_info['consumer_key'], auth_info['consumer_secret'])
    auth.set_access_token(auth_info['access_token'], auth_info['access_token_secret'])

    stream = Stream(auth, listener)
    stream.filter(track=['@arquivodetweets'])

if __name__ == '__main__':
    run(read_auth_info())
