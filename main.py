import time
import threading
from flask import Flask, render_template
import requests
from io import BytesIO
import openpyxl
from openpyxl.utils import range_boundaries
import os
import sheets
import datetime

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

ONEDRIVE_LINK = os.getenv("ONEDRIVE_LINK")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL"))
SHEET_NAME = os.getenv("SHEET_NAME")
CELL_RANGE = "AS6:AW25"
LOCAL_PORT=os.getenv("LOCAL_PORT")

latest_data = [['Bruder', 'ALP', '01:10.977', ''], ['MrSpooky', 'MCL', '01:11.520', '+0.542'], ['MrTino', 'HAA', '01:11.552', '+0.574'], ['TDash', 'RED', '01:11.563', '+0.586'], ['SkillMax', 'RCB', '01:11.586', '+0.609'], ['Stappen (LANCE_STROLL)', 'AST', '01:11.610', '+0.633'], ['MrBryan', 'MCL', '01:11.298', '+0.321'], ['Jacob', 'RCB', '01:11.732', '+0.754'], ['Bebricki', 'SAU', '01:11.883', '+0.905'], ['Crispy', 'MER', '01:11.886', '+0.909'], ['Acid_Ibis', 'RED', '01:11.928', '+0.951'], ['Marshall (Russian_Dlr)', 'ALP', '01:11.934', '+0.956'], ['BlueShay', 'WIL', '01:12.213', '+1.236'], ['Tifosi (xF13NDx)', 'SAU', '01:12.287', '+1.310'], ['Ch1LLpeper', 'MER', '01:12.490', '+1.513'], ['danyawarfov', 'FER', '01:12.631', '+1.654'], ['MelihVR', 'FER', '01:12.670', '+1.693'], ['Versa', 'HAA', '01:14.290', '+3.313'], ['Enoruwa', 'AST', '', ''], ['F4RM1LA', 'WIL', '', '']]

def update_loop():
    global latest_data
    while True:
        print("Refreshing data...")
        file = sheets.download_excel(sheets.convert_onedrive_link(ONEDRIVE_LINK))
        if file:
            latest_data = sheets.read_range(file, SHEET_NAME, CELL_RANGE)
        print(f"Latest data: {latest_data}")
        time.sleep(REFRESH_INTERVAL)

@app.route("/")
def index():
    global latest_data
    if latest_data is None:
        data = []
    else:
        data = latest_data
    return render_template("index.html", data=data)

import warnings
warnings.simplefilter("ignore", UserWarning)

def main():
    threading.Thread(target=update_loop, daemon=True).start()
    app.run(debug=False, port=LOCAL_PORT)
    print(f"Running on http://localhost:{LOCAL_PORT}")

if __name__ == "__main__":
    main()