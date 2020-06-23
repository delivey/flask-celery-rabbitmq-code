# flask-celery-rabbitmq-code

The tutorial code for: https://medium.com/@delivey/celery-beat-scheduler-flask-rabbitmq-e84cdba63ab7

## Running the app
1. Run `sudo rabbitmq-server`
2. Run `celery -A app.celery worker --loglevel=INFO --pidfile=''` in another terminal window.
3. Run `celery -A app.celery beat --loglevel=INFO --pidfile=''` in yet another terminal.
4. Finally, run `flask run` and the website should be up on: http://127.0.0.1:5000/
