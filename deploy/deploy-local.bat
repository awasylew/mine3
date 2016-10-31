%~d0
cd %~p0
rmdir venv /s /q
virtualenv venv
call venv\Scripts\activate
pip install -r requirements.txt
pause
