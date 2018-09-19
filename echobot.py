'''
Created on 19.09.2018

@author: fpuller
'''
from time import sleep
import data

TOKEN = data.TOKEN
CHAT_ID = data.CHAT_ID

import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from threading import Thread

SNOOZE=False;
ALRM=False;

def set_snooze():
    global SNOOZE
    print "set snooze"
    SNOOZE=True

def unset_snooze():
    global SNOOZE
    print "unset snooze"
    SNOOZE=False
    
def snooze():
    global SNOOZE
    return SNOOZE


def threaded_function(arg):
    print "thread start"
    time.sleep(60)
    unset_snooze()
    print "thread end"

def threaded_function_alarm(arg):
    print "thread start"
    for i in range(10):
        on_alarm_message()
        sleep(3)
    print "thread end"


def send_msg(text):
    chat_id = CHAT_ID
    bot.sendMessage(chat_id, text)    
  
def on_alarm_message():
    #content_type, chat_type, chat_id = telepot.glance()
    chat_id = CHAT_ID
    
    if not SNOOZE:            
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text='Snooze', callback_data='press')],
                   ])    
        bot.sendMessage(chat_id, 'Rauchalarm', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
  
    
    if snooze():
        bot.answerCallbackQuery(query_id, text='already Sleeping')
    bot.answerCallbackQuery(query_id, text='Sleeping... 60 seconds')
    set_snooze()
    thread = Thread(target = threaded_function, args = (10, ))
    thread.start()
        
    


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    
    if content_type == 'text':
        cmd = msg['text']
    
    if cmd.lower() == 'test':   
    
        if snooze():
            print "sleeping"
            send_msg("sleeping...")
        else:
            print "not sleeping"
            thread = Thread(target = threaded_function_alarm, args = (10, ))
            thread.start()
            
    else:
        send_msg("cmd unknown")
        

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    #warte auf Alarm
    sleep(10)
