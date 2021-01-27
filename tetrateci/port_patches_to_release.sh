#!/bin/bash
set -o errexit
set -o pipefail

cat <<- EOF > $HOME/.netrc
    machine github.com
    login $GITHUB_ACTOR
    password $GITHUB_TOKEN
    machine api.github.com
    login $GITHUB_ACTOR
    password $GITHUB_TOKEN
EOF
chmod 600 $HOME/.netrc

git config user.name github-actions
git config user.email github-actions@github.com

TARGETS=$(git branch -r | grep origin/tetrate-release)

for branch in $TARGETS; do
    branch_name=$(cut -f2 -d"/" <<< $branch)
    hub pull-request -b $branch -h origin/tetrate-workflow -m "AUTO: Backporting patches to $branch_name"
done