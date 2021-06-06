import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import pandas as pd


cred = credentials.Certificate("./json/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://pws-final-project-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

df = pd.read_csv ('C:/Users/Vincent/Desktop/PWS.csv', header = None, usecols=[0, 1, 2, 3, 7],
                 names=['When','ID','Status','Problem','Author'], converters={'Problem': lambda x: str(x)})
me = df[(df['Author'] == 'b06703012') & (df['Status'] == 'Accepted')]
me = me.T
me.columns = range(1,11)

ref.set(me.to_dict())