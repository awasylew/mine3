%~d0
cd %~p0
rmdir dtemp /s /q
mkdir dtemp
robocopy .. dtemp /s /xd deploy .git __pycache__
robocopy heroku dtemp /s
cd dtemp

call heroku apps:destroy --app mine1-test --confirm mine1-test
call heroku apps:create mine1-test
git init
call heroku git:remote -a mine1-test
git add .
git commit -am "commiting for deployment"
git push heroku master
rem rmdir dtemp /s /q
pause
