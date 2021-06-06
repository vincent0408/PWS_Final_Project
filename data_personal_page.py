import processing_personal as pp
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


cred = credentials.Certificate("./json/serviceAccountKey_data_personal_page.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://data-personal-page-default-rtdb.firebaseio.com//'
	})
ref = db.reference("/")




#ref.set(pp.get_personal_page(pp.df).T.to_dict())