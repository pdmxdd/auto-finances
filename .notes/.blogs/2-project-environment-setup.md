# Project Setup

- local coding environment
- Gmail setup
- Gmail credentials
- running the Gmail Python quickstart

Python3
Virtualenv
  - google-api-python-client 
  - google-auth-httplib2 
  - google-auth-oauthlib
credentials.json

## Virtualenv

```
virtualenv env_auto_finances --python=python3
```

```
source env_auto_finances/bin/activate
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlibCollecting google-api-python-client
pip3 freeze > requirements.txt
```

commit: [master c792641]

## Gmail Project Creation

- create a new project

### Enable OAuth

### Add Scopes

### Add User

### Create OAuth 2.0 Credentials

## Copy Quickstart script into main.py

## Run quickstart

```
python3 main.py
```

### Complete OAuth flow

```
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=154961763791-jamfp5re8tftdsf79cn1l5gm287630dq.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A54999%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly&state=z316LQeGHeq7UjSCiAt5BqOmw9LPv7&access_type=offline
```

#### What is happening?

output:

```
Labels:
CHAT
SENT
INBOX
IMPORTANT
TRASH
DRAFT
SPAM
CATEGORY_FORUMS
CATEGORY_UPDATES
CATEGORY_PERSONAL
CATEGORY_PROMOTIONS
CATEGORY_SOCIAL
STARRED
UNREAD
Notes
Auto-Finances/Transaction/Discover
Auto-Finances/Transaction/Chase
Personal
Auto-Finances/Recorded
Auto-Finances
Auto-Finances/Transaction
Work
```

commit: [master 16c7c17]

## Refactoring quickstart template into something useful

1. get gmail account label names and label ids

store them as a dictonary so I can enter the label name and it will return the ID