## Simple Issue Stream
Github Issues to CSV  

### Demo
https://demo-simple-issue-stream.herokuapp.com?user_token=249734g73h4g9shdnvosdnjv0824hg24908hg0eingpeg

### Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/WebDevEngines/simple-issue-stream)

### Environment

```
export GITHUB_USERNAME='username'
export GITHUB_PASSWORD='password'
export GITHUB_REPOSITORY='repo'
export TOKEN='random_token'
```

### Google Sheets Integration

```
=IMPORTDATA("https://<your-heroku-app>.herokuapp.com/?user_token=<TOKEN>")
```
