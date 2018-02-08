#!/usr/bin/env bash

cd ..
tar -zcf slackbot.tar.gz --exclude="*.git" slackbot
gcloud compute scp slackbot.tar.gz centos:~
rm slackbot.tar.gz
