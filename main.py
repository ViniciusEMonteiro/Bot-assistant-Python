import telepot
import time
import sqlite3
import json
import socket
import sys
import datetime
import thread
import pyaudio
import struct
import ConfigParser
import psycopg2

from telepot.loop import MessageLoop
from configparser import ConfigParser
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import matplotlib.pyplot as plt
from array import array
import numpy as np

confirmFlag = None
userName = None
chat_id = None
text = None

config_file = ConfigParser()
config_file.read('config')

Bot_Name=config_file.get('Develop configuration','Bot_Name')
Bot_hash=config_file.get('Develop configuration', 'Bot_hash')
BD_IP=config_file.get('Develop configuration', 'BD_IP')
BD_Port=config_file.get('Develop configuration', 'BD_Port')
BD_Name=config_file.get('Develop configuration', 'BD_Name')
BD_User=config_file.get('Develop configuration', 'BD_User')
BD_Pass=config_file.get('Develop configuration', 'BD_Pass')

print ("Let's started... My name is " + Bot_Name)

#bot = telepot.Bot(Bot_hash)

conn = None

try:
	print('Connecting to the PostgreSQL database...')
	conn = psycopg2.connect(host=BD_IP, port=BD_Port, database=BD_Name, user=BD_User, password=BD_Pass)

	cursor = conn.cursor()

	cursor.execute("""CREATE TABLE IF NOT EXISTS public.table_user (id serial PRIMARY KEY NOT NULL,Nome TEXT,id_type_user INT);""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS public.table_type_user (id serial PRIMARY KEY NOT NULL,Name TEXT);""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS public.table_service (id serial PRIMARY KEY NOT NULL,Name TEXT,help TEXT,Host TEXT,port INT,id_type_service INT,token TEXT);""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS public.table_type_service (id serial PRIMARY KEY NOT NULL,Name TEXT);""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS public.table_request (id serial PRIMARY KEY NOT NULL,Name TEXT,id_service INT,path TEXT,NumberParans INT,NameParans TEXT,TypeParans TEXT);""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS public.table_alias (id serial PRIMARY KEY NOT NULL,Name TEXT,id_user INT,id_request INT,DefaultMessage TEXT);""")

	cursor.close()

except (Exception, psycopg2.DatabaseError) as error:
    print('ERRO: ') 
    print(error)

def handle(msg):
	global userName, chat_id, text, confirmFlag


#MessageLoop(bot,handle).run_as_thread()

print ('I am running in Telegram...')