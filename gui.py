import datetime
import json
import os
import sys
import time
import tkinter as tk
from functools import partial

import googleapiclient
import httplib2

import sheet_links_1_17 as sheet_links


def configure_window(master, title="Python Application", width=600, height=600, resizable=True, centred=True, bg=None):
    master.title(title)

    if centred:
        s_width = master.winfo_screenwidth()
        s_height = master.winfo_screenheight()
        x = (s_width - width)//2
        y = (s_height - height)//2
        master.geometry('%dx%d+%d+%d' % (width, height, x, y))
    else:
        master.geometry('{}x{}'.format(width, height))

    if not resizable:
        master.resizable(width=False, height=False)
    
    if bg is not None:
        master.configure(bg=bg)

class App:
    def __init__(self, master, service):
        self.master = master
        self.col_txt_primary = "#F6F7F8"
        self.col_bg = "#011627"
        self.col_fg = "#70A288"
        self.font_l = ("Arial", 12, "bold")
        self.font_s = ("Arial", 10)

        self.gsheets = service.spreadsheets().values()
        self.saves_dir = None
        self.sheet_id = None
        self.last_modified_time = None

        configure_window(master=self.master, title="Minecraft All Advancements 1.17 Tracker", width=700, height=200, resizable=True, centred=True, bg=self.col_bg)

        output_frame = tk.Frame(self.master, borderwidth=2, bg=self.col_fg, relief=tk.SUNKEN)
        output_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1, anchor=tk.N, padx=10, pady=10)

        self.status = tk.StringVar(self.master)
        self.status.set("Loading...")
        output_label = tk.Label(output_frame, textvariable=self.status, font=self.font_l, bg=self.col_fg)
        output_label.pack(anchor="n", padx=5, pady=5)

        minecraft_directory = ""
        if sys.platform == "linux" or sys.platform == "linux2":
            # linux
            minecraft_directory = os.path.expanduser("~") + "/.minecraft"
        elif sys.platform == "darwin":
            # OS X
            minecraft_directory = os.path.expanduser("~") + "/Library/Application Support/minecraft"
        elif sys.platform == "win32":
            # Windows
            minecraft_directory = os.getenv('APPDATA') + "\\.minecraft"

        if not os.path.exists("settings.txt"):
            # Write settings
            self.status.set("Can't find settings file. Created default to be fixed.")
            with open("settings.txt", "w") as settings:
                settings.write("SHEET_ID = abcDEFghiJKLmnoPQRstuVWXz1234567890abcDEFghi\n")
                settings.write("# Uncomment the below line if you're using a different default minecraft directory.\n")
                settings.write("# MINECRAFT_APPDATA_DIRECTORY = \\path\\to\\.minecraft\n")
            input() # temporary pause
            sys.exit(1)

        # Read settings
        with open("settings.txt", "r") as settings:
            lines = settings.readlines()
            for line in lines:
                line = line.strip()
                if len(line) == 0 or line[0] == "#":
                    continue

                if len(line.split("=", 1)) < 2:
                    self.status.set(f"Couldn't parse settings option: {line}")
                    continue
                category = line.split("=", 1)[0].strip()
                data = line.split("=", 1)[1].strip()
                # Remove enclosing quotes
                if data[0] == '"' and data[-1] == '"':
                    data = data[1:-1]

                if category == "SHEET_ID":
                    self.sheet_id = data
                    self.status.set(f"SHEET_ID = {data}")
                elif category == "MINECRAFT_APPDATA_DIRECTORY":
                    minecraft_directory = data
                    self.status.set(f"MINECRAFT_APPDATA_DIRECTORY = {data}")

        if not os.path.basename(os.path.normpath(minecraft_directory)) == "saves":
            minecraft_directory = os.path.join(minecraft_directory,"saves")

        with open("debug_log.txt", "a") as f:
            f.write(f"Using saves directory: {minecraft_directory}\n")
        self.saves_dir = minecraft_directory

        if self.sheet_id is None:
            print("Settings file does not set SHEET_ID.")
            sys.exit(1)

        if not os.path.exists(self.saves_dir):
            err_msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Minecraft saves directory does not exist: {self.saves_dir}.\nMake sure to edit settings.txt to point to your minecraft installation directory."
            print(err_msg)
            with open("debug_log.txt", "a") as f:
                f.write(err_msg+"\n")
            sys.exit(1)
        
        self.master.after(100, self.update_data)

    def update_data(self):
        savename, data = self.get_current_advancement_progress()
        if data is not None:
            try:
                self.gsheets.batchUpdate(spreadsheetId=self.sheet_id,body={'valueInputOption': "USER_ENTERED","data":data}).execute()
                self.status.set(f"{savename}\n Last Updated at: {datetime.datetime.now().strftime('%I:%M:%S %p')}")
            except (ConnectionResetError, httplib2.ServerNotFoundError):
                err_msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Failure to connect to internet"
                print(err_msg)
                self.status.set(err_msg)
                with open("debug_log.txt", "a") as f:
                    f.write(err_msg+"\n")
                self.last_modified_time = None
                self.master.after(5000, self.update_data) # Try again in 5 seconds
                return
            except googleapiclient.errors.HttpError:
                err_msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Refused access to the Google Sheet ID provided.\nMake sure it is correct in settings.txt"
                print(err_msg)
                self.status.set(err_msg)
                with open("debug_log.txt", "a") as f:
                    f.write(err_msg+"\n")
                self.last_modified_time = None
                self.master.after(5000, self.update_data) # Try again in 5 seconds
                return
        self.master.after(1000, self.update_data)

    def get_reset_spreadsheet_data(self):
        data=[]    
        for k in sheet_links.links.keys():
            for _,v in sheet_links.links[k].items():
                data.append({'range':v,"values":[["FALSE"]]})
        return data

    def get_current_advancement_progress(self):
        all_saves = [os.path.join(self.saves_dir,d) for d in os.listdir(self.saves_dir) if os.path.isdir(os.path.join(self.saves_dir,d))]
        # print(all_saves)

        if all_saves:
            latest_save = max(all_saves, key=os.path.getmtime) # Get latest modified save
            savename = os.path.basename(latest_save)
            # print(latest_save)
        else:
            self.status.set("No savegame found")
            return "No savegame found", None

        if self.last_modified_time is not None and self.last_modified_time < os.path.getmtime(latest_save):
            self.last_modified_time = os.path.getmtime(latest_save)
        elif self.last_modified_time is None:
            self.last_modified_time = os.path.getmtime(latest_save)
        else:
            # No update
            return savename, None

        if not os.path.exists(os.path.join(latest_save,"advancements")):
            self.status.set("No advancements found. \nWorld still generating, or using old MC version.")
            return savename, None

        json_files = sorted([os.path.join(latest_save,"advancements",f) for f in os.listdir(os.path.join(latest_save,"advancements")) if os.path.isfile(os.path.join(latest_save,"advancements",f))])

        if len(json_files) > 1:
            msg = f"More than one advancement json file found: {json_files}. Using the first one."
            print(msg)
            with open("debug_log.txt", "a") as f:
                f.write(msg+"\n")
            json_path = json_files[0]
        elif len(json_files) == 0:
            self.status.set("No advancement json file found")
            return savename, None
        else:
            json_path = json_files[0]

        parsed_json = json.load(open(json_path,"r"))

        if not (sheet_links.advancements_dataversion_min <= parsed_json["DataVersion"] <= sheet_links.advancements_dataversion_max):
            self.status.set("Invalid Version used. Try 1.17+")
            return "Invalid Version used. Try 1.17+", None

        data = []
        
        advancements_sections = ["advancements_minecraft", "advancements_husbandry", "advancements_adventure", "advancements_nether", "advancements_end"]
        for cur_section in advancements_sections:
            for k,v in sheet_links.links[cur_section].items():
                completed = "FALSE"
                if k in parsed_json and parsed_json[k]["done"] == True:
                    completed = "TRUE"
                data.append({'range':v,"values":[[completed]]})

        progress_sections = ["minecraft:husbandry/bred_all_animals", "minecraft:husbandry/complete_catalogue", "minecraft:husbandry/balanced_diet", "minecraft:adventure/kill_all_mobs", "minecraft:adventure/adventuring_time", "minecraft:nether/explore_nether"]
        for cur_section in progress_sections:
            for k,v in sheet_links.links[cur_section].items():
                completed = "FALSE"
                if cur_section in parsed_json and k in parsed_json[cur_section]["criteria"]:
                    completed = "TRUE"
                data.append({'range':v,"values":[[completed]]})

        # Auto-tick the piglin brute if using verison prior to 1.16.2
        if parsed_json["DataVersion"] < sheet_links.advancements_dataversion_piglin_brute_addition:
            data.append({'range':sheet_links.links["minecraft:adventure/kill_all_mobs"]["minecraft:piglin_brute"],"values":[["TRUE"]]})

        return savename, data
