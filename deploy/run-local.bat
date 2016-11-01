%~d0
cd %~p0..
call deploy\venv\Scripts\activate
set FLASK_APP=mine.py
set FLASK_DEBUG=1
python -m flask run
pause
