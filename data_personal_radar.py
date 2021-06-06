import processing_personal as pp
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import pandas as pd

cred = credentials.Certificate("./json/serviceAccountKey_data_personal_radar.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://data-personal-radar-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

AnswerRate, FinishedACrate, histogram = pp.get_histogram(pp.df)
radar = pp.get_RadarChart(pp.df, AnswerRate, FinishedACrate)

ref.set(radar.T.to_dict())