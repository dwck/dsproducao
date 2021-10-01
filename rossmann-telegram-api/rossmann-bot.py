#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:35:56 2021

@author: dwerneck
"""
import pandas as pd
import os
import requests
import json
from flask import Flask,request,Response

# #constants
TOKEN = '1941402217:AAGbyCil-x8R5BaaZROy34xeJAWHXMVxgGU'
# #Bot Info
# https://api.telegram.org/bot1941402217:AAGbyCil-x8R5BaaZROy34xeJAWHXMVxgGU/getMe
# #Get Updates
# https://api.telegram.org/bot1941402217:AAGbyCil-x8R5BaaZROy34xeJAWHXMVxgGU/getUpdates
# #Webhook
# https://api.telegram.org/bot1941402217:AAGbyCil-x8R5BaaZROy34xeJAWHXMVxgGU/setwebHook?url=https://ac637b8658cb6b.localhost.run
# #Webhook Heroku
# https://api.telegram.org/bot1941402217:AAGbyCil-x8R5BaaZROy34xeJAWHXMVxgGU/setwebHook?url=https://dwck-rossmann-bot.herokuapp.com/
# #Send Message
# https://api.telegram.org/bot1941402217:AAGbyCil-x8R5BaaZROy34xeJAWHXMVxgGU/sendMessage

def send_message(chat_id,text):
    url = 'https://api.telegram.org/bot{}/'.format(TOKEN)
    url = url + 'sendMessage?chat_id={}'.format(chat_id)
    r = requests.post(url,json={'text':text})
    print('Status Code:{}'.format(r.status_code))
    
    return None

def load_dataset(store_id):

    df10 = pd.read_csv('test.csv')
    df_store_raw = pd.read_csv('store.csv')
    df_test = pd.merge(df10,df_store_raw,how='left',on='Store')

    # Choosing store for prediction
    df_test = df_test[df_test['Store'] == store_id]

    if not df_test.empty:
        # Remove Closed days and Id
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop('Id',axis=1)

        # Convert df to json
        data = json.dumps(df_test.to_dict(orient='records'))
    else:
        data = 'error'
    
    return data

def predict(data):
    # API call
    url = 'https://dwck-rossmann-model.herokuapp.com/rossmann/predict'
    header = {'Content-type':'application/json'}
    data = data

    r = requests.post(url,data=data,headers=header)
    print('Status Code {}'.format(r.status_code))

    d11 = pd.DataFrame(r.json(),columns=r.json()[0].keys())

    return d11

def parse_message(message):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']
    store_id = store_id.replace('/','')

    try:
        store_id = int(store_id)
    except ValueError:
        store_id = 'error'

    return chat_id,store_id


# API initialize 
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        chat_id,store_id = parse_message(message)

        if store_id != 'error':
            #loading data
            data = load_dataset(store_id)
            if data != 'error':
                #prediction
                d11 = predict(data)
                #calculation
                d22 = d11[['store','prediction']].groupby('store').sum().reset_index()
                #send message
                msg = 'The sales forecast to the store number #{} is ${:,.2f} in the next 6 weeks.'.format(d22['store'].values[0],d22['prediction'].values[0])
                send_message(chat_id,msg)
                return Response('OK',status=200)

            else:
                send_message(chat_id,'Store data is not available')
                return Response('OK',status=200) 

        else:
            send_message(chat_id,'This is not a valid Store ID')
            return Response('OK',status=200)
    else:
        return '<h1> Rossmann Telegram BOT </h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT',5000)
    app.run(host='0.0.0.0',port=port)