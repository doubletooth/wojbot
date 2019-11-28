import json
import os
import argparse

from twitter import Api
from slackclient import SlackClient

from secret import read_secret, manage_state


def should_post_tweet(whitelist, tweet_text, tweet_urls, only_state):
    """
    Determines whether it should post a tweet based on the tweet contents

    :param dict whitelist:
    :param str tweet_text:
    :param list tweet_urls:
    :param bool only_state:
    :rtype: bool
    """
    tweet_text = tweet_text.lower()

    if only_state:
        return False

    for url in tweet_urls:
        for blocked_url in whitelist['blacklisted_urls']:
            if blocked_url in url.expanded_url:
                return False

    if any(phrase in tweet_text for phrase in whitelist['whitelisted_phrases']):
        return True

    if any(player in tweet_text for player in whitelist['players']):
        return True

    if any(coach in tweet_text for coach in whitelist['coaches']):
        return True

    if any(team in tweet_text for team in whitelist['teams']):
        return True

    return False


def post_new_user_tweet(screen_name, slack_channel, max_tweets_allowed, twitter_client, slack_client, only_state):
    """
    Posts a tweet from screen name in the given slack channel, up to the max tweets allowed
    Posts tweets reverse chronologically

    :param str screen_name:
    :param str slack_channel:
    :param int max_tweets_allowed:
    :param twitter.api.Api twitter_client: twitter client instance
    :param slackclient.client.SlackClient slack_client: slack client instance
    :param bool only_state: only update the state file
    :rtype: NoneType
    """
    with open(os.path.join(os.path.dirname(__file__), '..', 'state', 'whitelist.json'), 'r') as f:
        whitelist = json.load(f)

    with manage_state() as state:
        new_tweet_found = False
        state_key = 'last_tweet_{}'.format(screen_name)

        timeline = twitter_client.GetUserTimeline(
            screen_name=screen_name,
            since_id=state.get(state_key),
            exclude_replies=True,
        )[:max_tweets_allowed]  # only get the latest tweets back to max tweets allowed

        for status in timeline:
            if not state.get(state_key) or not new_tweet_found:
                state[state_key] = status.id
                new_tweet_found = True

            if should_post_tweet(whitelist, status.text, status.urls, only_state):
                slack_client.api_call(
                    'chat.postMessage',
                    channel=slack_channel,
                    text=os.path.join('https://twitter.com/{}/status'.format(screen_name), str(status.id)),
                    as_user=True,
                )


def main():
    parser = argparse.ArgumentParser(
        description='Post tweets from a particular twitter user to a Weekend Productions LLC Slack Channel'
    )
    parser.add_argument('twitter_user', nargs='+', help='Twitter whose tweets are being relayed')
    parser.add_argument('--max-tweets-per-user', type=int, default=10,
                        help='Max tweets to post per program invocation')
    parser.add_argument('--destination-channel', default='#nba',
                        help='Slack channel or user DM to post to. Channels start with #, users with @')
    parser.add_argument('--only-state', action='store_true',
                        help='Only update the state file, not update the slack channel')

    args = parser.parse_args()

    twitter_client = Api(
        consumer_key=read_secret('CONSUMER_KEY'),
        consumer_secret=read_secret('CONSUMER_SECRET'),
        access_token_key=read_secret('ACCESS_TOKEN_KEY'),
        access_token_secret=read_secret('ACCESS_TOKEN_SECRET'),
    )
    slack_client = SlackClient(read_secret('SLACK_BOT_API'))

    for user in args.twitter_user:
        post_new_user_tweet(
            user,
            args.destination_channel,
            args.max_tweets_per_user,
            twitter_client,
            slack_client,
            args.only_state,
        )


if __name__ == '__main__':
    main()
