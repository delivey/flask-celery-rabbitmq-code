from flask import Flask, render_template
from celery import Celery
import sqlite3

app = Flask(__name__)

app.config["CELERY_BROKER_URL"] = 'amqp://ano:ano@localhost:5672/ano' # Change this
app.config["CELERY_RESULT_BACKEND"] = 'amqp://ano:ano@localhost:5672/ano' # Change this

celery_beat_schedule = {
    "time_scheduler": {
        "task": "app.number_adding",
        "schedule": 5.0, # In seconds
    }
}

celery = Celery(app.name) 

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
    conn = sqlite3.connect('database.db')
    db = conn.cursor() 

    number = db.execute("SELECT number FROM testtb").fetchone()[0]
    return render_template("index.html", number=number)

@celery.task # Don't forget to add this if your function will be run by celery
def number_adding():
    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    currentNumber = db.execute("SELECT number FROM testtb").fetchone()[0] 
    db.execute("UPDATE testtb SET number=number+10") 
    conn.commit()
    
