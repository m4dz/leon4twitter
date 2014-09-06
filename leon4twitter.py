#!/usr/bin/env python
import ConfigParser
import twitter

config = ConfigParser.ConfigParser()
config.read('credentials.cfg');

api = twitter.Api(consumer_key = config.get('oauth', 'consumer_key'),
                  consumer_secret = config.get('oauth', 'consumer_secret'),
                  access_token_key = config.get('oauth', 'access_token_key'),
                  access_token_secret = config.get('oauth', 'access_token_secret'))

print api.VerifyCredentials()
