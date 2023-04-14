
# Uni bot

A simple telegram bot for handling university deadlines and exams written in python.



## Features

- Getting exams and homeworks from google sheets document
- Custom alerts for users
- Hidden words for filtering content

## How to start?

Get your telegram bot API from https://t.me/BotFather.

Create your google document sheet. 

[Example for homeworks]("https://docs.google.com/spreadsheets/d/16I2GAZeuPgf6hgF9X41eIPItPQD1ELIDY5IHv17MsuY/edit#gid=0")

[Example for Exams]("https://docs.google.com/spreadsheets/d/16I2GAZeuPgf6hgF9X41eIPItPQD1ELIDY5IHv17MsuY/edit#gid=1143993539")

## Deployment

Create config.ini file near project files.

The content of this file should be like this:


```config.ini
[bot]
API_KEY=AAAAAAAAAAAAA
SHEET_ID=AAAAAAAAAAA
ADMIN_IDS=11111111111111
```

Now you can start your bot with:
```
python3 bot.py
```
