#!/bin/bash
if [ -z "$1" ] ; then
  echo "no jobid"
  exit 1
fi

jobid="$1"
jobdir="jobs/$jobid"

iterations=$(cat "$jobdir/iterations.txt")
textprompt=$(cat "$jobdir/textprompt.txt")

if [ -f "$jobdir/initimage.png" ]; then
  initimage="$jobdir/initimage.png"
else
  initimage=""
fi

echo -n "working (10 %)" > $jobdir/status.txt
sleep 1
echo -n "working (20 %)" > $jobdir/status.txt
sleep 1
echo -n "working (40 %)" > $jobdir/status.txt
sleep 1
echo -n "working (80 %)" > $jobdir/status.txt
sleep 1
echo -n "working (100 %)" > $jobdir/status.txt
sleep 1

echo -n "done" > $jobdir/status.txt
