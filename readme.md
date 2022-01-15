[![License: MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](./license.txt)
[![Versions](https://img.shields.io/badge/semver-2.0-green)](https://semver.org/spec/v2.0.0.html)
[![PyPI version](https://badge.fury.io/py/g2w.svg)](https://badge.fury.io/py/g2w)
[![](https://img.shields.io/docker/pulls/dgroup/g2w.svg)](https://hub.docker.com/r/dgroup/g2w "Image pulls")
[![](https://images.microbadger.com/badges/image/dgroup/g2w.svg)](https://microbadger.com/images/dgroup/g2w "Image layers")
[![Commit activity](https://img.shields.io/github/commit-activity/y/dgroup/g2w.svg?style=flat-square)](https://github.com/dgroup/g2w/graphs/commit-activity)
[![Hits-of-Code](https://hitsofcode.com/github/dgroup/g2w?branch=master)](https://hitsofcode.com/view/github/dgroup/g2w?branch=master)

[![CI](https://github.com/dgroup/g2w/actions/workflows/master.yml/badge.svg)](https://github.com/dgroup/g2w/actions/workflows/master.yml)
[![0pdd](http://www.0pdd.com/svg?name=dgroup/g2w)](http://www.0pdd.com/p?name=dgroup/g2w)
[![Dependency Status](https://requires.io/github/dgroup/g2w/requirements.svg?branch=master)](https://requires.io/github/dgroup/g2w/requirements/?branch=master)
[![Known Vulnerabilities](https://snyk.io/test/github/dgroup/g2w/badge.svg)](https://app.snyk.io/org/dgroup/project/97a5d0de-3c9f-40ef-8ed6-42370d7a3330)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dgroup_g2w\&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=dgroup_g2w)
[![Codebeat Badge](https://codebeat.co/badges/76acc08d-e3e2-486d-b377-aee722b58717)](https://codebeat.co/projects/github-com-dgroup-g2w-master)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7d93a4c0de9c40e5bae9633cd6fbc201)](https://www.codacy.com/gh/dgroup/g2w/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dgroup/g2w&amp;utm_campaign=Badge_Grade)
[![Codecov](https://codecov.io/gh/dgroup/g2w/branch/master/graph/badge.svg?token=PSTG3JNRX6)](https://codecov.io/gh/dgroup/g2w)

#### What is Worksection?
[Worksection](https://worksection.com) is a simple, lightweight task tracking system that provides:
 * Project and task management, planning and controlling, team organization
 * Flexible interface, recurring processes, time-tracking
 * Privacy settings, client companies, communication

Check it out.

#### Worksection task id in Git commit messages
Use [commit-msg](commit-msg) file to force your developers to have worksection task id during commits.
Just copy this file to your git repo as
```bash
cp commit-msg <your-git-repo>/.git/hook/commit-msg   # on Git server directly (server-side commit)
```
Since this moment all commit messages should have the following format `#WS-0000: The commit message`, where `0000` is worksection task id.

#### Open API docs
Run it and all endpoints details will be available here: http://localhost:8080/docs
```bash
> python g2w
...                                                                                                                                                
INFO:     Started server process [86248]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

#### Push notifications
Please note, that `GitLab` commit messages must have the following format: `#WS-0000: The commit message`, where `0000` is worksection task id.
1. Deploy locally g2w
    ```yml
    version: "3.9"
    services:
      g2ws:
        image: dgroup/g2w:0.2.0
        container_name: g2w
        environment:
          # Mandatory environment variables (docker, podman, etc.)
          WS_URL_ALL_USERS: "https://xxx.worksection.com/xxxx"    # https://worksection.com/faq/api-user.html#q1572
          WS_URL_POST_COMMENT: "https://xxx.worksection.com/xxxx" # https://worksection.com/faq/api-comments.html#q1575
          WS_ADMIN_EMAIL: "xxx.worksection.bot@gmail.com"         # plain worksection user email
          WS_ADMIN_USER_ID: "370080"                              # plain worksection user id
          WS_PRJ_223728_HASH: "xxx"                               # HASH generated for a particular Worksection project
        build:
          dockerfile: Containerfile
          context: .
        ports:
          - "8080:8080"
        restart: always
    ```
2. Configure webhook with `Push events` in Gitlab: 
   1. Open `project > Settings > Webhook` 
   2. Specify URL http://yourserverwith-g2w:8080/gitlab/push/223728, where `223728` is your worksection project id
   3. Ensure that `Push events` option is selected
   4. Press [`Add webhook`]
3. Configure reference to Worksection tasks from commits in Gitlab: 
   1. Open `project > Settings > Integrations > Custom issue tracker`
   2. Set `Project URL` like https://xxx.worksection.com/project/223728/, where `223728` is your worksection project id
   3. Set `Issue URL` like https://xxx.worksection.com/project/223728/:id
   4. Set `New issue URL` like https://xxx.worksection.com/project/223728/new/
   5. Press [`Save changes`]
4. Push commit(s) with following commit message format `#WS-0000: The commit message` format (`0000` is worksection task id) to your Gitlab project.

#### Simulate push Gitlab event
`223728` - worksection project id (read [more](/tests/test_app.py)):
```bash
curl --request POST \
  --url http://127.0.0.1:8080/gitlab/push/223728 \
  --header 'Content-Type: application/json' \
  --data '{
  "object_kind": "push",
  "event_name": "push",
  "before": "95790bf891e76fee5e1747ab589903a6a1f80f22",
  "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
  "ref": "refs/heads/master",
  "checkout_sha": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
  "user_id": 4,
  "user_name": "John Smith",
  "user_username": "jsmith",
  "user_email": "john@example.com",
  "user_avatar": "https://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=8://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=80",
  "project_id": 15,
  "project":{
    "id": 15,
    "name":"Diaspora",
    "description":"",
    "web_url":"http://example.com/mike/diaspora",
    "avatar_url":null,
    "git_ssh_url":"git@example.com:mike/diaspora.git",
    "git_http_url":"https://example.com/mike/diaspora.git",
    "namespace":"Mike",
    "visibility_level":0,
    "path_with_namespace":"mike/diaspora",
    "default_branch":"master",
    "homepage":"http://example.com/mike/diaspora",
    "url":"git@example.com:mike/diaspora.git",
    "ssh_url":"git@example.com:mike/diaspora.git",
    "http_url":"https://example.com/mike/diaspora.git"
  },
  "repository":{
    "name": "Diaspora",
    "url": "git@example.com:mike/diaspora.git",
    "description": "",
    "homepage": "http://example.com/mike/diaspora",
    "git_http_url":"https://example.com/mike/diaspora.git",
    "git_ssh_url":"git@example.com:mike/diaspora.git",
    "visibility_level":0
  },
  "commits": [
    {
      "id": "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
      "message": "Update Catalan translation to e38cb41.\n\nSee https://gitlab.com/gitlab-org/gitlab for more information",
      "title": "Update Catalan translation to e38cb41.",
      "timestamp": "2011-12-12T14:27:31+02:00",
      "url": "http://example.com/mike/diaspora/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
      "author": {
        "name": "Jordi Mallach",
        "email": "jordi@softcatala.org"
      },
      "added": ["CHANGELOG"],
      "modified": ["app/controller/application.rb"],
      "removed": []
    },
    {
      "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
      "message": "fixed readme",
      "title": "fixed readme",
      "timestamp": "2012-01-03T23:36:29+02:00",
      "url": "http://example.com/mike/diaspora/commit/da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
      "author": {
        "name": "GitLab dev user",
        "email": "gitlabdev@dv6700.(none)"
      },
      "added": ["CHANGELOG"],
      "modified": ["app/controller/application.rb"],
      "removed": []
    }
  ],
  "total_commits_count": 4
}'
```

## Install it from PyPI

```bash
pip install g2w
```

## Materials & Links
* http://www.md5.cz - generate WS hash