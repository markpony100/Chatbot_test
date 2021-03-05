from transitions.extensions import GraphMachine
from collections import Counter
from utils import (
    send_text_message,
    push_message,
    push_buttons_templates,
    push_image_carousel,
    push_carousel)
import pandas as pd
from linebot import LineBotApi


def Chat_Reply(event):
    print("IN Group Reply")
    text = event.message.text[1:]
    print(text)
    userid = event.source.user_id 
    product = pd.read_csv("products.csv")
    print(product["產品"])
    #Order State
    if ("我要" in text[:2]):
        members = pd.read_csv("members.csv")
        
        if userid not in members["ID"]:#確認使用者有註冊會員
            send_text_message(event.reply_token, "您尚未註冊會員,請先加我好友跟我聊聊天唷>.<")
            return
        
        
    
    
    if(text in product["產品"].values):
        print("in 產品")
        push_carousel(event.reply_token,product)
        
    
    