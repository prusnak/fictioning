import os, time
from shutil import copyfile
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    send_from_directory,
    make_response,
)

app = Flask(__name__)


def get_job_id():
    return str(int(time.time() * 1e9))


def get_job_dir(id):
    return "jobs/%s" % id


def get_mode():
    try:
        return open("mode.txt", "rt").read()
    except:
        return "freestyle"


@app.route("/")
def index():
    mode = get_mode()
    if mode == "freestyle":
        custom_init_image = True
        last_jobid = None
        iterations = None
    else:
        custom_init_image = False
        try:
            last_jobid = request.cookies.get("last_jobid")
            if last_jobid is not None:
                job_dir = get_job_dir(last_jobid)
                iterations = int(open(job_dir + "/iterations.txt", "rt").read())
            else:
                last_jobid = None
                iterations = None
        except:
            custom_init_image = True
            last_jobid = None
            iterations = None

    team = request.cookies.get("team", "")

    return render_template(
        "index.html",
        custom_init_image=custom_init_image,
        last_jobid=last_jobid,
        iterations=iterations,
        team=team,
    )


@app.route("/reflect")
def reflect():
    return render_template("reflect.html")


@app.route("/mode/<mode>")
def mode_workshop(mode):
    open("mode.txt", "wt").write(mode)
    return "mode=%s" % mode


@app.route("/submit", methods=["POST"])
def submit():
    id = get_job_id()
    job_dir = get_job_dir(id)

    team = request.form["team"]
    textprompt = request.form["textprompt"]
    # imageprompt = request.files["imageprompt"]
    try:
        initimage = request.files["initimage"]
    except:
        initimage = None
    try:
        initimage_ref = request.form["initimage_ref"]
    except:
        initimage_ref = None
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
    elif initimage_ref:
        copyfile(job_dir + '/../' + initimage_ref, job_dir + "/initimage.png")
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
    mode = get_mode()

    resp = make_response(
        render_template(
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
    )

    resp.set_cookie("team", team)
    if mode != "freestyle":
        resp.set_cookie("last_jobid", id)

    return resp
