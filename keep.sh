#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${DIR}
git add source
git commit -m "auto commit at $(date)"
git push origin master
