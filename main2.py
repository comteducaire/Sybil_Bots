import tweepy

consumer_key = 'QhyOPxxxvJaOdp248cEBmFULw'
consumer_secret ='nNgrjrBFnnozI7urzHeO3DduRy0mEHqBq1ASzNYuUe93l36SxL'
access_token = '102995859-ttxAcxp6nAXpSiTTVVb7zX7sk9ijVqsmYKAYKgyR'
access_token_secret = 'xHv7Vp7PJAb1u51D1eQxZS6syoicPfSg5ygYCV0SdCNuS'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
