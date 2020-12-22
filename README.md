# MGDrivE Factorial Dataset Machine Learning App

<p align="center"><img src="https://user-images.githubusercontent.com/45245420/102834902-1c1b8900-43aa-11eb-867e-9f7c93e73de3.png"/></p>

## How to deploy this app:

1. Clone this repository
```
  git clone https://github.com/conducive333/mgdrive-fdml-app.git
```

2. Make a [Heroku account](https://www.heroku.com/home)

3. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

4. Initialize Heroku
```
  heroku create [app-name]
```

5. Deploy to Heroku
```
  git add .
  git commit -m "initial commit"
  git push heroku main
```

6. To turn on the app, use
```
  heroku ps:scale web=1
```

7. To visit the app, you can either open it from heroku.com or use 
```
  heroku open
```

8. To turn off the app, use
```
  heroku ps:scale web=0
```
