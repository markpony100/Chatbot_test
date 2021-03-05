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


class ToUserMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.product_lst=pd.read_csv("products.csv")

    def is_going_to_func_lobby(self,event):
        return True

    def on_enter_func_lobby(self,event):
        print("In func lobby")
        self.order = {"ID":None,"NAME":None, "PRODUCT":None,"ADDRES":None,"NUMBERS":None,"Phone":None}
        userid = event.source.user_id 
        #push_message(userid,"welcome lobby")
        push_buttons_templates(event.reply_token,
            " Orderbot訂單系統","您想做以下哪個動作?",
            ["訂單查詢","會員登錄"])
        self.order["ID"] = userid
        print("\nUser id : ",self.order,"\n")
    def is_leaving_func_lobby(self,event):
        text = event.message.text
        return text.lower() == "exit"
        
    
