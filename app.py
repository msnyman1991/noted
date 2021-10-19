import flask
from flask import Flask,render_template,request,redirect
from pymongo import MongoClient
import datetime
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from bson.json_util import dumps


app = Flask(__name__)

client = MongoClient('localhost', 27017)

# MongoDB client
db = client.noted.user_notes

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/all_notes')
def all_notes():
    return render_template('all_notes.html')

@app.route('/create_note')
def note():
    return render_template('note.html')

@app.route('/create_note', methods=["POST"])
def post_note():

    # Get data from Note input form
    note_topic = request.form['note_topic']
    note = request.form['note']

    # Note
    author = "Morne"
    date = datetime.datetime.utcnow()
    tags = "[my-note]"

    # Post note to DB
    posts = db.posts
    post_id = posts.insert_one({'note_topic': note_topic, 'note': note, 'author': author, 'date': date, 'tags': tags})
    post_id
    _id = (str(post_id.inserted_id))

    x = print(_id)
    posts.find_one_and_update({"_id": post_id.inserted_id}, 
                                {"$set": {"note_id": (str(post_id.inserted_id))}})

    env = Environment(loader=FileSystemLoader('templates'))
    return redirect("/all_notes")

@app.route('/delete_note', methods=['GET', 'POST'])
def delete_note():

    noteId = request.form['_id']
    
    db = client.noted.user_notes
    posts = db.posts
    delete = posts.delete_one({'note_id': noteId})
    delete

    env = Environment(loader=FileSystemLoader('templates'))
    return redirect("/all_notes")

# Find all notes for user
@app.route('/my_notes')
def find_notes():
    posts = db.posts
    author = "Morne"
    find_notes = posts.find({"author": f"{author}"})

    notes = []
    for x in find_notes:
        notes.append(x)

    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('view_notes.html')
    return flask.Response(tmpl.generate(result=dumps(notes)))

