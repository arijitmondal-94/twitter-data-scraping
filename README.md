# Twitter Data Scraping

## Description

### This is a simple script to fetch tweets unsing Twitter API based on hashtag_phrase. The hashtags can be added in the .env file including fields for API keys. This script writes all the data fetched in .csv file. It does not query historical data.

## How do I run it?

1. Add twitter API keys and hashtags in the **.env** file

2. Install dependencies from requirments.txt

```shell
> python3 -m pip install -r requirements.txt 
```

3. then as simple as running the script

```shell
> python3 tweet_scraper.py 
```

4. To run it in detached shell [OPTIONAL]

```shell
> nohup python3 tweet_scaper.py &
```

