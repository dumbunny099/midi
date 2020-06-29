from flask import Flask
import pickle
import numpy as np
from music21 import converter,instrument,note,chord,stream
from keras.models import load_model
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
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
storage = firebase.storage()
db = firebase.database()
numberOfSongs = [50,50,50,50,50]
emotions = ["funny","sad", "scared","anger","nature"]
offsets = [0.48, 0.48, 0.5, 0.52, 0.5]

if len(numberOfSongs) == 0:
    print("NO SONGS CREATED")
for emotionNum in range(len(emotions)):
    with open(emotions[emotionNum] + ".bin", "rb") as file:
        data_list = []
        while True:
            try:
                data = pickle.load(file)
            except EOFError:
                break
            data_list.append(data)


    n_vocab = data_list[0]
    net_in = data_list[1]
    int_to_note = data_list[2]
    model = load_model(emotions[emotionNum] + ".h5",compile=False)
    for numberofSong in range(numberOfSongs[emotionNum]):
        print("song of " + emotions[emotionNum] + " #%2d" % numberofSong)
        start = np.random.randint(0, len(net_in) - 1)
        pattern = net_in[start]
        pred_out = []

        for i in range(0, 400):
            pred_in = np.reshape(pattern, (1, len(pattern), 1))
            prediction = model.predict(pred_in, verbose=0)
            index = np.argmax(prediction)
            result = int_to_note[index]
            print('\r', 'Predicted', i, " ", result, end='\n')
            pred_out.append(result)
            pattern = np.append(pattern, index / float(n_vocab))
            pattern = pattern[1:len(pattern)]
        offset = 0
        output_notes = []
        for pattern in pred_out:
            if ('.' in pattern) or pattern.isdigit():
                notes_in_chord = pattern.split('.')
                notes = []
                for current_note in notes_in_chord:
                    new_note = note.Note(int(current_note))
                    new_note.storedInstrument = instrument.StringInstrument()
                    notes.append(new_note)
                new_chord = chord.Chord(notes)
                new_chord.offset = offset
                output_notes.append(new_chord)
            else:
                new_note = note.Note(pattern)
                new_note.offset = offset
                new_note.storedInstrument = instrument.StringInstrument()
                output_notes.append(new_note)
            offset += offsets[emotionNum]
        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp=(emotions[emotionNum] + 'output_%2d.mid' % numberofSong))
        storage.child("midis/" + emotions[emotionNum] + "/output_%2d.mid" % numberofSong).put(
            emotions[emotionNum] + "output_%2d.mid" % numberofSong)
    print(emotions[emotionNum] + " :")
    db.child("cnt"+str(emotionNum)).update({emotions[emotionNum]: 0})
print("All process is completed")