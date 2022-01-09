from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://Andrew:password@cluster0-xth9g.mongodb.net/Richard?retryWrites=true&w=majority")
db = client.get_database('total_records')
records = db.register


# Add your connection string into your application code
# client = pymongo.MongoClient("mongodb+srv://Andrew:<password>@cluster0.g9opq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client.test
