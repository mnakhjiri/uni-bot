import configparser

import telebot

config = configparser.ConfigParser()
config.read('config.ini')

api = config['bot']['API_KEY']
bot = telebot.TeleBot(api)

admins = config['bot']['ADMIN_IDS'].split(",")
sheet_id = config['bot']['SHEET_ID']
exams_gid = "1143993539"
hw_gid = "0"

sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
exam_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={exams_gid}"
hw_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={hw_gid}"
