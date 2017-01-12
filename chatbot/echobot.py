import json
import requests
from parse import *

TOKEN = "324199340:AAGcvFLAuMd8adm2snY3HGO4NUVecZzLmHI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)   #insert token to the url
print URL
# print "\n"

def get_url(url):
	res = requests.get(url)
	content = res.content.decode("UTF-8")
	return content
def get_json_from_url(url):
	content = get_url(url)
	js_content = json.loads(content)
	return js_content
def get_updates():
	url = URL + "getUpdates"
	js_content = get_json_from_url(url)
	return js_content

def get_last_chat_id_and_text(updates):
	num_updates = len(updates["result"])
	last_update = num_updates - 1
	text = updates["result"][last_update]["message"]["text"]
	chat_id = updates["result"][last_update]["message"]["chat"]["id"]
	return(text, chat_id)
def send_message(text, chat_id):
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
	# url = parse("sendMessage?text={}&chat_id={}",text,chat_id)
	print url
	# url = URL + "sendMessage?text=" + text + "&chat_id=" + chat_id	
	get_url(url)

text, chat = get_last_chat_id_and_text(get_updates())
# text = text.decode('utf-8', 'ignore')
print text
text = text.encode('ascii', 'ignore')     #Vietnamese to reply
print text, chat
send_message(text, chat)