#!/usr/bin/env bash

cd /home/akshay


# TODO move out state file so script doesn't re-push same tweets multiple times

echo "[gcloud] Extracting project..."
tar -zxf slackbot.tar.gz

echo "[gcloud] Loading crontab..."
echo "* * * * * python3.6 /home/akshay/slackbot/src/twitter_bot_woj.py wojespn ZachLowe_NBA ShamsCharania" > tmp_ctab
crontab tmp_ctab

echo "[gcloud] Cleaning up files..."
rm tmp_ctab
rm slackbot.tar.gz
