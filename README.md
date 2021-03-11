# Twitter Data Scraping

## Description

### This script is designed to read tweets filterted by hashtags and create a csv file. As of this implementation the tweet fields saved in csv file are

* tweet id

* timestamp for when it was created

* full text

* screen name

* location

* coordinates

* hashtags in the tweet

* user follow count

## How it works?

#### At first the script will try read a maximum of 30k tweets for the hastags. It goes as far back as twitter api allows to read. Then it will sleep for *SLEEP_TIME* in **.env** and read *ITEM_LIMIT* tweets when it wakes up. This will repeat for 1400 times unles it is explicitly set higher or lower

#### I wrote this script to delpoy it on a free-tier ec2 and keep it running until I am satisified with the number of tweets collected

## How do I run it?

### To run the script

1. replace your authenitcation details in the **.env** file and the hashtags that interests you

2. install dependencies from requirments.txt

```shell
python3 -m pip install -r requirements.txt 
```

3. then as simple as running the script

```shell
python3 tweet_scaper.py 
```

### if you are deploying it on a remote machine and execution stops when ssh is disconnected, use this

```shell
nohup python3 tweet_scaper.py &
```
