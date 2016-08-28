# gitplaylist

[![CircleCI](https://circleci.com/gh/gitplaylist/backend.svg?style=shield)](https://circleci.com/gh/gitplaylist/backend)
[![codecov](https://codecov.io/gh/gitplaylist/backend/branch/master/graph/badge.svg)](https://codecov.io/gh/gitplaylist/backend)
[![docker](https://img.shields.io/docker/pulls/gitplaylist/backend.svg)](https://hub.docker.com/r/gitplaylist/backend/)
[![Imagelayers](https://imagelayers.io/badge/gitplaylist/backend:latest.svg)](https://imagelayers.io/?images=gitplaylist/backend:latest)
[![Requirements Status](https://requires.io/github/gitplaylist/backend/requirements.svg?branch=master)](https://requires.io/github/gitplaylist/backend/requirements/?branch=master)
[![Maintenance](https://img.shields.io/maintenance/yes/2016.svg?maxAge=2592000)](https://github.com/gitplaylist/backend)


## Setup
```bash
$ git submodule init && git submodule update
$ sudo gem install sass
$ sudo npm install -g browserify babel-cli babelify
$ npm install
$ pip install pip-save
$ pip install -r requirements.txt
$ ./manage.py runserver
```

In project root directory run:
```
ln -s ../../hooks/pre-commit.sh .git/hooks/pre-commit
sudo chmod +x .git/hooks/pre-commit
```

## Project Management
[Trello Organization](https://trello.com/gitplaylist)
