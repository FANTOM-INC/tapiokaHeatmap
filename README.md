# 使い方
1. .envを作成し、中身を次のようにする。


CONSUMER_KEY = aaaaa


CONSUMER_SECRE = bbbbb


ACCESS_TOKEN = ccccc


ACCESS_SECRET = ddddd

2. get_tweet.pyの下記を変更する。
self.api_count = 100は１００回APIを叩くので任意の自然数に置き換える。
self.url = "https://api.twitter.com/1.1/tweets/search/fullarchive/hogehoge.json"
はfull-archiveのhogehogeというenvironmentを参照するので、適切に置き換える。
[ここ](https://stackoverflow-com.translate.goog/questions/55349475/twitter-premium-not-authorized?_x_tr_sl=en&_x_tr_tl=ja&_x_tr_hl=ja&_x_tr_pto=nui,sc)などを参照するとよい。
      
これでget_tweet.pyの準備は完了である。
この.pyを実行すると、twitterAPIを叩いて取得したデータをpandasのpickle形式でpkls/0.pkl,...に保存する。

3. make_heatmap.pyの下記を変更する。
self.max_file_num = 86はpkls/n.pklの最大値を入力する。86個のファイルを読み込むということである。
self.split_num = 4は1年を４等分、つまり３ヶ月ごとにプロットするということである。12の約数を入力する。
for k in [2019,2020,2021] を表示したい年数に変更する。

これでmake_heatmap.pyの準備は完了である。
この.pyを実行すると、pkls/n.pklを読み込み結合して、時系列でツイート数をヒートマップにすることができる。
