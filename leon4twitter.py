#!/usr/bin/env python
import ConfigParser
import twitter

config = ConfigParser.ConfigParser()
config.read('credentials.cfg');

api = twitter.Api(consumer_key = config.get('oauth', 'consumer_key'),
                  consumer_secret = config.get('oauth', 'consumer_secret'),
                  access_token_key = config.get('oauth', 'access_token_key'),
                  access_token_secret = config.get('oauth', 'access_token_secret'))

logs = dict()

for dm in api.GetDirectMessages():
    if not dm.sender_id in logs:
        logs[dm.sender_id] = list()
    logs[dm.sender_id].append(dm)

for dm in api.GetSentDirectMessages():
    if not dm.recipient_id in logs:
        logs[dm.recipient_id] = list()
    logs[dm.recipient_id].append(dm)

for id, l in logs.iteritems():
    user = api.GetUser(id)
    print user.screen_name
    for dm in sorted(l, key=lambda dm: dm.created_at):
        print "(%s) %s" % (dm.sender_screen_name, dm.text)
