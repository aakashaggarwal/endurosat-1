from app import app
from flask import render_template, redirect
from flask import request
from .forms import SampleForm
import os
import urllib
from rq import Queue
from rq.job import Job
from worker import conn
import requests


def get_result(value_string):
    response = requests.post('http://134.209.128.19:8080/function/hello-python', data=value_string)
    return response.text

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    form = SampleForm()

    # If form is upon submission and is validated success
    if form.validate_on_submit():
        return redirect('index')

    return render_template('forms.html', form=form)

@app.route('/result', methods=[ 'POST'])
def result():
    jsonData = request.args['string_value']
    q = Queue(connection=conn)

    job = q.enqueue_call(
        func=get_result, args=(jsonData,), result_ttl=5000
    )
    return str(job.get_id()), 200


@app.route('/launch', methods=['GET', 'POST'])
def launch():
    file1 = open('hello-python/handler.py', 'w')
    jsonData = request.args
    # code_lines = jsonData['code'].split("\n")

    # final_lines = ''
    # for line in code_lines:
    #     final_lines = final_lines + line + "\n\t"

    # print(final_lines)
    # Writing a string to file
    file1.write(jsonData['code'])
    file1.close()
    os.system("faas-cli build -f ./hello-python.yml; faas-cli push -f ./hello-python.yml; faas-cli deploy -f ./hello-python.yml")
    return {
        "user": "John Doe",
    }

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202


@app.route('/forms', methods=['GET', 'POST'])
def forms():
    form = SampleForm()

    # If form is upon submission and is validated success
    if form.validate_on_submit():
        return redirect('index')

    return render_template('forms.html', form=form)
