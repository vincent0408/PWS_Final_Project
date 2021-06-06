﻿import processing_total as pt
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


cred = credentials.Certificate("./json/serviceAccountKey_data_total_status.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://pws-final-project-data-total-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/")

ref.set(pt.get_status().to_dict())
