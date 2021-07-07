""" Application entry point """
from app import app
from rq import Queue
from rq.job import Job
from worker import conn

q = Queue(connection=conn)

# Used for development only
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
