# Demo OAuth Web Client

Update `oauthclient/settings.py` to point to the correct `API_HOST` and use the
correct `CLIENT_ID`.

Run using:

```bash
$ virtualenv -p python3 pyenv
$ pyenv/bin/pip install -r requirements.txt
$ pyenv/bin/python manage.py migrate
$ pyenv/bin/python runserver
```
