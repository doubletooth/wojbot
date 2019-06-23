#!/usr/bin/env bash

cd ..

echo "[local] Compressing project..."
COPYFILE_DISABLE=true tar -zcf slackbot.tar.gz \
--exclude="*.git" \
--exclude=".idea*" \
--exclude="*__pycache__/*" \
--exclude=".DS_Store" slackbot

echo "[local] Deploying project..."

# probably dumb, but don't want file printed out during deploy
gcloud compute scp slackbot.tar.gz centos:~ >/dev/null
gcloud compute scp --quiet slackbot/deploy/deploy_gcloud.sh centos:~ >/dev/null

gcloud compute ssh --command="/home/akshay/deploy_gcloud.sh && rm /home/akshay/deploy_gcloud.sh" centos
rm slackbot.tar.gz
echo "[local] Complete"
