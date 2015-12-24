#!/usr/bin/python3
import os
import json
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
        #conf = open('T2Statusnet.conf','r')
        #conf = conf.read()
        #conf = conf.split()

        # Prints T2Statusnet.conf values
        print('#### Config: ####')
        print('T Account :',config['twitter_account'])
        #print('Friend? :',conf[conf.index('Friend')+1])
        #print('UR T User :',conf[conf.index('T_user')+1])
        #print('S User :',conf[conf.index('S_user')+1])
        print('#################')
        # Sets T2Statusnet.conf values
        #T_acc = config['twitter_account']
        #Friend = conf[conf.index('Friend')+1]
        #T_user = conf[conf.index('T_user')+1]
        #S_user = conf[conf.index('S_user')+1]
        #S_pass = conf[conf.index('S_pass')+1]
        # will ask Oauth permission on the first run
        if not os.path.exists(self.my_twitter_creds):
            oauth_dance("T2Statusnet", self.consumer_key, self.consumer_secret,self.my_twitter_creds)

        self.oauth_token, self.oauth_secret = read_token_file(self.my_twitter_creds)
        self.savefile = os.path.expanduser('~/.T2Statusnetsavefile')

    def send_to_statusnet(self, message, gnusocial, password):
        # Send S_msg to statusnet

        #Download Medias

        #Change URLs

        #twurl -H upload.twitter.com -X POST "/1.1/media/upload.json" --file "/path/to/media.jpg" --file-field "media"

        # , 'media_ids'
        params = {'status' : message['text'].encode('utf-8')}
        #return
        request = requests.post('http://mix.eibriel.com/api/statuses/update.json',auth=(gnusocial, password),data = params)
        request_json = request.json()
        # Example of request_json :
        # {'in_reply_to_user_id': None, 'created_at': 'Sun Sep 15 09:53:35 +0200 2013', 'in_reply_to_status_id': None, 'geo': None, 'user': {'protected': False, 'time_zone': 'Iran', 'following': True, 'profile_image_url_profile_size': 'http://quitter.se/avatar/114829-96-20130726162743.png', 'screen_name': 'rayeshman', 'followers_count': 18, 'location': 'Iran', 'statusnet_blocking': False, 'url': None, 'name': 'Hossein Rayeshman', 'created_at': 'Thu Jul 18 20:30:26 +0200 2013', 'statusnet_profile_url': 'http://quitter.se/rayeshman', 'id': 114829, 'utc_offset': '16200', 'friends_count': 23, 'notifications': True, 'profile_image_url_original': 'http://quitter.se/avatar/114829-480-20130726162742.png', 'description': None, 'groups_count': 6, 'favourites_count': 10, 'profile_image_url': 'http://quitter.se/avatar/114829-48-20130726162743.png', 'statuses_count': 302}, 'text': 'Another test!', 'in_reply_to_screen_name': None, 'truncated': False, 'repeated': False, 'favorited': False, 'source': 'api', 'uri': 'http://quitter.se/notice/2142154', 'statusnet_conversation_id': 1916333, 'statusnet_html': 'Another test!', 'id': 2142154}

    def read_from_twitter(self, twitter_user, gnusocial, password):
        twitter = Twitter(auth=OAuth(self.oauth_token, self.oauth_secret, self.consumer_key, self.consumer_secret))
        #example of twitter.statuses.user_timeline(id=T_user,count = 1)
        #[{'id_str': '379151029298036736', 'lang': 'en', 'in_reply_to_screen_name': None, 'retweet_count': 0, 'truncated': False, 'contributors': None, 'in_reply_to_status_id': None, 'favorited': False, 'place': None, 'created_at': 'Sun Sep 15 07:53:44 +0000 2013', 'coordinates': None, 'user': {'utc_offset': None, 'time_zone': None, 'id_str': '1004621052', 'url': None, 'profile_use_background_image': True, 'lang': 'en', 'friends_count': 77, 'location': 'Iran', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_image_url': 'http://a0.twimg.com/profile_images/3125454858/557400e39051ec941f5f38f22e4e4e64_normal.png', 'contributors_enabled': False, 'default_profile': True, 'following': False, 'favourites_count': 30, 'listed_count': 2, 'profile_text_color': '333333', 'follow_request_sent': False, 'geo_enabled': False, 'is_translator': False, 'created_at': 'Tue Dec 11 18:42:32 +0000 2012', 'profile_background_color': 'C0DEED', 'name': 'Hossein Rayeshman', 'profile_image_url_https': 'https://si0.twimg.com/profile_images/3125454858/557400e39051ec941f5f38f22e4e4e64_normal.png', 'protected': False, 'id': 1004621052, 'notifications': False, 'profile_link_color': '0084B4', 'default_profile_image': False, 'entities': {'description': {'urls': []}}, 'verified': False, 'followers_count': 27, 'screen_name': 'rayeshman', 'statuses_count': 223, 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'description': '', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_background_tile': False, 'profile_sidebar_border_color': 'C0DEED'}, 'in_reply_to_user_id': None, 'id': 379151029298036736, 'in_reply_to_status_id_str': None, 'entities': {'hashtags': [], 'urls': [], 'user_mentions': [], 'symbols': []}, 'retweeted': False, 'favorite_count': 0, 'geo': None, 'source': '<a href="http://quitter.se" rel="nofollow">quitter.se</a>', 'text': 'Another test!', 'in_reply_to_user_id_str': None}]

        if not os.path.exists(self.savefile):
            twitter_data = {}
        else:
            with open(self.savefile) as data_file:
                twitter_data = json.load(data_file)

        if not twitter_user in twitter_data:
            # Writes last Id_str on savefile on first run
            try:
                twits = twitter.statuses.user_timeline(id=twitter_user,count = 1)
            except TwitterHTTPError:
                print ("Twitter error")
                return
            #twitter_data = {}
            twitter_data[ twitter_user ] = {'last_tweet': twits[0]['id_str']}

            with open(self.savefile, 'w') as data_file:
                json.dump(twitter_data, data_file)
            #file = open(self.savefile , 'w')
            #file.write(twits[0]['id_str'])
            #file.close()
            print('No New tweet to send to statusnet!(maybe this is your first run of this app you can send a tweet and then run this script again!)')
        else:
            #file = open(self.savefile , 'r')
            #last_tweet = file.read()
            #file.close()
            with open(self.savefile) as data_file:
                twitter_data = json.load(data_file)

            # Read last Id_str
            try:
                twits = twitter.statuses.user_timeline(id=twitter_user, since_id=twitter_data[twitter_user]['last_tweet'], count = 30)
            except TwitterHTTPError:
                print ("Twitter error")
                return
            except ValueError:
                print ("Value error")
                return

            #last_tweet_id = None
            #for i in twits:
            #    if i['id_str'] == twitter_data[twitter_user]['last_tweet'] : # last_tweet and i['id_str'] are strings.
            #        last_tweet_id = twits.index(i)

            if len(twits) > 0:
                for twit in reversed(twits):
                    print(twit['text'])
                    #print(twits[i])
                    self.send_to_statusnet(twit, gnusocial, password)
                #return
                twitter_data[twitter_user]['last_tweet'] = twits[0]['id_str']
                with open(self.savefile, 'w') as data_file:
                    json.dump(twitter_data, data_file)
                #file = open(self.savefile , 'w')
                #file.write(twits[0]['id_str'])
                #file.close()
            else:
                print('Nothing to send to statusnet!')


t2g = t2statusnet()

t2g.setting()
for account in config['accounts']:
    t2g.read_from_twitter(account['twitter'], account['gnusocial'], account['password'])
