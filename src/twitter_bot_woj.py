import os

from twitter import Api
from slackclient import SlackClient

from secret import read_secret, manage_state

client = Api(
    consumer_key=read_secret('CONSUMER_KEY'),
    consumer_secret=read_secret('CONSUMER_SECRET'),
    access_token_key=read_secret('ACCESS_TOKEN_KEY'),
    access_token_secret=read_secret('ACCESS_TOKEN_SECRET'),
)
sc = SlackClient(read_secret('SLACK_BOT_API'))


def post_new_user_tweet(screen_name, slack_channel='#nba'):
    with manage_state() as state:
        new_tweet_found = False
        state_key = 'last_tweet_{}'.format(screen_name)

        timeline = client.GetUserTimeline(screen_name=screen_name, since_id=state.get(state_key))
        for status in timeline:
            if not state.get(state_key) or not new_tweet_found:
                state[state_key] = status.id
                new_tweet_found = True

            sc.api_call(
                'chat.postMessage',
                channel=slack_channel,
                text=os.path.join('https://twitter.com/{}/status'.format(screen_name), str(status.id)),
                as_user=True,
            )


post_new_user_tweet('_jakemiller', '@akshay')
