#set up your config.py file in the same directory. it should looks like 
"""
api_id = 99999999
api_hash = "qwertyuiopasdfghjkl1234567890dfgh"
phone_number = "+000000000000"

python -m venv venv                     #create virtual environment

source venv/bin/activate                # for Linux/macOS
venv\Scripts\activate                   # for Windows

pip install -r requirements.txt         # install library for connecting to Telegram

py main.py                              # for run the script