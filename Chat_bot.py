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
    product = pd.read_csv("products.csv",encoding = "big5")
    #order state
    if ("我要" in text[:2]):
        members = pd.read_csv("members.csv")
        userid = event.source.user_id 
        for ID in members["ID"]:
            if userid == ID :#確認使用者有註冊會員
                send_text_message(event.reply_token,"訂單已完成")
                return
                
        send_text_message(event.reply_token, "您尚未註冊會員,請先加我好友跟我聊聊天唷>.<")
        #訂單狀態
        
        
    
    #demo  with image carousel
    elif(text == "產品" ):
        print("in 產品")
        push_image_carousel(event.reply_token,product)
    
    elif ("賣" in text):
        print("IN 產品介紹")
        
        #send_text_message(event.reply_token,
        
    
    