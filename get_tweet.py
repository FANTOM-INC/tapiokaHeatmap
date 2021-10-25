import json
import pandas as pd
from requests_oauthlib import OAuth1Session
import time
from dotenv import load_dotenv
load_dotenv()

class Reshape_data:
    def __init__(self):
        
        self.tweet_col =['created_at', 'id', 'id_str', 'text', 'display_text_range', 'source',
                        'truncated', 'in_reply_to_status_id', 'in_reply_to_status_id_str',
                        'in_reply_to_user_id', 'in_reply_to_user_id_str',
                        'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place',
                        'contributors', 'is_quote_status', 'quote_count', 'reply_count',
                        'retweet_count', 'favorite_count', 'entities', 'extended_entities',
                        'favorited', 'retweeted', 'possibly_sensitive', 'filter_level', 'lang',
                        'matching_rules', 'extended_tweet', 'quoted_status_id',
                        'quoted_status_id_str', 'quoted_status', 'quoted_status_permalink'] 

    def create_DataFrame(self,tweet_datas):
        
        dict_array = []
        for i in range(len(tweet_datas)):
            tweet = self.flatten_dict(tweet_datas[i])
            dict_array.append(tweet)
        
        DataFrame = pd.DataFrame.from_dict(dict_array)
        return DataFrame

    # dictを平坦化する
    def flatten_dict(self,d, pre_lst=[], result=None):
        if result is None:
            result = {}
        for k,v in d.items():
            pre_lst.append(k)
            if isinstance(v, dict):
                self.flatten_dict(v, pre_lst=pre_lst, result=result)
            else:
                result[tuple(pre_lst)] = v
            pre_lst.pop(-1)
        return result 



    def save_csv(self,tweet_datas,i):

        DataFrame = self.create_DataFrame(tweet_datas)
        DataFrame.to_pickle('pkls/{}.pkl'.format(i))


class twitter_api:
    def __init__(self):

        #取得した認証キーを設定
        self.CONSUMER_KEY = os.environ['CONSUMER_KEY']
        self.CONSUMER_SECRE = os.environ['CONSUMER_SECRE']
        self.ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
        self.ACCESS_SECRET = os.environ['ACCESS_SECRET']
        self.api_count = 100

        self.twitter = OAuth1Session(self.CONSUMER_KEY, self.CONSUMER_SECRE, self.ACCESS_TOKEN, self.ACCESS_SECRET)
        self.url = "https://api.twitter.com/1.1/tweets/search/fullarchive/hogehoge.json"
        self.Reshape_data = Reshape_data()

    #APIを叩いてデータを取得する
    def get_data(self,params):
        res = self.twitter.get(self.url, params = params)
        return res

    def run(self):
        next_token = ''

        for i in range(self.api_count):

            if next_token == '':
                params = {'query' : 'タピオカ has:geo -is:retweet', #検索したいワード
                        "maxResults" : "500",
                        "fromDate":"201901010000"}
            else:
                params = {'query' : 'タピオカ has:geo -is:retweet', #検索したいワード
                          "maxResults" : "500",
                          "fromDate":"201901010000",
                          'next':next_token}
 

            res = self.get_data(params)
            r = json.loads(res.text)

            tweet_datas = r['results']
            self.Reshape_data.save_csv(tweet_datas,i)

            if 'next' in r.keys():
                next_token = r['next']
                with open('next_token.txt', mode='w') as f:
                    f.write(next_token)
            else:
                next_token = ''
            time.sleep(10)


env = twitter_api()
env.run()
