#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser, os, time
import twitter

config = ConfigParser.ConfigParser()
config.read('default.cfg');

logdir = os.path.abspath(config.get('path', 'log'))

logs = dict()

api = twitter.Api(consumer_key = config.get('oauth', 'consumer_key'),
                  consumer_secret = config.get('oauth', 'consumer_secret'),
                  access_token_key = config.get('oauth', 'access_token_key'),
                  access_token_secret = config.get('oauth', 'access_token_secret'))

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
    logfile = os.path.join(logdir, '%s.log' % user.screen_name)

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    with open(logfile, "a") as log:
        for dm in sorted(l, key=lambda dm: dm.created_at):
            log.write(("[%s](%s) %s\r\n" % (time.strftime("%Y-%m-%d %H:%M", time.localtime(dm.created_at_in_seconds)),
                                            dm.sender_screen_name,
                                            dm.text)).encode('utf-8'))
            api.DestroyDirectMessage(dm.id)
