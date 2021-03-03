'''
This script collects tweets
'''

import os
import tweepy
import csv
import logging
import time

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    filename='twitter_scraping.log', 
    level=logging.INFO,
    filemode='a', 
    format= '%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ScrapeScrape():

    def __init__(self, scarpe_size: int):
        """[summary]
        """    
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")
        self.access_token = os.environ.get("ACCESS_TOKEN")
        self.access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        self.hashtag_phrase = os.environ.get("HASHTAG_PHRASE")
        self.fname = os.environ.get("FILE_NAME")
        self.scrape_size = scarpe_size

    def scrape_tweets(self):
        """[summary]
        """    
        header = ['id', 'timestamp', 'tweet_text', 'username', 'location', 'coordinates', 'place_json', 'all_hashtags', 'followers_count']
        #create authentication for accessing Twitter
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        #initialize Tweepy API
        api = tweepy.API(auth, wait_on_rate_limit=True)
        #get the name of the spreadsheet we will write to
        tweepy_data = tweepy.Cursor(api.search, q=self.hashtag_phrase+' -filter:retweets', lang="en", tweet_mode='extended').items(self.scrape_size)
        for tweet in reversed(list(tweepy_data)):
            row = [
                tweet.id, 
                tweet.created_at, 
                tweet.full_text.replace('\n',' ').encode('utf-8'),
                tweet.user.screen_name.encode('utf-8'),
                tweet.user.location,
                tweet.coordinates,
                tweet.place,
                [e['text'] for e in tweet._json['entities']['hashtags']],
                tweet.user.followers_count
                ]
            try:
                with open(self.fname, 'r') as file:
                    last_id = file.read().splitlines()[-1][0:19]
                with open(self.fname, 'a+') as file:
                    if int(row[0]) <= int(last_id):
                        continue
                    else:
                        w = csv.writer(file)
                        w.writerow(row)
                        logging.info('New tweet added')
            except IOError:
                with open(self.fname, 'w+') as file:
                    w = csv.writer(file)
                    w.writerow(header)
                    w.writerow(row)
                    logging.info('New tweet added')
            except Exception as e:
                logging.error(e)
                print(e)
                exit()
    

def main():
    # Pyhton normaly goes back a few hours from data request.
    # So I think it is a good idea to do a big scrape at first the do small scrapes
    # configuration can 30k items at first go and then 3 every two minutes (at least for the hashtags we are using)
    logging.info('Execution Started: %s', datetime.today())

    big_scraper = ScrapeScrape(30000)
    big_scraper.scrape_tweets()

    for _ in range(0, 1440):
        START = time.time()
        logging.info('Scraping Started: %s', datetime.today())
        scraper = ScrapeScrape(int(os.getenv('ITEM_LIMIT')))
        scraper.scrape_tweets()
        logging.info('Scraping Ended: %s', datetime.today())
        logging.info('Execution time: %s', (time.time()-START))
        time.sleep(int(os.getenv('SLEEP_TIME')))
        logging.info('Woke up to check new tweets')


if __name__ == '__main__':
    

    main()
    logging.critical('Execution Terminated')