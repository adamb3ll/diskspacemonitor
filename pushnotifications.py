"""Sends notification using pushover or prowl"""

#import shutil
#import sys
import os
from collections import namedtuple
import requests

def read_pushover_settings(filename):
    """Attempt to read push over settings"""
    PushOverSettings = namedtuple('PushOverSettings', ['apptoken', 'userkey'])
    try:
        currentdir = os.getcwd()
        apptoken = ""
        userkey = ""
        with open(currentdir + "/" + filename, 'r') as file:
            apptoken = file.readline().rstrip('\n')
            userkey = file.readline().rstrip('\n')
        settings = PushOverSettings(apptoken, userkey)
        return settings
    except IOError:
        pass

def read_prowl_settings(filename):
    """Attempt to read prowl settings"""
    ProwlSettings = namedtuple('ProwlSettings', ['apikey'])
    try:
        currentdir = os.getcwd()
        apikey = ""
        with open(currentdir + "/" + filename, 'r') as file:
            apikey = file.readline().rstrip('\n')
        settings = ProwlSettings(apikey)
        return settings
    except IOError:
        pass

def send_notification_with_pushover(app_token, user_key, event, message):
    """Tell the phone"""
    files = {
        'token': (None, app_token),
        'user': (None, user_key),
        'title': (None, event),
        'message': (None, message),
    }

    requests.post('https://api.pushover.net/1/messages.json', files=files)

def send_notification_with_prowl(apikey, event, message):
    """Tell the phone"""
    files = {
        'apikey': (None, apikey),
        'application': (None, event),
        'event': (None, ""),
        'description': (None, message),
    }

    requests.post('https://api.prowlapp.com/publicapi/add', files=files)

def push_notification(event, message):
    notification_system = "none"
    notify_settings = read_pushover_settings("pushover.txt")
    if hasattr(notify_settings, "apptoken"):
        notification_system = "pushover"
    else:
        notification_system = "prowl"
        notify_settings = read_prowl_settings("prowl.txt")

    if notification_system == "pushover":
        send_notification_with_pushover(notify_settings.apptoken, notify_settings.userkey, event, message)
    elif notification_system == "prowl":
        send_notification_with_prowl(notify_settings.apikey, event, message)
    else:
        print("No notifications configured")
