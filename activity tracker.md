# Activity Tracker Documentation

## Overview

The Activity Tracker is a Python script designed to monitor and log the active window on a user's computer, recording the time spent on each activity. This data is stored in a JSON file and can be visualized using matplotlib.

## Dependencies

Ensure the following Python packages are installed:

- `datetime`
- `time`
- `json`
- `pywin32` (specifically `win32gui`)
- `matplotlib`

You can install the required packages using pip:

```sh
pip install pywin32 matplotlib


## Constants

- `ACTIVITIES_FILE`: The filename for storing activity data. Default is `"activities.json"`.

## Functions

### `get_active_window_name()`

Returns the name of the currently active window.


def get_active_window_name():
    """Returns the name of the currently active window."""
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

### `load_activities(filepath)`


Loads activities from a JSON file. If the file does not exist or contains invalid JSON, it returns an empty dictionary.

def load_activities(filepath):
    """Loads activities from a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


### `save_activities(filepath, activities)`

Saves the activities dictionary to a JSON file.

def save_activities(filepath, activities):
    """Saves activities to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(activities, f, indent=4)


### `add_time_entry(activities, activity_name, start_time, end_time)`

Adds a time entry for a specific activity to the activities dictionary.

def add_time_entry(activities, activity_name, start_time, end_time):
    """Adds a time entry to the activities dictionary."""
    if activity_name not in activities:
        activities[activity_name] = []
    activities[activity_name].append({
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": (end_time - start_time).total_seconds()
    })



### `plot_activities(activities)`

Plots the durations of the activities over time using matplotlib.

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



### `track_activities()`

Tracks the active window and records the time spent on each activity. Saves data periodically and plots the results when interrupted.

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


## Running the Script

To run the Activity Tracker, execute the script from the command line:


python activity_tracker.py

