from folium.plugins import heat_map_withtime
import pandas as pd
import json
import numpy as np
from pprint import pprint
import itertools
import datetime
from dateutil.relativedelta import relativedelta
import folium
from folium import plugins

class Environments:
    def __init__(self):
        self.max_file_num = 250
        self.split_num = 4

    def concat_df(self, max_file_num):

        df = pd.read_pickle('pkls/0.pkl')
        for i in range(1,max_file_num):
            df = pd.concat([df,pd.read_pickle('pkls/{}.pkl'.format(i))],axis=0,join='inner',ignore_index=True)
        return df

       
    def format_df(self,df):
        DataFrame = pd.DataFrame([],columns = {}).dropna()
        DataFrame['created_at'] = df[('created_at',)].map(lambda x:datetime.datetime.strptime(x,'%a %b %d %H:%M:%S +0000 %Y'))

        DataFrame['prefecture'] = df[('place', 'name')]
        DataFrame['latitude'] = df[('place', 'bounding_box', 'coordinates')].map(lambda x: np.array(x)[0,:,1].mean() if type(x) == list else x)
        DataFrame['longitude'] = df[('place', 'bounding_box', 'coordinates')].map(lambda x: np.array(x)[0,:,0].mean() if type(x) == list else x)
        DataFrame['text'] = df[('text',)]

        return DataFrame

    def DataFrame_groupby(self,df,keys):
        DataFrame = df[[keys,'latitude']].groupby([keys]).mean()
        DataFrame['longitude'] = df[[keys,'longitude']].groupby([keys]).mean()
        df['count'] = 0.1
        DataFrame['count'] = df[[keys,'count']].groupby([keys]).sum()
        return DataFrame
       
    def run(self):
        DataFrame = self.concat_df(self.max_file_num)
        DataFrame = self.format_df(DataFrame)

        time_columns = []
        df_timeSeries = pd.DataFrame([],columns={})

        for k in [2019,2020,2021]:
            start_date = datetime.datetime(k,1,1,0,0,0)
            for i in range(self.split_num):
                now_date_s = start_date + relativedelta(month=1+i*int(12/self.split_num))
                now_date_e = start_date + relativedelta(month=(i+1)*int(12/self.split_num))

                DataFrame_sep_month =  DataFrame[(now_date_s<=  DataFrame['created_at']) & (DataFrame['created_at'] <= now_date_e) ]
                DataFrame_sep_month = self.DataFrame_groupby(DataFrame_sep_month,'text')
                column_name = now_date_s.strftime('%Y/%m')
                df_timeSeries = pd.concat([df_timeSeries,DataFrame_sep_month[['count']].rename(columns={'count':column_name})],axis=1)
                time_columns.append(column_name)



        df_coordinates = self.DataFrame_groupby(DataFrame,'text')[['latitude','longitude']]

        df_timeSeries = pd.concat([df_timeSeries,df_coordinates],axis=1)
        df_timeSeries = df_timeSeries.fillna(0)
 
        heat_map_data = []
        for idx in time_columns:
            heat_map_data_per_month = []

            for i in range(len(df_timeSeries)):
                df_timeSeries_sep = df_timeSeries[['latitude','longitude',idx]].iloc[i]
                if df_timeSeries_sep[idx] != 0:
                    heat_map_data_per_month.append([df_timeSeries_sep['latitude'],df_timeSeries_sep['longitude'],df_timeSeries_sep[idx]])
            heat_map_data.append(heat_map_data_per_month)
            
        japan_map = folium.Map(location=[35, 135], zoom_start=6)
        hm = plugins.HeatMapWithTime(heat_map_data, index=list(time_columns),auto_play=False,radius=20,max_opacity=1,gradient={0.05: 'blue', 0.25: 'lime', 0.5:'yellow',0.75: 'orange', 0.9:'red'})

        Hm.add_to(japan_map)
        japan_map.save("map.html")
 

        



env = Environments()
env.run()
