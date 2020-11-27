import datetime
import os
import pickle
import time
import tkinter as tk

import httplib2
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build

import gui


def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    while True:
        try:
            service = build('sheets', 'v4', credentials=creds)
            break
        except httplib2.ServerNotFoundError:
            err_msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Failure to connect to internet"
            print(err_msg)
            with open("debug_log.txt", "a") as f:
                f.write(err_msg+"\n")
            time.sleep(5)

    return service

def main():
    if os.path.exists("debug_log.txt"):
        os.remove("debug_log.txt")
    root = tk.Tk()
    app = gui.App(root, get_service())
    root.mainloop()

main()

