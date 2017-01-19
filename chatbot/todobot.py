import json
import requests
import urllib
import time
from dbhelper import DBHelper

db = DBHelper()


TOKEN = "324199340:AAGcvFLAuMd8adm2snY3HGO4NUVecZzLmHI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)   #insert token to the url

def get_url(url):
	res = requests.get(url)
	content = res.content.decode("UTF-8")
	return content
def get_json_from_url(url):
	content = get_url(url)
	js_content = json.loads(content)
	return js_content

# Return the messages are not replied
def get_updates(offset=None):
	url = URL + "getUpdates"
	if offset:
		url += "?offset={}&timeout=100".format(offset)
	js_content = get_json_from_url(url)
	return js_content

def get_last_update_id(updates):
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)		#return the biggest id in the conversation

def echo_all(updates):
	for update in updates["result"]:
		text = update["message"]["text"]
		chat_id = update["message"]["chat"]["id"]
		send_message(text, chat_id)

def handle_updates(updates):
	for update in updates["result"]:
		text = update["message"]["text"]
		chat_id = update["message"]["chat"]["id"]
		items= db.get_items(chat_id)
		if text == "/done":
			keyboard = build_keyboard(items)
			send_message("Select an item to delete", chat_id, keyboard)
		elif text == "/start":
			send_message("Hola Nguyen xin chao cac ban den voi ung dung ToDoList. Nhap /start de bat dau. Nhap /done de xoa nhung cong viec da xong", chat_id)

		elif text in items:
			db.delete_item(text, chat_id)
			items = db.get_items(chat_id)
			keyboard = build_keyboard(items)
			send_message("select an item to delete", chat_id, keyboard)
		else:
			db.add_item(text, chat_id)
			items = db.get_items(chat_id)
		message = "\n".join(items)
		send_message(message, chat_id)

def get_last_chat_id_and_text(updates):
	num_updates = len(updates["result"])
	last_update = num_updates - 1
	text = updates["result"][last_update]["message"]["text"]
	chat_id = updates["result"][last_update]["message"]["chat"]["id"]
	return(text, chat_id)

def send_message(text, chat_id, reply_markup = None):
	# text = parse.quote_plus(text) 			#correctly encoding our message text
	text = urllib.quote_plus(text.encode('utf-8'))
	url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
	if reply_markup:
		url += "&reply_markup".format(reply_markup)
	get_url(url)

def build_keyboard(items):
	keyboard = [[item] for item in items]
	print keyboard
	reply_markup = {"keyboard" : keyboard, "on_time_keyboard" : True}
	print reply_markup	
	return json.dumps(reply_markup)

def main():
	db.setup()
	last_update_id = None
	while True:
		updates = get_updates(last_update_id)
		if (len(updates["result"]) > 0):
			last_update_id = get_last_update_id(updates) + 1
			print last_update_id
			handle_updates(updates)
		time.sleep(0.5)
if __name__ == '__main__':
	main()