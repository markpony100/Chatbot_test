import os
import json
from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    CarouselTemplate,
    CarouselColumn
)


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

#def save_order(orders):
    
def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"
    
    
def push_message(userid, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(userid, TextSendMessage(text=text))
    return "OK"
    
def send_image_url(reply_token, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"    

def push_buttons_templates(reply_token,title,t_text,buttons):
    line_bot_api = LineBotApi(channel_access_token)
    action = []
    for elem in buttons:
        action.append(MessageTemplateAction(
                                        label=elem,
                                        text=elem
                      ))
    line_bot_api.reply_message(reply_token,
    TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title=title,
                                text=t_text,
                                actions=action
                                )
                        )
     )
def push_image_carousel(reply_token,product_lst):#reply_token,title,product_lst
    line_bot_api = LineBotApi(channel_access_token)
    carousel_cols = []
    for idx in range(len(product_lst)):
        carousel_cols.append(
            ImageCarouselColumn(
                image_url=product_lst.iloc[idx].網址,
                action=MessageTemplateAction(
                    label=product_lst.iloc[idx].產品,
                    text=product_lst.iloc[idx].產品,
                )
            )
        )
    Image_Carousel = TemplateSendMessage(
        alt_text="template",
        template=ImageCarouselTemplate(columns=carousel_cols)
    )
    line_bot_api.reply_message(reply_token,Image_Carousel)
    return "OK"
    
def push_carousel(reply_token,product_lst):
    line_bot_api = LineBotApi(channel_access_token)
    column=[]
    for idx in range(len(product_lst)): #設定columns
        product_rename = ""
        p_name = product_lst.iloc[idx].產品
        action = []
        product_info = product_lst.iloc[idx].規格
        if "+" in product_info:#確認是變動產品名稱
            product_info = product_info.strip("+")
            product_rename = p_name
        
        for elem in product_info.split(","): #設定action
            action.append(MessageTemplateAction(label = product_rename+elem,
                                                 text = "我想訂購 "+product_rename+elem+"*")
                         )
        column.append( CarouselColumn( #設定欄
            thumbnail_image_url=product_lst.iloc[idx].網址,
            title = p_name,
            text='品項',
            actions=action
            )
        )
    Carousel_template = TemplateSendMessage(#建立template
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=column
        )
    )
    line_bot_api.reply_message(reply_token,Carousel_template)
    return "OK"

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
