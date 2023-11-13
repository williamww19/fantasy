@echo off
rem Run Python script
python main.py

rem Add changes to Git
git add .

rem Commit changes
git commit -m "Automated commit"

rem Push changes
git push
