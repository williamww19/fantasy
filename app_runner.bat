@echo off
rem Git change to main branch
git checkout main

rem Update main branch
git pull

rem Run Python script
py main.py

rem Add changes to Git
git add .

rem Commit changes
git commit -m "Automated commit"

rem Push changes
git push
