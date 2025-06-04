# Formula V Qualifying Server

This project has been made for Formula V to fetch the qualifying data live for our streams. The default icons are used from the Formula V Discord server's emojis, you may change these if you want to use it for yourself, just keep in mind that the "team" of a driver has to equal to the icon name. 

### Setup:
1. Install python 3.13 or higher (https://www.python.org/downloads/)
    - You might have to restart your pc after installation
2. Create a file called `.env` inside the folder
3. Setup the required valuables:
    ```
    ONEDRIVE_LINK=the public view link to the spreadsheet
    REFRESH_INTERVAL=how often you want refreshing
    SHEET_NAME=name of the sheet
    LOCAL_PORT=the local port you want the app to run on
    ```
    You can see an example configuration at the end of the document
4. Install dependencies:
    ```bat
    pip install -r requirements.txt
    ```
5. Start the app:
    ```
    python main.py
    ```
6. That's it! You can now test the app manually if you open your browser and go to `http://127.0.0.1:{your port here}`

### OBS overlay:
1. Create a new **Browser** source inside OBS
2. Set the URL to `http://127.0.0.1:{your port here}`
3. Set the correct width and height, whatever works for you
4. Click refresh and you should be able to see the data once it's loaded in

### Example config:
This is the Formula V S14 spreadsheet it is quite heavy (47.6MB as of right now) so for testing i would advise you not to use this.
```
ONEDRIVE_LINK=https://1drv.ms/x/c/9c4419a56c87af87/EeGS-7ifYeZMmBEuwePw4isBNTC79SLv--PKTPnrOE5uew?e=F8pwfO
REFRESH_INTERVAL=10
SHEET_NAME=F1_R1
LOCAL_PORT=4258
```