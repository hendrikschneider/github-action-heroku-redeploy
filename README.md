# github-action-heroku-redeploy
Github action to rebuild a deployed heroku app.

# Usage:
1) Create API token: https://devcenter.heroku.com/articles/platform-api-quickstart#authentication
2) Set Github secret:
    - HEROKU_API_KEY
    
3) Add workflow:
```
on: [push]

jobs:
  Redeploy:
    runs-on: ubuntu-latest
    name: Redeploy
    steps:
    - name: Redeploy
      uses: hendrikschneider/github-action-heroku-redeploy@v1.0
      with:
        HEROKU_APP_NAME: ${{secrets.HEROKU_APP_NAME}}
        HEROKU_API_KEY: ${{secrets.HEROKU_API_KEY}}
```