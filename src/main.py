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
    now = datetime.now()
    
    # 1. Get timestamp with exactly 3 decimal places (milliseconds)
    # This results in a string like "1737604359.123"
    ts_str = f"{now.timestamp():.3f}"
    
    # 2. Remove the dot to get your "string of numbers"
    # Result: "1737604359123"
    DTN_UNIX = ts_str.replace('.', '')
    
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    
    default_save = {
        "balance": 100,
        "datestamps": {
            "last_played": formatted_date,
            "created_on": formatted_date
        },
        "metadata" : {
            "HardwareID": HARDWARE_ID,
            "DTN": DTN_UNIX, # Now includes milliseconds safely
            "Hash" : None
        }
    }

    # Generate the hash using the exact same DTN_UNIX
    hash_input = f'{default_save["balance"]}!{HARDWARE_ID}!{DTN_UNIX}'
    default_save["metadata"]["Hash"] = hashlib.sha256(hash_input.encode()).hexdigest()

    # Generate filename
    save_file_id = hashlib.sha256((HARDWARE_ID + DTN_UNIX).encode()).hexdigest()[:20]
    save_file_name = f'PyCasino_{save_file_id}.json'
    
    SAVE_FILE_PATH = os.path.join(SAVES_FOLDER_PATH, save_file_name)
    with open(SAVE_FILE_PATH, 'w') as f:
        json.dump(default_save, f, indent=4)

def verify_save(save_file):
    SAVE_FILE_PATH = os.path.join(SAVES_FOLDER_PATH, save_file)
    with open(SAVE_FILE_PATH, 'r') as f:
        save_data = json.load(f)
        
    HARDWARE_ID = str(uuid.getnode())
    check_str = f'{str(save_data["balance"])}!{HARDWARE_ID}!{save_data["metadata"]["DTN"]}'
    expected_hash = hashlib.sha256(check_str.encode()).hexdigest()
    
    is_valid = expected_hash == save_data["metadata"]["Hash"]

    # Return a dictionary so JS can read "result.success" and "result.data"
    return {
        "success": is_valid,
        "data": save_data if is_valid else None,
        "message": "Verification successful" if is_valid else "Hash mismatch"
    }

def initialize_game():
    window = pywebview.create_window("PyCasino", UIPATH, width=800, height=600)
    window.expose(fetch_saves, load_settings, create_save_file, verify_save)
    pywebview.start(gui='qt')

if __name__ == "__main__":
    initialize_game()
