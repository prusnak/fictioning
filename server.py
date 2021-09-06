import os, time
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

def get_job_id():
    return str(int(time.time() * 1e9))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    id = get_job_id()
    job_dir = "jobs/%s" % id

    job_label = request.form["job_label"]
    initial_file = request.files["initial_file"]

    os.mkdir(job_dir)
    open(job_dir + "/label.txt", "wt").write(job_label)
    initial_file.save(job_dir + "/initial.jpg")

    return redirect(url_for("show_job", id=id))

@app.route("/job/<id>")
def show_job(id):
    return "job: " + id
