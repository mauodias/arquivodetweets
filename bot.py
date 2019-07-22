#!/usr/bin/env python3
import os
import sys
import time

import json

from tools import ScreenCapture as SC, Uploader, Archiver

import tweepy

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class Listener(StreamListener):

    def __init__(self, archiver, uploader, screencapturer, auth):
        self.archiver = archiver
        self.uploader = uploader
        self.screencapturer = screencapturer
        self.auth = auth
        self.api = tweepy.API(auth)

    def on_data(self, data):
        print('Someone is calling!')
        tweet = json.loads(data)

        tweet_id = tweet.get('id_str')
        tweet_user = tweet.get('screen_name')
        tweet_id_to_archive = tweet.get('in_reply_to_status_id_str')
        tweet_user_to_archive = tweet.get('in_reply_to_screen_name')
        print(f'Loaded tweet {tweet_id_to_archive} from user {tweet_user_to_archive}')

        tweet_url = f'https://twitter.com/{tweet_user_to_archive}/status/{tweet_id_to_archive}'
        wayback_url = self.archiver.archive_wayback(tweet_url)
        print(f'Created wayback URL: {wayback_url}')

        archiveis_url = self.archiver.archive_is(tweet_url)
        print(f'Created archive.is URL: {archiveis_url}')

        screenshot_url = self.uploader.upload(self.screencapturer.capture(tweet_url), base64=True)['url']
        print(f'Screenshot taken: {screenshot_url}')

        message = f'''Tweet arquivado!

Links:
  - {wayback_url}
  - {archiveis_url}

Screenshot: {screenshot_url}'''

        print(f'Message will be:\n\n{message}\n\nWill wait 5 seconds to avoid being detected as spam')
        time.sleep(5)
        print('Tweeting...')

        self.api.update_status(message, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
        print('Done! Sleeping for 30 seconds...')
        time.sleep(30)
        print('Awake!')

def run(auth_info):
    print('Let\'s get ready to rumbleeeeeeeee!')
    auth = OAuthHandler(auth_info['consumer_key'], auth_info['consumer_secret'])
    auth.set_access_token(auth_info['access_token'], auth_info['access_token_secret'])
    listener = Listener(Archiver(), Uploader(auth_info['imgur_client_id']), SC(), auth)

    stream = Stream(auth, listener)
    stream.filter(track=['@arquivodetweets'])

def read_auth_info():
    try:
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        imgur_client_id = os.environ['IMGUR_CLIENT_ID']
        env_vars = {'consumer_key': consumer_key, 'consumer_secret': consumer_secret,
                'access_token': access_token, 'access_token_secret': access_token_secret,
                'imgur_client_id': imgur_client_id}
        return env_vars
    except:
        print('''Environment variables not configured properly. Values expected:
- TWITTER_CONSUMER_KEY
- TWITTER_CONSUMER_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_TOKEN_SECRET
- IMGUR_CLIENT_ID''')
        sys.exit(1)

if __name__ == '__main__':
    try:
        run(read_auth_info())
    except KeyboardInterrupt:
        print('Good bye!')
        sys.exit(0)
