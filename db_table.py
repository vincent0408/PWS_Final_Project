import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import csv
import json
import pandas as pd


cred = credentials.Certificate("./json/serviceAccountKey_table.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://pws-final-project-tab-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

df = pd.read_csv ('C:/Users/Vincent/Desktop/PWS.csv', header = None,
                 names=['When','ID','Status','Problem','Time', 'Memory', 'Language',
                        'Author', 'HW'], converters={'Problem': lambda x: str(x),
                        'HW': lambda x: '-'.join(x.split())})
df['Problem'] = '0' + df['HW'].apply(lambda x:x[-1])  + df['Problem'].apply(lambda x: x[-2:])
df['When'] = df['When'].apply(lambda x:x.replace('-', '/'))
ref.set(df.T.to_dict())


