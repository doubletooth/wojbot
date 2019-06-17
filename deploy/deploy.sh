#!/usr/bin/env bash

cd ..
tar -zcf slackbot.tar.gz --exclude="*.git" --exclude=".idea*" slackbot
gcloud compute scp slackbot.tar.gz centos:~
rm slackbot.tar.gz
