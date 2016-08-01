#!/usr/bin/python3
import os
import json
import time
import random
import requests

from twitter import *
from config import config

class t2statusnet:
    def setting(self):
        #Set values of some variable.
        #global consumer_key ,consumer_secret ,my_twitter_creds ,T_acc ,Friend ,T_user ,S_user ,S_pass ,oauth_token ,oauth_token ,savefile
        self.consumer_key = 'Woy1uni80jmsrmlXZ81ZOw'
        self.consumer_secret = 'MQcRt1Nl80MVtgrWbv25pWunYcurnNdXwgOTuiZe91A'
        self.my_twitter_creds = os.path.expanduser('~/.T2Statusnetauth')

        # Prints config.py values
        print('#### Config: ####')
        print('T Account :',config['twitter_account'])
        print('#################')
        # will ask Oauth permission on the first run
        if not os.path.exists(self.my_twitter_creds):
            oauth_dance("T2Statusnet", self.consumer_key, self.consumer_secret,self.my_twitter_creds)

        self.oauth_token, self.oauth_secret = read_token_file(self.my_twitter_creds)
        self.savefile = os.path.expanduser('~/.T2Statusnetsavefile')
        self.ratelimits = os.path.expanduser('~/.T2Statusnetratelimits')

    def send_to_statusnet(self, message, gnusocial, password):
        # Send S_msg to statusnet

        #Download Medias

        #Change URLs

        #twurl -H upload.twitter.com -X POST "/1.1/media/upload.json" --file "/path/to/media.jpg" --file-field "media"

        # , 'media_ids'
        text = ''
        if 'retweeted_status' in message:
           print(message['retweeted_status']['user'])
           text = '♻ @{0}: {1}'.format(message['retweeted_status']['user']['screen_name'], message['retweeted_status']['text'])
        else:
            text = message['text']
        params = {'status' : text.encode('utf-8')}
        #return
        request = requests.post('http://mix.eibriel.com/api/statuses/update.json',auth=(gnusocial, password),data = params)
        request_json = request.json()
        if request.status_code != 200:
            print (request.text)
            return False
        return True

    def read_from_twitter(self, twitter_user, gnusocial, password):
        remaining = None
        reset = None
        twitter = Twitter(auth=OAuth(self.oauth_token, self.oauth_secret, self.consumer_key, self.consumer_secret))

        if not os.path.exists(self.ratelimits):
            ratelimits_data = {'reset': 0, 'remaining': 0}
        else:
            with open(self.ratelimits) as data_file:
                ratelimits_data = json.load(data_file)

        #print (ratelimits_data)
        time_margin = 60
        time_diff = ratelimits_data['reset'] - int(time.time()) + time_margin
        #print (time_diff)
        if time_diff > 0:
            print('Waiting {0} seconds for rate limit to reset'.format(time_diff))
            return

        if not os.path.exists(self.savefile):
            twitter_data = {}
        else:
            with open(self.savefile) as data_file:
                twitter_data = json.load(data_file)

        if not twitter_user in twitter_data:
            # Writes last Id_str on savefile on first run
            try:
                twits = twitter.statuses.user_timeline(id=twitter_user,count = 1)
                remaining = int(twits.headers.get('x-rate-limit-remaining'))
                reset = int(twits.headers.get('x-rate-limit-reset'))
            except TwitterHTTPError as error:
                #print (error)
                if error.response_data['errors'][0]['code']:
                    print ("Limit Exceeded")
                else:
                    print ("Twitter error")
                return
            except ValueError:
                print ("Value error")
                return
            twitter_data[ twitter_user ] = {'last_tweet': twits[0]['id_str']}

            with open(self.savefile, 'w') as data_file:
                json.dump(twitter_data, data_file)
            print('No New tweet to send to statusnet!(This is your first run of this app)')
        else:
            with open(self.savefile) as data_file:
                twitter_data = json.load(data_file)

            # Read last Id_str
            try:
                twits = twitter.statuses.user_timeline(id=twitter_user, since_id=twitter_data[twitter_user]['last_tweet'], count = 30, trim_user = False, exclude_replies = True)
                remaining = int(twits.headers.get('x-rate-limit-remaining'))
                reset = int(twits.headers.get('x-rate-limit-reset'))
                #print (dir(twits))
                #print (twits)
            except TwitterHTTPError as error:
                #print (dir(error.response_data))
                if error.response_data['errors'][0]['code']:
                    print ("Limit Exceeded")
                else:
                    print ("Twitter error")
                #raise
                return
            except ValueError:
                print ("Value error")
                return

            if len(twits) > 0:
                for twit in reversed(twits):
                    print(twit['text'])
                    send_stat = self.send_to_statusnet(twit, gnusocial, password)
                if send_stat:
                    twitter_data[twitter_user]['last_tweet'] = twits[0]['id_str']
                    with open(self.savefile, 'w') as data_file:
                         json.dump(twitter_data, data_file)
            else:
                print('Nothing to send to statusnet!')

        if remaining == 0:
            with open(self.ratelimits, 'w') as data_file:
                json.dump({'time': int(time.time()), 'reset': reset}, data_file)


t2g = t2statusnet()

t2g.setting()
random.shuffle(config['accounts'])
for account in config['accounts']:
    print (account['twitter'])
    t2g.read_from_twitter(account['twitter'], account['gnusocial'], account['password'])
