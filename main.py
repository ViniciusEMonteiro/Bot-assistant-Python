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

from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import matplotlib.pyplot as plt
from array import array
import numpy as np

confirmFlag = None
userName = None
chat_id = None
text = None