import flask
from flask import Flask,render_template,request
import pymongo
from pymongo import MongoClient
import datetime
import pprint

client = MongoClient('localhost', 27017)

# MongoDB client
db = client.noted.user_notes

# Note
author = "Morne"
date = datetime.datetime.utcnow()
tags = "[my-note]"
note_topic = input("Note Topic: ")
note = input("Write a Note: ")

post = {"author": f"{author}",
        "topic": f"{note_topic}",
         "text": f"{note}",
         "tags": f"{tags}",
         "date": f"{date}"}

# Post note to DB
posts = db.posts
post_id = posts.insert_one(post).inserted_id
post_id

# Find all notes for user
find_notes = posts.find({"author": f"{author}"})

for document in find_notes:
        print(document['text'])