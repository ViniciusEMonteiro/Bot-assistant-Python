#!/usr/bin/env python
import os
import telepot
import time
import sqlite3
import json
import socket
import sys
import datetime
import _thread
import cv2
import requests
import threading 

import struct
import configparser
import psycopg2

from telepot.loop import MessageLoop
from configparser import ConfigParser
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from array import array
import numpy as np
import base64

confirmFlag = None
userName = None
chat_id = None
text = None

cwd = os.getcwd()
config_file = ConfigParser()
config_file.read(cwd+'/config')

Bot_Name=config_file.get('Develop configuration','Bot_Name')
Bot_hash=config_file.get('Develop configuration', 'Bot_hash')
BD_IP=config_file.get('Develop configuration', 'BD_IP')
BD_Port=config_file.get('Develop configuration', 'BD_Port')
BD_Name=config_file.get('Develop configuration', 'BD_Name')
BD_User=config_file.get('Develop configuration', 'BD_User')
BD_Pass=config_file.get('Develop configuration', 'BD_Pass')

print ("Let's started... My name is " + Bot_Name)

bot = telepot.Bot(Bot_hash)

def enviar_imagem(frame, chat_id):

	retval, buffer = cv2.imencode('.jpg', frame)

	body = {
		'chat_id': chat_id,
    }
	files = {
		'photo': buffer,
    }
	r = requests.post('https://api.telegram.org/bot{}/sendPhoto'.format(Bot_hash), data=body, files=files)
	if r.status_code >= 400:
		print('Houve um erro ao enviar mensagem. Detalhe: {}'.format(r.text))
	else:
		print('Mensagem enviada com sucesso.')

clf = cv2.CascadeClassifier(cwd+'/haarcascade_frontalface_alt.xml')

conn = None
cursor = None

try:
	print('Connecting to the PostgreSQL database...')
	conn = psycopg2.connect(host=BD_IP, port=BD_Port, database=BD_Name, user=BD_User, password=BD_Pass)
	cursor = conn.cursor()

	cursor.execute(str("CREATE TABLE IF NOT EXISTS public.table_user (id BIGINT PRIMARY KEY NOT NULL,name TEXT,id_type_user INT, monitoramento BOOL);"))
	cursor.execute(str("CREATE TABLE IF NOT EXISTS public.table_type_user (id serial PRIMARY KEY NOT NULL,name TEXT);"))
	cursor.execute(str("CREATE TABLE IF NOT EXISTS public.table_service (id serial PRIMARY KEY NOT NULL,name TEXT,help TEXT,host TEXT,port INT,id_type_service INT,token TEXT);"))
	cursor.execute(str("CREATE TABLE IF NOT EXISTS public.table_type_service (id serial PRIMARY KEY NOT NULL,Name TEXT);"))
	cursor.execute(str("CREATE TABLE IF NOT EXISTS public.table_request (id serial PRIMARY KEY NOT NULL,name TEXT,id_service INT,path TEXT,numberParans INT,nameParans TEXT,TypeParans TEXT);"))
	cursor.execute(str("CREATE TABLE IF NOT EXISTS public.table_alias (id serial PRIMARY KEY NOT NULL,name TEXT,id_user INT,id_request INT,defaultMessage TEXT);"))
	conn.commit()
	
	print('Conected!')

except (Exception, psycopg2.DatabaseError) as error:

	print('ERRO: ') 

	print(error)

	cursor.close()

	exit()

monitoramento = 0

def handle(msg):

	global userName, chat_id, text, confirmFlag

	conn = psycopg2.connect(host=BD_IP, port=BD_Port, database=BD_Name, user=BD_User, password=BD_Pass)

	cursor = conn.cursor()

	chat_id = msg['chat']['id']

	if('text' in msg):
		text = msg['text']

	print('Mensagem recebida: ' + text + ' - Usuario: ' + str(chat_id))

	cursor.execute(str("SELECT EXISTS(SELECT 1 FROM public.table_user WHERE id = {} )".format(chat_id)))

	clienteExiste, = cursor.fetchone()

	cursor.execute(str("SELECT EXISTS(SELECT 1 FROM public.table_user WHERE id = {} AND name IS NULL)".format(chat_id)))

	clienteHasName, = cursor.fetchone()

	if not clienteExiste:

		cursor.execute(str("INSERT INTO public.table_user (id) VALUES ({})".format(chat_id)))

		conn.commit()

		bot.sendMessage(chat_id, "Insira o seu nome para acesso ao sistema: ")

	elif clienteHasName:

		userName = text

		print (userName)

		cursor.execute(str("UPDATE public.table_user SET name = {}, id_type_user = {} WHERE id = {}".format(str("\'{}\'".format(userName)), 1, chat_id)))

		conn.commit()

		bot.sendMessage(chat_id, '{}, seu cadastro foi realizado com sucesso! Obrigado!'.format(userName), 
			reply_markup=ReplyKeyboardMarkup(
				keyboard=[[KeyboardButton(text=u'Monitorar')], [KeyboardButton(text=u'Cancelar')]]))

	elif text == u'Monitorar':

		cursor.execute(str("UPDATE public.table_user SET monitoramento = {} WHERE id = {}".format(True, chat_id)))
		
		conn.commit()

		bot.sendMessage(chat_id, "Monitoramento ativo")

	elif text == u'Cancelar':
		
		cursor.execute(str("UPDATE public.table_user SET monitoramento = {} WHERE id = {}".format(False, chat_id)))

		conn.commit()

		bot.sendMessage(chat_id, "Monitoramento parado")

	else:
		print('Oh No!')

MessageLoop(bot,handle).run_as_thread()

print ('I am running in Telegram...')

while 1:
	conn = psycopg2.connect(host=BD_IP, port=BD_Port, database=BD_Name, user=BD_User, password=BD_Pass)

	cursor = conn.cursor()

	cursor.execute(str("SELECT EXISTS(SELECT id FROM public.table_user WHERE monitoramento = True )"))

	clienteExiste, = cursor.fetchone()

	if clienteExiste:

		cap = cv2.VideoCapture(-1)

		cursor.execute(str("SELECT id FROM public.table_user WHERE monitoramento = True"))

		idExiste, = cursor.fetchone()

		print("Monitorando" + str(idExiste))

		ret, frame = cap.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = clf.detectMultiScale(gray)

		for x, y, w, h in faces:

			cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
		
		if len(faces) > 0:

			enviar_imagem(frame, idExiste)

		cap.release()

	time.sleep(1)

cap.release()