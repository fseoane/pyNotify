#!/bin/bash

mkdir -p .env 
python -m venv .env
source .env/bin/activate

python -m pip install --requirement requirements.req 

pyinstaller --onefile --windowed --icon notification.svg --upx-dir /usr/bin/ pyNotify.py

deactivate
