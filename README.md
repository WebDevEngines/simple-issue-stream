## Simple Issue Stream
Stream Github issues in a simplified CSV format  

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/WebDevEngines/simple-issue-stream)

Set environment:  
```
export GITHUB_USERNAME='username'
export GITHUB_PASSWORD='password'
export GITHUB_REPOSITORY='repo'
export TOKEN='random_token'
```

Use from Google Sheets:  
```
=IMPORTDATA("https://<your-heroku-app>.herokuapp.com/?user_token=<random_token>")
```