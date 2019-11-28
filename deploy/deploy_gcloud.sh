#!/usr/bin/env bash

cd /home/akshay || echo "Unable to navigate to /home/akshay" && exit 1

echo "[gcloud] Extracting project..."
tar -zxf slackbot.tar.gz

echo "[gcloud] Loading crontab..."

FOLLOW_LIST=$(xargs < /home/akshay/slackbot/state/follow_list.txt)
echo "* * * * * python3.6 /home/akshay/slackbot/src/twitter_bot_woj.py ${FOLLOW_LIST}" > tmp_ctab
crontab tmp_ctab

echo "[gcloud] Cleaning up files..."
rm tmp_ctab
rm slackbot.tar.gz
