from app import app
from flask import render_template, redirect
from flask import request
from .forms import SampleForm
import os
from flask_dramatiq import Dramatiq
import urllib

dramatiq = Dramatiq()

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    form = SampleForm()

    # If form is upon submission and is validated success
    if form.validate_on_submit():
        return redirect('index')

    return render_template('forms.html', form=form)


@app.route('/launch', methods=['GET', 'POST'])
def launch():
    file1 = open('hello-python/handler.py', 'w')
    jsonData = request.args
    code_lines = jsonData['code'].split("\n")

    final_lines = ''
    for line in code_lines:
        final_lines = final_lines + line + "\n\t"

    print(final_lines)
    L = "def handle(req): \n"
    L = L +"\t"+ final_lines +"\n"
    L = L +"\t" + "return req"
    print(L)
    # Writing a string to file
    file1.write(L)
    file1.close()
    os.system("faas-cli build -f ./hello-python.yml; faas-cli push -f ./hello-python.yml; faas-cli deploy -f ./hello-python.yml")
    return {
        "user": "John Doe",
    }


@app.route('/forms', methods=['GET', 'POST'])
def forms():
    form = SampleForm()

    # If form is upon submission and is validated success
    if form.validate_on_submit():
        return redirect('index')

    return render_template('forms.html', form=form)
