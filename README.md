# The WojBot Repository

This repository holds various utility scripts I use every now and then to consume NBA basketball. As of right now there are two scripts

* [Woj Bot For Slack](#woj-bot)
* [Team Schedule To Google Calendar](#team-schedule-to-google-calendar)

## Setup

The two main executables are within /src (where / is `/path/to/top/level` for this repo). 
This project runs on python3.7+ (I may have stray `breakpoint()`s in my code), so you will need that as well as pipenv for your distribution.
After installing those two tools, you need to configure your pipenv environment
```shell script
cd /path/to/top/level
pipenv install
```

Once that's done, you should be able to run your scripts! 
As a quick test, you should be able to generate the help message for the `parse_players.py` script

```shell script
pipenv run python src/parse_players.py -h
usage: parse_players.py [-h] [--store STORE]

Pull NBA players list from Wikipedia page

optional arguments:
  -h, --help     show this help message and exit
  --store STORE  Where to store new whitelist file
```

### Woj Bot For Slack

A simple bot to post tweets from a timeline to a slack group. 
It requires some tokens from twitter and slack bot api key. 
An example of these tokens is provided in `secret/secret.example.txt`.

Usage:
```shell script
cd /path/to/top/level
pipenv run python src/twitter_bot_woj.py latenightakshay --destination-channel "@akshay" --max-tweets-per-user 1
```
In the case above, I'm pushing the last tweet I tweeted to myself to my personal channel on Slack. 
It's useful to do the testing on yourself or a private channel to not bother others. 
Otherwise, the tool just spams you and there's no rate limiting.

To deploy, I just run a cron job once a minute during trade deadline season to stay up to date on my NBA breaking news.
I set that up using my deploy scripts, which are probably not useful to you. They're just helpers for me to push to my droplet

### Team Schedule To Google Calendar

A script to upload your team's schedule to your personal google calendar. 
You'll need an OAuth client id and client secret to bundle into a credentials.json file. 

I got mine from [this google calendar api quickstart page](https://developers.google.com/calendar/quickstart/python).
It makes a gcloud project for you and gives you a nice and easy way to download the file. 
The first time you run the script you have to fulfill the authentication flow, but after that you should be good.
I dump the credentials.json in the top level of this project and .gitignore the file as well as the pickled cred object for easy reuse.
Then, to run the script from the repo top level, I just

```shell script
cd /path/to/top/level
pipenv run python src/schedule.py --calendar-name "Philadelphia 76ers"
```

I'm probably gonna run this once a year, but whatever


# Questions

Feel free to open up an issue if you have any questions!
