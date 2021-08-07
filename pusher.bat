@echo off

python backup.py

git branch
set /P commitName="What is the name of the commit? "
git add .
git commit -m "%commitName%"
set /P branchName="What is the name of the branch? "
git push origin "%branchName%"


pause

