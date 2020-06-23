from flask import Flask, render_template
from celery import Celery
import sqlite3

app = Flask(__name__)

app.config["CELERY_BROKER_URL"] = 'amqp://ano:ano@localhost:5672/ano' # change the placeholders to your users values
app.config["CELERY_RESULT_BACKEND"] = 'amqp://ano:ano@localhost:5672/ano' # change the placeholders to your users values

celery_beat_schedule = {
    "time_scheduler": {
        "task": "app.number_adding", # sets task to the 'number_adding' function.
        # runs the task every 5 seconds
        "schedule": 5.0,
    }
}

celery = Celery(app.name) # makes the celery app

# basic celery config
celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    beat_schedule=celery_beat_schedule,
)

@app.route("/")
def index():
    conn = sqlite3.connect('database.db') # connects to db
    db = conn.cursor() # creates a cursor to the db

    number = db.execute("SELECT number FROM testtb").fetchone()[0]
    return render_template("index.html", number=number)

@celery.task # used for specifiying functions that should be run with celery
def number_adding(): # define the function
    conn = sqlite3.connect('database.db') # connects to db
    db = conn.cursor() # creates a cursor to the db

    currentNumber = db.execute("SELECT number FROM testtb").fetchone()[0] #  gets the current number from db
    newNumber = currentNumber + 10 # generates a new number
    db.execute("UPDATE testtb SET number=(?)", (newNumber,)) # updates the db with the new number
    conn.commit() # commits the new data
    