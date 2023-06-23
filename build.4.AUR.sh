#!/bin/bash

mkdir -p .env 
python -m venv .env
source .env/bin/activate

# python  -m pip install --upgrade pip setuptools wheel

# python -m pip cache purge

# python -m pip install gotify[stream]
# python -m pip install pyinstaller
# python -m pip install pygame
# python -m pip install pygobject
# python -m pip install asyncio
# python -m pip install pystray
# python -m pip install pillow
# python -m pip install psutil

python -m pip install --requirement requirements.req 

pyinstaller --onefile --windowed pyNotify.py

deactivate
#rm -rf .env