# Deployment Instructions

## The app is ran on our digital ocean instance by modifying the systemd daemon files and ran from systemctl as such

```
Digital Ocean Info:
ip: 137.184.178.55
password: ASK_DEVS
```

- Our project is located at `/home/django/selecto`
- We use Gunicorn for mangaging the running of our service
- You can find these settings here: `/etc/systemd/system/gunicorn.service` 
- You can also change nginx routing traffic by editing `/etc/nginx/sites-enabled/default`
- Don't forget to run `pip install -r requirements.txt`

If you made changes to systemd files... you need to run this to load changes:
```
vim /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
```

## When you want to deploy...

You can stop gunicorn using:
```
sudo systemctl stop gunicorn
```

And you can run gunicorn using...
```
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

If there are permission issues with writing to DB:
```
chown django:django /home/django/selecto/web/selecto
chown django:django /home/django/selecto/web/selecto/db.sqlite3
```

To access the admin page in prod, please go here:
```
http://selecto.pro/admin/
```

The username and password can be created by using your saved superuser account.
This is made by this command:
```
python manage.py createsuperuser

```
