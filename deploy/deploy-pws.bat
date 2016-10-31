%~d0
cd %~p0
rmdir temp-pws /s /q
mkdir temp-pws
robocopy .. temp-pws /s /xd deploy .git __pycache__
robocopy pws temp-pws /s
cd temp-pws
cf push
cd ..
rmdir temp-pws /s /q
pause
