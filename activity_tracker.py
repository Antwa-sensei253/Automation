import datetime
import time
import json
import win32gui
import matplotlib.pyplot as plt

# Constants
ACTIVITIES_FILE = "activities.json"

def get_active_window_name():
    """Returns the name of the currently active window."""
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def load_activities(filepath):
    """Loads activities from a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_activities(filepath, activities):
    """Saves activities to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(activities, f, indent=4)

def add_time_entry(activities, activity_name, start_time, end_time):
    """Adds a time entry to the activities dictionary."""
    if activity_name not in activities:
        activities[activity_name] = []
    activities[activity_name].append({
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": (end_time - start_time).total_seconds()
    })

def plot_activities(activities):
    """Plots the durations of the activities over time."""
    num_activities = len(activities)
    fig, axs = plt.subplots(1, num_activities, figsize=(15, 5))

    if num_activities == 1:
        axs = [axs]

    for i, (activity_name, entries) in enumerate(activities.items()):
        durations = [entry["duration"] / 3600 for entry in entries]
        axs[i].hist(durations, alpha=0.8)
        axs[i].set_title(activity_name)
        axs[i].set_xlabel('Duration (hours)')
        axs[i].set_ylabel('Frequency')

    plt.show()

def track_activities():
    """Tracks the active window and records time spent on each activity."""
    activities = load_activities(ACTIVITIES_FILE)
    active_window_name = ""
    start_time = datetime.datetime.now() 

    try:
        while True:
            new_window_name = get_active_window_name()
            if new_window_name != active_window_name:
                if active_window_name:
                    end_time = datetime.datetime.now()
                    add_time_entry(activities, active_window_name, start_time, end_time)
                    save_activities(ACTIVITIES_FILE, activities)
                active_window_name = new_window_name
                start_time = datetime.datetime.now()
            time.sleep(1)
    except KeyboardInterrupt:
        end_time = datetime.datetime.now()
        add_time_entry(activities, active_window_name, start_time, end_time)
        save_activities(ACTIVITIES_FILE, activities)
        plot_activities(activities)

if __name__ == "__main__":
    track_activities()