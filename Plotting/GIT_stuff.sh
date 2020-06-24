#
#!/bin/bash

# Git commands
alias gp='git pull'
alias gpp='git push'
alias gs='git status'
alias gsu='git status -uno'
alias ga='git add'
alias gc='git commit -m'

# Forced pull
git fetch --all
git reset --hard origin/master

# Sparse checkout (will still fetch everything first)
mkdir <repo>
cd <repo>
git init
git remote add -f origin <url>

git config core.sparseCheckout true

echo "some/dir/" >> .git/info/sparse-checkout
echo "another/sub/tree" >> .git/info/sparse-checkout

git pull origin master
