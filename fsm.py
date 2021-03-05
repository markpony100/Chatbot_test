from transitions.extensions import GraphMachine
from collections import Counter
from utils import send_text_message,push_message
import pandas as pd


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        #self.info = {"ID":None,"Product":None,"ADDRES":None,"NUMBERS":None}
        
    def is_going_to_lobby(self,event):
        return True
        
        
    def on_enter_lobby(self, event):
        print("In lobby")
        userid = event.source.user_id 
        push_message(userid,"You are in lobby")
        push_message(userid,"welcome")
       
        
    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_state1(self, event):
        print("I'm entering state1")
        reply_token = event.reply_token
        
        send_text_message(reply_token, "Trigger state1")
        #self.go_back_to_lobby()
        
    def remain_state1(self,event):
        text = event.message.text
        return text.lower() == "remain"
        
    def on_exit_state1(self,event):
        text = event.message.text
        #print("Leaving state1")
        return text.lower() == "leave state1"

    def on_enter_state2(self, event):
        print("I'm entering state2")
        #push_message(userid,"entering state2")
        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        #self.go_back_to_lobby()

    def on_exit_state2(self):
        print("Leaving state2")
