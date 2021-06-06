import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import pandas as pd

df = pd.read_csv ('C:/Users/Vincent/Desktop/PWS Rankings.csv')
HW_NO = 6
hw_frame = []
for i in range(HW_NO):
    temp = df[df['HW'] == (i+1)]
    temp.columns = ['User', 'HW{} Total Score'.format(i+1), 'HW{}-1'.format(i+1), 'HW{}-2'.format(i+1),
                   'HW{}-3'.format(i+1), 'HW{}-4'.format(i+1), 'HW{}-5'.format(i+1), 'HW']
    hw_frame.append(temp.iloc[:, :-1])
rankings = hw_frame[0]
for i in range(1, HW_NO):
    rankings= pd.merge(rankings, hw_frame[i], on = ['User'], how='outer')
pd.set_option('display.max_rows', None)
rankings = rankings.set_index('User')
rankings.index.name = None
rankings = rankings.fillna(0)
rankings.rename(index={'b06302345@ntu.edu.tw':'b06302345'}, inplace=True)

cred = credentials.Certificate("./json/serviceAccountKey_data_rankings.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://pws-final-project-chart-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

ref.set(rankings.T.to_dict())