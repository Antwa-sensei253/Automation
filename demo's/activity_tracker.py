from __future__ import print_function

import datetime
import time
import json
import win32gui

import matplotlib.pyplot as plt
from dateutil import parser
import uiautomation as auto

ALPHA = 0.8
SECONDS_PER_HOUR = 3600
ACTIVITIES_FILE = "activities.json"
JSON_DUMP_PARAMS = {"indent": 4, "sort_keys": True}


class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {
            "name": self.name,
            "time_entries": [time.serialize() for time in self.time_entries]
        }


class TimeEntry:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time

    def _get_specific_times(self):
        days, seconds = self.total_time.days, self.total_time.seconds
        self.hours = days * 24 + seconds // SECONDS_PER_HOUR
        self.minutes = (seconds % SECONDS_PER_HOUR) // 60
        self.seconds = seconds % 60

    def serialize(self):
        self._get_specific_times()
        return {
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "days": self.total_time.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds
        }


class ActivityList:
    def __init__(self):
        self.activities = []

    def initialize(self, filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                self.activities = [Activity(activity["name"],
                                            self._get_time_entries_from_json(activity))
                                   for activity in data["activities"]]
        except FileNotFoundError:
            print("No JSON file found. Creating a new file...")
            self._create_empty_json(filepath)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON data in activities.json. Creating a new file...")
            self._create_empty_json(filepath)

    def _create_empty_json(self, filepath):
        with open(filepath, "w") as f:
            json.dump({"activities": []}, f, **JSON_DUMP_PARAMS)

    def _get_time_entries_from_json(self, data):
        return [TimeEntry(parser.parse(entry["start_time"]),
                          parser.parse(entry["end_time"]))
                for entry in data["time_entries"]]

    def serialize(self):
        return {
            "activities": [activity.serialize() for activity in self.activities]
        }

    def plot_activities(self):
        num_activities = len(self.activities)
        fig, axs = plt.subplots(1, num_activities, figsize=(15, 5))
        for i, activity in enumerate(self.activities):
            all_durations = [entry.total_time.total_seconds() / SECONDS_PER_HOUR
                             for entry in activity.time_entries]
            axs[i].hist(all_durations, alpha=ALPHA)
            axs[i].set_title(activity.name)
            axs[i].set_xlabel('Duration (hours)')
            axs[i].set_ylabel('Frequency')
        plt.show()


def url_to_name(url):
    string_list = url.split("/")
    return string_list[2]


def get_active_window_name():
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    return active_window_name


def get_chrome_url():
    window = win32gui.GetForegroundWindow()
    chrome_control = auto.ControlFromHandle(window)
    edit = chrome_control.EditControl()
    return f"https://{edit.GetValuePattern().Value}"


ACTIVE_WINDOW_NAME = ""
ACTIVITY_NAME = ""
START_TIME = datetime.datetime.now()
ACTIVE_LIST = ActivityList()
FIRST_TIME = True

# Create an instance of ActivityList and initialize it with data from the JSON file
activity_list = ActivityList()
activity_list.initialize(ACTIVITIES_FILE)

try:
    try:
        while True:
            previous_site = ""
            new_window_name = get_active_window_name()

            if "Google Chrome" in new_window_name:
                new_window_name = url_to_name(get_chrome_url())

            if ACTIVE_WINDOW_NAME != new_window_name:
                print(ACTIVE_WINDOW_NAME)
                ACTIVITY_NAME = ACTIVE_WINDOW_NAME

                if not FIRST_TIME:
                    end_time = datetime.datetime.now()
                    time_entry = TimeEntry(START_TIME, end_time)
                    time_entry._get_specific_times()

                    exists = False
                    for activity in ACTIVE_LIST.activities:
                        if activity.name == ACTIVITY_NAME:
                            exists = True
                            activity.time_entries.append(time_entry)

                    if not exists:
                        activity = Activity(ACTIVITY_NAME, [time_entry])
                        ACTIVE_LIST.activities.append(activity)
                    with open(ACTIVITIES_FILE, "w") as json_file:
                        json.dump(ACTIVE_LIST.serialize(), json_file,
                                  **JSON_DUMP_PARAMS)
                FIRST_TIME = False
                ACTIVE_WINDOW_NAME = new_window_name
                START_TIME = datetime.datetime.now()

            time.sleep(1)
    finally:
        # Plot the activities at the end of the script, after the loop has finished
        activity_list.plot_activities()
except KeyboardInterrupt:
    with open(ACTIVITIES_FILE, "w") as json_file:
        json.dump(ACTIVE_LIST.serialize(), json_file, **JSON_DUMP_PARAMS)
