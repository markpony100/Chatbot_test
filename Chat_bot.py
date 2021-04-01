from transitions.extensions import GraphMachine
from collections import Counter
from utils import (
    send_text_message,
    push_message,
    push_buttons_templates,
    push_image_carousel,
    push_carousel,
    order_check
    )  
import pandas as pd
from linebot import LineBotApi


def Chat_Reply(event):
    print("IN Group Reply")
    text = event.message.text[1:]
    print(text)
    product = pd.read_csv("Products.csv",encoding = "big5")
    #order state
    if ("我要" in text[:2]):
        print("In Order")
        print(product.Keys)
        members = pd.read_csv("Members.csv",encoding="big5")
        userid = event.source.user_id 
        for idx, ID in enumerate(members["ID"]):
            if userid == ID :#確認使用者有註冊會員
                #儲存訂單資訊
                order = order_check(text[2:],product)
                if order:
                    order_df = pd.read_csv("Orders.csv",encoding = "big5")
                    info = members.iloc[idx]
                    df = pd.DataFrame([[info.ID,
                                        info.NAME,
                                        info.ADDRESS,
                                        info.PHONE,
                                        order[0],
                                        order[1]]],
                                        columns = ["ID","姓名","地址","手機","產品","數量"])
                    order_df=pd.concat([order_df,df])
                    order_df.to_csv("Orders.csv",encoding = "big5",index=False)
                    send_text_message(event.reply_token,info.NAME+"的訂單已完成")
                return
        send_text_message(event.reply_token, "您尚未註冊會員,請先加我好友跟我聊聊天唷>.<")
        #訂單狀態
        
        
    
    #demo  with image carousel
    elif(text == "產品" ):
        print("in 產品")
        push_image_carousel(event.reply_token,product)

        
    
    