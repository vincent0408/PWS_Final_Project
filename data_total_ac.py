import processing_total as pt
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


cred = credentials.Certificate("./json/serviceAccountKey_data_total_ac.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://data-total-ac-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

ref.set(pt.get_ac_num().to_dict())