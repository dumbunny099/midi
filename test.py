import pyrebase
config = {
        "apiKey": "AIzaSyDN7aKdltzoA7UPVATLstIW1wpJKIVnHwI",
        "authDomain": "test-55ccb.firebaseapp.com",
        "databaseURL": "https://test-55ccb.firebaseio.com",
        "projectId": "test-55ccb",
        "storageBucket": "test-55ccb.appspot.com",
        "messagingSenderId": "1075050033316",
        "appId": "1:1075050033316:web:136c6efe27c312e2a3f631",
        "measurementId": "G-JPKG9M86K9"
    }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
email = "hotshot12343@gmail.com"
password = "123456"
# user = auth.create_user_with_email_and_password(email, password)
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()
print(db.child("cnt0").child("funny").get().val())
db.child("cnt0").update({"funny" : 5})
db.child("cnt1").update({"sad" : 3})
db.child("cnt2").update({"scared" : 2})
db.child("cnt3").update({"anger" : 4})
db.child("cnt4").update({"nature" : 1})