%~d0
cd %~p0
rmdir dtemp /s /q
mkdir dtemp
robocopy .. dtemp /s /xd deploy venv .git __pycache__
robocopy pws dtemp /s
cd dtemp
cf push
cd ..
rmdir dtemp /s /q
pause
