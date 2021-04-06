import os
import sys, time

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,PostbackEvent

from User_bot import ToUserMachine
from Chat_bot import Chat_Reply
from utils import send_text_message

load_dotenv()
IDLE_TIME = 30
TIME = None
USER = None
user_machine = ToUserMachine(
	states=["user","func_lobby","member_lobby","check_lobby"],
	transitions=[
		{#初始到功能選則
			"trigger": "advance",
			"source": "user",
			"dest": "func_lobby",
			"conditions": "is_going_to_func_lobby"
		},
		{#初始到功能選則
			"trigger": "advance",
			"source": "func_lobby",
			"dest": "member_lobby",
			"conditions": "is_going_member_lobby",
		},
		{#初始到功能選則
			"trigger": "advance",
			"source": "member_lobby",
			"dest": "check_lobby",
			"conditions": "is_going_check_lobby",
		},
		{#初始到功能選則
			"trigger": "advance",
			"source": "check_lobby",
			"dest": "member_lobby",
			"conditions": "back_member_lobby",
		},
		{#初始到功能選則
			"trigger": "advance",
			"source": "check_lobby",
			"dest": "func_lobby",
			"conditions": "is_leaving_check_lobby",
		},
		{"trigger": "go_back_to_func_lobby", "source": ["check_lobby,member_lobby"], "dest": "func_lobby"},
	],
	initial="user",
	auto_transitions=True,
	show_conditions=True,
)
app = Flask(__name__, static_url_path="")


#get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
	print("Specify LINE_CHANNEL_SECRET as environment variable.")
	sys.exit(1)
if channel_access_token is None:
	print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
	sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
	signature = request.headers["X-Line-Signature"]
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# parse webhook body
	try:
		events = parser.parse(body, signature)
	except InvalidSignatureError:
		abort(400)

	# if event is MessageEvent and message is TextMessage, then echo text
	for event in events:
		if not isinstance(event, MessageEvent):
			continue
		if not isinstance(event.message, TextMessage):
			continue

		line_bot_api.reply_message(
			event.reply_token, TextSendMessage(text=event.message.text)
		)

	return "OK"
	
@app.route("/maintain", methods=["POST"])
def maintain():
	signature = request.headers["X-Line-Signature"]
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# parse webhook body
	try:
		events = parser.parse(body, signature)
	except InvalidSignatureError:
		abort(400)

	# if event is MessageEvent and message is TextMessage
	print("in maintain")
	for event in events:
		if event.source.type == "user":
			send_text_message(event.reply_token,"維修中，請稍後")
		if event.source.type == "group":
			if event.message.text[0] == "!" or event.message.text[0] == "！":
				send_text_message(event.reply_token,"維修中!請稍後~")
			
	return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
	signature = request.headers["X-Line-Signature"]
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info(f"Request body: {body}")
	global TIME#設定全域變數
	global USER#設定全域USER
	global IDLE_TIME
	# parse webhook body
	try:
		events = parser.parse(body, signature)
	except InvalidSignatureError:
		abort(400)
	#call orderbot 
	
	#set multi user buffer
	
	
	for event in events:
		#User state
		if event.source.type == "user":
			print("IN USER STATE")
			if not isinstance(event, MessageEvent):
				continue
			if not isinstance(event.message, TextMessage):
				continue
			if not isinstance(event.message.text, str):
				continue
			if USER == None:
				current_id = event.source.user_id
				USER = current_id			
			else:
				if USER != current_id and time.time()- TIME <IDLE_TIME:#不同人呼叫
					send_text_message(event.reply_token, "伺服器目前占用，請稍後")
					continue
				elif  USER != current_id and time.time()- TIME >IDLE_TIME:#不同人呼叫，超出時間
					print("\nNEW USER\n")
					USER = current_id
					user_machine.to_user(event)
				elif time.time()- TIME >IDLE_TIME:#超出時間重啟FSM
					print("\nRefresh\n")
					USER = None
					user_machine.to_user(event)
			
			if USER == current_id:#計算同一人的回覆時間
				TIME = time.time()
			#print("\nLast Time : ", time.time()- TIME)#若有文字訊息顯示傳值間距
			print(f"\nFSM STATE: {user_machine.state}")
			print(f"REQUEST BODY: \n{body}")
			response = user_machine.advance(event)
			if response == False:
				send_text_message(event.reply_token, "輸入不符合")
		
		#Group State
		elif event.source.type == "group":
			print("IN GROUP")
			if event.message.text[0] == "!" or event.message.text[0] == "！":
				response = Chat_Reply(event)
			
			
		print("\nmessage done\n")
	return "OK"


if __name__ == "__main__":
	port = os.environ.get("PORT", 8000)
	USER = None
	TIME = time.time()#初始時間
	app.run(host="0.0.0.0", port=port, debug=True)