# This repository is now archived
It is no longer supported/updated, but the tracker may still work.

See CTM's amazing All Advancements tool for a better experience (and more supported versions): https://github.com/DarwinBaker/AATool

## Minecraft All Advancements 1.17 Tracker Spreadsheet

Connects to a [Google Sheets](https://docs.google.com/spreadsheets/d/1Pz3v74yC1BZVO2wZtmu13JF9cDcMVkm-NbD9mvoGNlE) spreadsheet, which is updated as advancements are achieved.

## Minecraft All Advancements 1.16.1-1.16.4 Tracker Spreadsheet

Connects to a [Google Sheets](https://docs.google.com/spreadsheets/d/1IsXHUT_P8Qd6SmHQ5gD190n4d2gNceJZZpAjimH928M) spreadsheet, which is updated as advancements are achieved.

## Spreadsheet Info

This allows you to share a link to the spreadsheet so that others can see your progress in real-time.
If you have a second monitor, then you can have this spreadsheet open there, for your planning.
Otherwise you could also have the spreadsheet open on your phone, to view your progress.

Note: the progress only updates when the game is saved or paused.

### To run

See the [youtube walkthrough and demo](https://youtu.be/RamvJtxFHx0) or follow the steps below.

* Copy the [google sheets spreadsheet](https://docs.google.com/spreadsheets/d/1IsXHUT_P8Qd6SmHQ5gD190n4d2gNceJZZpAjimH928M) to your Google Drive: File -> Make a copy
* **Important Note**: this step is different compared to the video as Google changed the process. Follow the instructions in the linked PDF: Enable the [Google Sheets API](https://github.com/UnlucksMcGee/minecraft_all_advancements_tracker/blob/main/GoogleSheetsAPI-Instructions.pdf) for your Google account and download the `credentials.json` file.

* Download the [Version for Minecraft 1.17](https://github.com/UnlucksMcGee/minecraft_all_advancements_tracker/releases/tag/V2.0) or the older [Version for Minecraft 1.16.1-1.16.4](https://github.com/UnlucksMcGee/minecraft_all_advancements_tracker/releases/tag/V1.1) for your operating system.
* Change the `settings.txt` file with the sheet ID of the spreadsheet copy in your Google Drive.
* Double click the main application to launch it.
* The first time you run the application, it will open up your browser where you authenticate the API enabled above, to generate a token which is saved to `token.pickle` file.

### Troubleshooting

If the application fails to launch. Make sure you have `credentials.json` in the same directory, as well as `settings.txt` updated to the correct sheet ID and Minecraft directory location (if needed). Delete the `token.pickle` file so that it will be generated again.

### To build to EXE

* `pyinstaller run.py --name "MC AA Tracker" --onefile --windowed --icon icon.ico`
