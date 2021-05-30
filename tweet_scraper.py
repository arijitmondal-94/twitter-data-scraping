"""This is a simple script to fetch tweets unsing Twitter API based on hashtag_phrase
The hashtags can be added in the .env file including fields for API keys. This script
writes all the data fetched in .csv file. 

Writes:
    .csv: Fteched tweets are written in this file.
"""
import tweepy
import os
import csv
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()
class Twitter:

    def __init__(self, scarpe_size):
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")
        self.access_token = os.environ.get("ACCESS_TOKEN")
        self.access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        self.hashtag_phrase = os.environ.get("HASHTAG_PHRASE")
        self.fname = os.environ.get("FILE_NAME")
        self.scrape_size = scarpe_size
        self.header = [
            'id', 'timestamp', 'tweet_text', 'username', 'location',
            'coordinates', 'place_json', 'all_hashtags', 'followers_count'
        ]

    def authentication(self) -> tweepy.API:
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        return api

    def get_dataframe(self) -> pd.DataFrame:

        if os.path.isfile(self.fname):
            print('File exist')
        else:
            with open(self.fname, 'a+') as file:
                w = csv.writer(file)
                w.writerow(self.header)
                print('File created')

        df = pd.read_csv('energy_tweets.csv', header=0)

        return df

    def get_tweets(self):

        api = self.authentication()
        tweepy_data = tweepy.Cursor(api.search, q=self.hashtag_phrase + " -filter:retweets", lang="en",
                                    tweet_mode='extended').items(self.scrape_size)
        df = self.get_dataframe()
        for tweet in tweepy_data:
            row = [
                tweet.id,
                tweet.created_at,
                tweet.full_text.replace('\n', ' ').encode('utf-8'),
                tweet.user.screen_name.encode('utf-8'),
                tweet.user.location,
                tweet.coordinates,
                tweet.place,
                [e['text'] for e in tweet._json['entities']['hashtags']],
                tweet.user.followers_count
            ]
            print(row[0], row[1])
            if row[0] in df['id'].values:
                continue
            else:
                df2 = pd.DataFrame(data=[row], columns=self.header)
                df = df.append(df2, ignore_index=True)
        df.sort_values(by=['id'])
        df.to_csv('energy_tweets.csv', index=False)


def main():
    # wakes up every minute collects latest 30 tweets
    obj = Twitter(30) # Number of new tweets to fetch
    for _ in range(1441):
        obj.get_tweets()
        time.sleep(60)


if __name__ == '__main__':
    main()