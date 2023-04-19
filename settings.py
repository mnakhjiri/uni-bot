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
poll_answer_options = ["نظریه گراف", "مدار الک", "معماری", "دی اس", "سیستم عامل", "هوش عبدوس", "هوش سلیمی", "سیگنال",
                       "مدار مجتمع", "جبر خطی", "آمار و احتمال"]
db_user = config['database']["db_user"]
db_pass = config["database"]["db_pass"]
db_host = config["database"]["db_host"]
db_port = config["database"]["db_port"]
db_name = config["database"]["db_name"]
mysql_active = False
