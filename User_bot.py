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

    def is_going_to_func_lobby(self,event):
        return True

    def on_enter_func_lobby(self,event):
        print("In func lobby")
        self.data = {"ID":None,"NAME":None,"ADDRESS":None,"PHONE":None}
        userid = event.source.user_id 
        #push_message(userid,"welcome lobby")
        push_buttons_templates(event.reply_token,
            " Orderbot訂單系統","您想做以下哪個動作?",
            ["訂單查詢","會員登錄"])
        self.data["ID"] = userid
        print("\nUser id : ",self.data,"\n")
        
    def is_leaving_func_lobby(self,event):
        text = event.message.text
        if text.lower() == "exit":
            self.go_back_to_func_lobby()
            
    def is_going_member_lobby(self, event):
        text = event.message.text
        return text.lower() == "會員登錄"
    def on_enter_member_lobby(self , event):
        push_message(self.data["ID"],"請依以下模板輸入:\n您的大名/暱稱\n寄送地址/自取地區\n您的電話")
        
    def is_leaving_member_lobby(self, event):
        text = event.message.text
        if text.lower() == "exit":
            self.go_back_to_func_lobby()
            
    def is_going_check_lobby(self,event):
        text = event.message.text
        sent = text.split("\n")
        if len(sent) == 3:
            self.data["NAME"]= sent[0]
            self.data["ADDRESS"]= sent[1]
            self.data["PHONE"]= sent[2]
            return True
        return False
        
    def on_enter_check_lobby(self,event):
        check_string = "請確認訂單內容:\n姓名: {name}\n電話: {phone}\n地址: {ADDRESS}"
        push_message(self.data["ID"],check_string.format(name=self.data["NAME"],phone=self.data["PHONE"],ADDRESS=self.data["ADDRESS"]))
        push_buttons_templates(event.reply_token,"資料確認","*請詳細確認訂單資訊*",["是","否"])
        
    def back_member_lobby(self, event):
        text = event.message.text
        return text.lower() == "否"
    
    def is_leaving_check_lobby(self,event):
        text = event.message.text
        if text.lower() == "是":
            save_data = pd.DataFrame({"ID":[self.data["ID"]],
                                      "NAME":[self.data["NAME"]],
                                      "ADDRESS":[self.data["ADDRESS"]],
                                      "PHONE":["'"+self.data["PHONE"]]})
            members = pd.read_csv("members.csv",encoding= "big5")
            pd.concat([members,save_data]).to_csv("members.csv",encoding = "big5",index=False)
            push_message(self.data["ID"],"註冊成功")
            return True