# Minecraft All Advancements 1.16.1-1.16.4 Tracker

Connects to a [Google Sheets](https://docs.google.com/spreadsheets/d/1IsXHUT_P8Qd6SmHQ5gD190n4d2gNceJZZpAjimH928M) spreadsheet, which is updated as advancements are achieved.

This allows you to share a link to the spreadsheet so that others can see your progress in real-time.
If you have a second monitor, then you can have this spreadsheet open there, for your planning.
Otherwise you could also have the spreadsheet open on your phone, to view your progress.

# To run:
* Copy the [google sheets spreadsheet](https://docs.google.com/spreadsheets/d/1IsXHUT_P8Qd6SmHQ5gD190n4d2gNceJZZpAjimH928M) to your Google Drive: File -> Make a copy
* Enable the [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) for your Google account and download the `credentials.json` file.

* Change the `settings.txt` file with the sheet ID of the spreadsheet copy in your Google Drive.
* ```python
python run.py
```

