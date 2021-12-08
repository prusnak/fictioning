import os
import subprocess
import time


def schedule(jobid):
    print("schedule", jobid)
    cwd = os.path.dirname(os.path.realpath(__file__))
    subprocess.Popen(
        [cwd + "/process.sh", jobid],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


while True:
    jobs = sorted(os.listdir("jobs"))
    running = 0

    for j in jobs:
        jobdir = "jobs/" + j
        try:
            status = open(jobdir + "/status.txt", "rt").read()
        except:
            continue
        if status not in ["done", "not started yet"]:
            running = 1
        if not running and status == "not started yet":
            status = "started"
            running = 1
            schedule(j)
        print("%s [%s]" % (j, status))

    print()
    time.sleep(5)
