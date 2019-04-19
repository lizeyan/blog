#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${DIR}
git pull origin master
cd /git/directory
if [[ `git status --porcelain` ]]; then
  # Changes
  git add source
  git commit -m "auto commit at $(date)"
  git push origin master
else
  # No changes
  echo No changes
fi
