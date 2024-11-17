#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

pip install python-dotenv
pip install aiogram
pip install google-api-python-client

# Запускаем основной скрипт
python3 main.py