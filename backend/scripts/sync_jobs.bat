@echo off

cd /d C:\Users\user\Desktop\new\job-matcher\backend

if not exist logs mkdir logs

C:\Users\user\Desktop\new\job-matcher\backend\.venv\Scripts\python.exe -m scripts.sync_jobs >> logs\sync_jobs.log 2>&1