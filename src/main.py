import os
import sys
import json
import hashlib
import random
import webview as pywebview
import PyQt5
import uuid
import datetime

from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets

USER_APPDATA_FOLDER = os.getenv('APPDATA')
APPDATA_PYCASINO_PATH = os.path.join(USER_APPDATA_FOLDER, 'PyCasino')
PYCASINO_STORAGE_PATH = os.path.join(APPDATA_PYCASINO_PATH, 'data')
SETTINGS_FILE_PATH = os.path.join(PYCASINO_STORAGE_PATH, 'settings.json')
SAVES_FOLDER_PATH = os.path.join(PYCASINO_STORAGE_PATH, 'saves')

UIPATH = "./ui/index.html"

if not os.path.exists(APPDATA_PYCASINO_PATH):
    os.makedirs(APPDATA_PYCASINO_PATH)
if not os.path.exists(PYCASINO_STORAGE_PATH):
    os.makedirs(PYCASINO_STORAGE_PATH)
if not os.path.exists(SAVES_FOLDER_PATH):
    os.makedirs(SAVES_FOLDER_PATH)

def load_settings():
    if not os.path.exists(SETTINGS_FILE_PATH):
        settings = {
            "volume": 50,
            "language": "en",
        }
        with open(SETTINGS_FILE_PATH, 'w') as f:
            json.dump(settings, f)

    with open(SETTINGS_FILE_PATH, 'r') as f:
        settings = json.load(f)

    return settings

def fetch_saves():
    if not os.path.exists(SAVES_FOLDER_PATH):
        os.makedirs(SAVES_FOLDER_PATH)

    if not os.listdir(SAVES_FOLDER_PATH):
        create_save_file()

    save_files = [f for f in os.listdir(SAVES_FOLDER_PATH) if f.endswith('.json')]
    return save_files

def create_save_file():
    HARDWARE_ID = str(uuid.getnode())
    DATETIME_NOW = datetime.now()
    DATETIME_UNIX = str(datetime.now().timestamp()).replace('.', '')
    
    default_save = {
        "balance": 100,
        "datestamps": {
            "last_played": str(DATETIME_NOW.strftime("%Y-%m-%d %H:%M:%S")),
            "created_on": str(DATETIME_NOW.strftime("%Y-%m-%d %H:%M:%S"))
        },
        "metadata" : {
            "HardwareID": HARDWARE_ID,
            "DTN": DATETIME_UNIX,
            "Hash" : None
        }
    }

    default_save["metadata"]["Hash"] = hashlib.sha256((f'{str(default_save["balance"])}!{HARDWARE_ID}!{default_save["metadata"]["DTN"]}').encode()).hexdigest()

    save_file_id = hashlib.sha256((HARDWARE_ID + DATETIME_UNIX).encode()).hexdigest()[:20]

    save_file_name = f'PyCasino_{save_file_id}.json'
    SAVE_FILE_PATH = os.path.join(SAVES_FOLDER_PATH, save_file_name)
    with open(SAVE_FILE_PATH, 'w') as f:
        json.dump(default_save, f)

def initialize_game():
    window = pywebview.create_window("PyCasino", UIPATH, width=800, height=600)
    window.expose(fetch_saves, load_settings)
    pywebview.start(gui='qt')

if __name__ == "__main__":
    initialize_game()
