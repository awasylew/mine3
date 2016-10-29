%~d0
cd %~p0
rmdir dtemp /s /q
mkdir dtemp
robocopy .. dtemp /s /xd deploy venv .git __pycache__
robocopy heroku dtemp /s
cd dtemp
rem cf push
rem pause
rem cd ..
rem rmdir dtemp /s /q
