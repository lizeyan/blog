#!/use/bin/env bash
echo $1
git add $1
git commit -m "auto commit at $(date)"
git push origin master
