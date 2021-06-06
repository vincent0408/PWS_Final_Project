import processing_total as pt
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


cred = credentials.Certificate("./json/serviceAccountKey_data_total_time.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://data-total-time-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

#df = pt.get_time_data(pt.df)


#ref.set(df.to_dict())