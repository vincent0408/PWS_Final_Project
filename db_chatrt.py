import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import csv
import json
import pandas as pd


cred = credentials.Certificate("./serviceAccountKey_chart.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://pws-final-project-chart-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

d = {'0101':{'b06703012': '1', 'b06703042': '20'}, 
     '0201':{'b06703012': '2', 'b06703042': '19'},
      '0301':{'b06703012': '3', 'b06703042': '18'},
      '0401':{'b06703012': '4', 'b06703042': '17'},
      '0501':{'b06703012': '5', 'b06703042': '16'},
      '0601':{'b06703012': '6', 'b06703042': '15'},
      '0701':{'b06703012': '7', 'b06703042': '14'},
      '0801':{'b06703012': '8', 'b06703042': '13'},
      '0901':{'b06703012': '9', 'b06703042': '12'},
     '1001':{'b06703012': '10', 'b06703042': '11'}}
df = pd.DataFrame(data = d)
ref.set(df.to_dict())
