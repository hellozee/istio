#!/bin/bash
set -o errexit
set -o pipefail

git config user.name github-actions
git config user.email github-actions@github.com

TARGETS=$(git branch -r | grep origin/tetrate-release)

for branch in $TARGETS; do
    branch_name=$(cut -f2 -d"/" <<< $branch)
    hub pull-request -b $branch -h origin/tetrate-workflow -m "AUTO: Backporting patches to $branch_name"
done