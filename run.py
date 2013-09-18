#!/usr/bin/python3
from twitter import *
import requests,os
#
# Config these lines.
#

# Stausnet(Gnusocial) user/password here:
S_user = 'rayeshman'
S_pass = 'h2010nh2010n1'

# Twitter user name
T_user = 'rayeshman'

def send_to_statusnet(S_msg):
    params = {'status' : S_msg.encode('utf-8')}
    request = requests.post('http://quitter.se/api/statuses/update.json',auth=(S_user, S_pass),data = params)
    request_json = request.json()
# Example of request_json :
# {'in_reply_to_user_id': None, 'created_at': 'Sun Sep 15 09:53:35 +0200 2013', 'in_reply_to_status_id': None, 'geo': None, 'user': {'protected': False, 'time_zone': 'Iran', 'following': True, 'profile_image_url_profile_size': 'http://quitter.se/avatar/114829-96-20130726162743.png', 'screen_name': 'rayeshman', 'followers_count': 18, 'location': 'Iran', 'statusnet_blocking': False, 'url': None, 'name': 'Hossein Rayeshman', 'created_at': 'Thu Jul 18 20:30:26 +0200 2013', 'statusnet_profile_url': 'http://quitter.se/rayeshman', 'id': 114829, 'utc_offset': '16200', 'friends_count': 23, 'notifications': True, 'profile_image_url_original': 'http://quitter.se/avatar/114829-480-20130726162742.png', 'description': None, 'groups_count': 6, 'favourites_count': 10, 'profile_image_url': 'http://quitter.se/avatar/114829-48-20130726162743.png', 'statuses_count': 302}, 'text': 'Another test!', 'in_reply_to_screen_name': None, 'truncated': False, 'repeated': False, 'favorited': False, 'source': 'api', 'uri': 'http://quitter.se/notice/2142154', 'statusnet_conversation_id': 1916333, 'statusnet_html': 'Another test!', 'id': 2142154}

def read_from_twitter():
    consumer_key = 'Woy1uni80jmsrmlXZ81ZOw'
    consumer_secret = 'MQcRt1Nl80MVtgrWbv25pWunYcurnNdXwgOTuiZe91A'
    my_twitter_creds = os.path.expanduser('~/.T2Statusnetauth')
    if not os.path.exists(my_twitter_creds):
        oauth_dance("T2Statusnet", consumer_key, consumer_secret,my_twitter_creds)

    oauth_token, oauth_secret = read_token_file(my_twitter_creds)
    twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret))
    twits = twitter.statuses.user_timeline(id=T_user,count = 1)
#example of twitter.statuses.user_timeline(id=T_user,count = 1)
#[{'id_str': '379151029298036736', 'lang': 'en', 'in_reply_to_screen_name': None, 'retweet_count': 0, 'truncated': False, 'contributors': None, 'in_reply_to_status_id': None, 'favorited': False, 'place': None, 'created_at': 'Sun Sep 15 07:53:44 +0000 2013', 'coordinates': None, 'user': {'utc_offset': None, 'time_zone': None, 'id_str': '1004621052', 'url': None, 'profile_use_background_image': True, 'lang': 'en', 'friends_count': 77, 'location': 'Iran', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_image_url': 'http://a0.twimg.com/profile_images/3125454858/557400e39051ec941f5f38f22e4e4e64_normal.png', 'contributors_enabled': False, 'default_profile': True, 'following': False, 'favourites_count': 30, 'listed_count': 2, 'profile_text_color': '333333', 'follow_request_sent': False, 'geo_enabled': False, 'is_translator': False, 'created_at': 'Tue Dec 11 18:42:32 +0000 2012', 'profile_background_color': 'C0DEED', 'name': 'Hossein Rayeshman', 'profile_image_url_https': 'https://si0.twimg.com/profile_images/3125454858/557400e39051ec941f5f38f22e4e4e64_normal.png', 'protected': False, 'id': 1004621052, 'notifications': False, 'profile_link_color': '0084B4', 'default_profile_image': False, 'entities': {'description': {'urls': []}}, 'verified': False, 'followers_count': 27, 'screen_name': 'rayeshman', 'statuses_count': 223, 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'description': '', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_background_tile': False, 'profile_sidebar_border_color': 'C0DEED'}, 'in_reply_to_user_id': None, 'id': 379151029298036736, 'in_reply_to_status_id_str': None, 'entities': {'hashtags': [], 'urls': [], 'user_mentions': [], 'symbols': []}, 'retweeted': False, 'favorite_count': 0, 'geo': None, 'source': '<a href="http://quitter.se" rel="nofollow">quitter.se</a>', 'text': 'Another test!', 'in_reply_to_user_id_str': None}]
    savefile = os.path.expanduser('~/.T2Statusnetsavefile')
    if not os.path.exists(savefile):
        file = open(savefile , 'w')
        file.write(twits[0]['id_str'])
        file.close()
    else:
        file = open(savefile , 'r')
        last_tweet = file.read()
        file.close()
        print('Last tweet:',last_tweet)
        print('type of last_tweet:',type(last_tweet))
        twits = twitter.statuses.user_timeline(id=T_user,count = 20)
        for i in twits:
            if i['id_str'] == last_tweet :
                last_tweet_id = twits.index(i)
                print("last tweet index:",last_tweet_id)
                check_twitter()

def check_twitter():
    if last_tweet_id != 0 :
        for i in range(last_tweet_id):
            print(twits[i]['text'])
            send_to_statusnet(twits[i]['text'])
        file = open(savefile , 'w')
        file.write(twits[0]['id_str'])
        file.close()
    else:
        print(False)
    file = open(savefile , 'w')
    file.write(twits[0]['id_str'])
    file.close()

read_from_twitter()
