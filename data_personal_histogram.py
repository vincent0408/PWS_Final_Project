import processing_personal as pp
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


cred = credentials.Certificate("./json/serviceAccountKey_data_personal_histogram.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://data-personal-histogram-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

answer_rate, finished_ac_rate, histogram = pp.get_histogram(pp.df)

ref.set(answer_rate.T.to_dict())

