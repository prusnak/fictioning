#!/bin/bash
if [ -z "$1" ] ; then
  echo "no jobid"
  exit 1
fi

jobid=$1
jobdir=jobs/$jobid

# ls $jobdir
# iterations=$(cat $jobdir/iterations.txt)

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
