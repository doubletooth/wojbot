#!/usr/bin/env bash

# Call this script from the slackbot root directory

UPDATE_LOCAL=

for i in "$@"
do
case ${i} in
    --update-local-state)
        UPDATE_LOCAL=1
        ;;
    *)
        ;;
esac
done

if [[ -n "$UPDATE_LOCAL" ]]; then
    # probably dumb, but don't want file printed out during deploy
    gcloud compute scp --quiet centos:~/slackbot/state/state.json state/state.json >/dev/null
fi


cd ..  # move out of the base level of the project to zip everything up

echo "[local]  Compressing project..."
COPYFILE_DISABLE=true tar -zcf slackbot.tar.gz \
--exclude="*.git" \
--exclude=".idea*" \
--exclude="*__pycache__/*" \
--exclude=".DS_Store" slackbot

echo "[local]  Deploying project..."

# probably dumb, but don't want file printed out during deploy
gcloud compute scp slackbot.tar.gz centos:~ >/dev/null
gcloud compute scp slackbot/deploy/deploy_gcloud.sh centos:~ >/dev/null

gcloud compute ssh --command="/home/akshay/deploy_gcloud.sh && rm /home/akshay/deploy_gcloud.sh" centos
rm slackbot.tar.gz
echo "[local]  Complete"
