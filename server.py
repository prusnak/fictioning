import os, time
from shutil import copyfile
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    send_from_directory,
)

app = Flask(__name__)


def get_job_id():
    return str(int(time.time() * 1e9))


def get_job_dir(id):
    return "jobs/%s" % id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    id = get_job_id()
    job_dir = get_job_dir(id)

    team = request.form["team"]
    textprompt = request.form["textprompt"]
    # imageprompt = request.files["imageprompt"]
    initimage = request.files["initimage"]
    iterations = request.form["iterations"]
    # model = request.form["model"]

    os.mkdir(job_dir)
    open(job_dir + "/status.txt", "wt").write("not started yet")
    open(job_dir + "/team.txt", "wt").write(team)
    open(job_dir + "/textprompt.txt", "wt").write(textprompt)
    # if imageprompt:
    #     imageprompt.save(job_dir + "/imageprompt.png")
    if initimage:
        initimage.save(job_dir + "/initimage.png")
    open(job_dir + "/iterations.txt", "wt").write(iterations)
    for i in range(50, int(iterations) + 50, 50):
        copyfile("static/blank.png", job_dir + "/%03d.png" % i)
    # if model:
    #     open(job_dir + "/model.txt", "wt").write(model)

    return redirect(url_for("show_job", id=id))


@app.route("/job/<id>/<path:path>")
def send_png(id, path):
    return send_from_directory("jobs/" + id, path)


@app.route("/job/<id>")
def show_job(id):
    job_dir = get_job_dir(id)
    status = open(job_dir + "/status.txt", "rt").read()
    team = open(job_dir + "/team.txt", "rt").read()
    textprompt = open(job_dir + "/textprompt.txt", "rt").read()
    imageprompt = os.path.isfile(job_dir + "/imageprompt.png")
    initimage = os.path.isfile(job_dir + "/initimage.png")
    iterations = int(open(job_dir + "/iterations.txt", "rt").read())
    # model = open(job_dir + "/model.txt", "rt").read()

    refresh = status != "done"

    return render_template(
        "job.html",
        id=id,
        refresh=refresh,
        status=status,
        team=team,
        textprompt=textprompt,
        imageprompt=imageprompt,
        initimage=initimage,
        iterations=iterations,
    )
