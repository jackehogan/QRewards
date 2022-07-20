from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db, mail
import json
import random
from flask_mail import Mail, Message

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/qrewards/<location>', methods=['GET','POST'])
def qrewards(location):
    print(location)
    # users = User.query.all()
    users = User.query.filter_by(location=location)
    deals = [note for user in users for note in user.notes]
    idx = random.randint(0,len(deals)-1)
    note = deals[idx]

    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        msg = Message('Hello from QRewards!', sender='qrewardsraffle@gmail.com', recipients=[email])
        msg.body = "Hey " + email + " sending you this deal! " + note.data
        print(msg.body)
        mail.send(msg)

        # import vonage
        # client = vonage.Client(key="5f841ab4", secret="zzWhOuUmzunlOL7x")
        # sms = vonage.Sms(client)
        #
        # responseData = sms.send_message(
        #     {
        #         "from": "18335787007",
        #         "to": "14152331142",
        #         "text": "A text message sent using the Nexmo SMS API",
        #     }
        # )
        #
        # if responseData["messages"][0]["status"] == "0":
        #     print("Message sent successfully.")
        # else:
        #     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    return render_template("qrewards.html",user=current_user,note = note)
