@echo off
rem Git change to main branch
git checkout main

rem Update main branch
git pull

rem Run Python script
C:\Users\wylyy\Documents\Personal\Fantasy\webapp\venv\Scripts\python.exe C:\Users\wylyy\Documents\Personal\Fantasy\webapp\main.py

rem Add changes to Git
git add .

rem Get current date and time
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a
set datetime=%datetime:~0,14%
set year=%datetime:~0,4%
set month=%datetime:~4,2%
set day=%datetime:~6,2%
set hour=%datetime:~8,2%
set minute=%datetime:~10,2%
set second=%datetime:~12,2%

rem Commit changes with timestamp
git commit -m "Automated commit - %year%-%month%-%day% %hour%:%minute%:%second%"

rem Push changes
git push
