import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import csv
import json
import pandas as pd


cred = credentials.Certificate("./json/serviceAccountKey_password.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://pws-final-project-password-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

df = pd.read_csv ('C:/Users/Vincent/Desktop/pws_user.csv', header=None)
df.insert(1, '',df[0] )
df = df.T
df.columns = df.iloc[0]
df = df[1:].T
df.index.name = None
df.columns = ['Password']
#d = {'b06703012': ['1234'], 'b06703042': ['5678'], 'b06702055':['1234']}
#df = pd.DataFrame(data = d)
ref.set(df.T.to_dict())
