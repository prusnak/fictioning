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
  initimage="-ii ../$jobdir/initimage.png"
else
  initimage=""
fi

echo -n "processing" > $jobdir/status.txt

pushd VQGAN-CLIP

python3 generate.py -i "$iterations" -p "$textprompt" $initimage -o "../$jobdir/%03d.png"

popd

echo -n "done" > $jobdir/status.txt
