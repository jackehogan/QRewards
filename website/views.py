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

@views.route('/qrewards', methods=['GET','POST'])
def qrewards():
    users = User.query.all()
    deals = [note for user in users for note in user.notes]
    idx = random.randint(0,len(deals)-1)
    note = deals[idx]

    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        msg = Message('Hello from the other side!', sender='qrewardsraffle@gmail.com', recipients=[email])
        msg.body = "Hey " + email + " sending you this deal! " + note.data
        print(msg.body)
        mail.send(msg)

    return render_template("qrewards.html",user=current_user,note = note)
