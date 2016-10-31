%~d0
cd %~p0
rmdir temp-heroku /s /q
mkdir temp-heroku
robocopy .. temp-heroku /s /xd deploy .git __pycache__
robocopy heroku temp-heroku /s
cd temp-heroku

call heroku apps:destroy --app mine1-test --confirm mine1-test
call heroku apps:create mine1-test
git init
call heroku git:remote -a mine1-test
git add .
git commit -am "commiting for deployment"
git push heroku master

cd ..
rmdir temp-heroku /s /q
pause
