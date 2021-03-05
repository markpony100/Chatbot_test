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
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.product_lst=pd.read_csv("product.csv")
        
        
    def is_going_to_func_lobby(self,event):
        return True

    def on_enter_func_lobby(self,event):
        print("In func lobby")
        self.order = {"ID":None,"NAME":None, "PRODUCT":None,"ADDRES":None,"NUMBERS":None,"Phone":None}
        userid = event.source.user_id 
        push_message(userid,"welcome lobby")
        push_buttons_templates(event.reply_token,
            " Orderbot訂單系統","您想做以下哪個動作?",
            ["訂單查詢","產品預訂"])
        self.order["ID"] = userid
        print("\nUser id : ",self.order,"\n")
        
    def is_going_to_order_lobby(self, event):
        text = event.message.text
        return text.lower() == "訂單查詢"

    def is_going_to_product_lobby(self, event):
        text = event.message.text
        return text.lower() == "產品預訂"

    def on_enter_order_lobby(self, event):
        print("I'm entering order_lobby")
        push_buttons_templates(event.reply_token,
            "標題","你要做啥?",
            ["leave","remain"])
        #reply_token = event.reply_token
        #send_text_message(reply_token, "Trigger state1")
        #self.go_back_to_lobby()
        
    def on_enter_product_lobby(self, event):
        print("I'm entering product_lobby")
        userid = event.source.user_id 
        push_message(userid,"請點選您要預訂的商品")
        push_carousel(event.reply_token,self.product_lst)
        #push_image_carousel(event.reply_token,self.product_lst)#reply_token,title,product_lst
        #介紹產品:傳圖片
        
    def is_going_to_number_lobby(self,event):
        text = event.message.text
        if  text[:4] == "我想訂購" and text[-1] == "*":
            self.order["PRODUCT"] = text[5:-1] #儲存產品名稱
            print(self.order,"\n")
            return True
        return False
        
    def on_enter_number_lobby(self, event):
        print("I'm entering number_lobby")
        userid = event.source.user_id 
        push_message(userid,"請問您需要幾份(請輸入阿拉伯數字)")

    def is_going_to_info_lobby(self, event):
        text = event.message.text
        try:
            int(text) #確認輸入為數字
            self.order["NUMBERS"] = text
            print(self.order,"\n")
            return True
        except:
            return False
        
    def on_enter_info_lobby(self, event):
        print("Entering info lobby")
        userid = event.source.user_id 
        push_message(userid,"請依以下模板輸入資訊:\n您的姓名\n您的電話\n寄送地址(自取請填自取)")
    
    def is_going_to_check_lobby(self, event):
        text = event.message.text#確認有正確輸入
        text=text.split("\n")
        if len(text)>1:
            self.order["NAME"] = text[0]
            self.order["PHONE"] = text[1]
            self.order["ADDRES"] = text[2]
            return True
        return False
    
    def on_enter_check_lobby(self, event):#訂單確認
        print("Entering check lobby")
        userid = event.source.user_id 
        check_string = "請確認訂單內容:\n姓名: {name}\n電話: {phone}\n地址: {address}\n品項: {product}\n數量: {number}"
        push_message(userid,check_string.format(name=self.order["NAME"],phone=self.order["PHONE"],address=self.order["ADDRES"],product=self.order["PRODUCT"],number=self.order["NUMBERS"]))
        push_buttons_templates(event.reply_token,"訂單確認","*請詳細確認訂單資訊*",["是","否"])#reply_token,title,t_text,buttons
    
    #各狀態下離開的方法
    def on_exit_order_lobby(self,event):
        text = event.message.text
        return text.lower() == "exit"
        
    def on_exit_product_lobby(self,event):
        text = event.message.text
        return text.lower() == "exit"

        
    def on_exit_number_lobby(self,event):

        text = event.message.text
        return text.lower() == "exit"

        
    def on_exit_info_lobby(self,event):
        text = event.message.text
        return text.lower() == "exit"
        
    def on_exit_check_lobby(self, event):
        userid = event.source.user_id 
        text = event.message.text
        if text == "是":
            #SAVE_ORDER()
            push_message(userid,"您已成功建立訂單!")
        elif text == "否":
            push_message(userid,"~重新引導~")
        else :
            return False
        return True
'''
machine = ToMachine(
    states=["user","func_lobby", "order_lobby", "product_lobby","number_lobby","info_lobby","check_lobby"],
    transitions=[
        {#初始到功能選則
            "trigger": "advance",
            "source": "user",
            "dest": "func_lobby",
            "conditions": "is_going_to_func_lobby",
        },
        {#功能選擇至訂單查詢
            "trigger": "advance",
            "source": "func_lobby",
            "dest": "order_lobby",
            "conditions": "is_going_to_order_lobby",
        },
        {#功能選擇至產品預訂
            "trigger": "advance",
            "source": "func_lobby",
            "dest": "product_lobby",
            "conditions": "is_going_to_product_lobby",
        },
        {#產品預訂至選擇數量
            "trigger": "advance",
            "source": "product_lobby",
            "dest": "number_lobby",
            "conditions": "is_going_to_number_lobby",
        },
        {#選擇數量至輸入訂單資訊
            "trigger": "advance",
            "source": "number_lobby",
            "dest": "info_lobby",
            "conditions": "is_going_to_info_lobby",
        },
        {#輸入訂單資訊至訂單確認
            "trigger": "advance",
            "source": "info_lobby",
            "dest": "check_lobby",
            "conditions": "is_going_to_check_lobby",
        },
        {#訂單查詢回功能選擇
            "trigger": "advance",
            "source": "order_lobby",
            "dest": "func_lobby",
            "conditions": "on_exit_order_lobby",
        },
        {#產品預訂至功能選擇
            "trigger": "advance",
            "source": "product_lobby",
            "dest": "func_lobby",
            "conditions": "on_exit_product_lobby",
        },
        {#數量選擇至功能選擇
            "trigger": "advance",
            "source": "number_lobby",
            "dest": "func_lobby",
            "conditions": "on_exit_number_lobby",
        },
        {#資料填寫至功能選擇
            "trigger": "advance",
            "source": "info_lobby",
            "dest": "func_lobby",
            "conditions": "on_exit_info_lobby",
        },
        {#資料填寫至功能選擇
            "trigger": "advance",
            "source": "check_lobby",
            "dest": "func_lobby",
            "conditions": "on_exit_check_lobby",
        }
        #,{"trigger": "go_back_to_func_lobby", "source": ["check_lobby"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=True,
    show_conditions=True,
)'''
