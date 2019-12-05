## Misc Scripts

This repository holds various utility scripts I use every now and then to consume NBA basketball. As of right now there are two scripts

* [Woj Bot For Slack](#woj-bot)
* [Team Schedule To Google Calendar](#team-schedule-to-google-calendar)

### Woj Bot For Slack

A simple bot to post tweets from a timeline to a slack group. 
It requires some tokens from twitter and slack bot api key. 
An example of these tokens is provided in secret/secret.example.txt.

The two main source files run under python3+ (tested on 3.6 and 3.7), and all requirements are in requirements.txt.
Run --help on either src/twitter_bot_woj.py or src/parse_players.py to determine how to run.

As a side note, you probably wanna try posting to private channels to not bother other people.

As another side note, the deploy scripts are probably not useful for you. 
They're just for me to deploy to my droplet easily.

### Team Schedule To Google Calendar

A script to upload your team's schedule to your personal google calendar. 
You'll need an OAuth client id and client secret to bundle into a credentials.json file. 

I got mine from [this google calendar api quickstart page](https://developers.google.com/calendar/quickstart/python).
It makes a gcloud project for you and gives you a nice and easy way to download the file. 
The first time you run the script you have to fulfill the authentication flow, but after that you should be good.
I dump the credentials.json in the top level of this project and .gitignore the file as well as the pickled cred object for easy reuse.
Then, to run the script from the repo top level, I just

```bash
cd /path/to/top/level
pipenv run python src/schedule.py --calendar-name "Philadelphia 76ers"
```

I'm probably gonna run this once a year, but whatever


## Questions

Feel free to open up an issue if you have any questions!
