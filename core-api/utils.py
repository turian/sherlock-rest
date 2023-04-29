import json
import os
import subprocess
import sys
import time

from django.conf import settings

BASE_DIR = settings.BASE_DIR


def check_socialnetwork_availability(names):
    """This function takes in a list of names and return the
    list of socila network each of those names has been used
    as username, it return list of linkin a json file.
    It uses sherlock for tracking names and uses subprocess
    to interact with sherlock."""
    start_time = time.time()
    results = {}

    output_file = f"{names[0]}_name.json"

    directory = os.path.join(BASE_DIR, "sherlock/sherlock/sherlock.py")
    print(directory)
    for name in names:
        command = f"{sys.executable} {directory} {name} --print-found"

        output = subprocess.check_output(command, shell=True, text=True)

        results[name] = output.splitlines()
    end_time = time.time()
    time_taken = end_time - start_time

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    print(time_taken)

    # Alternative method, using sherlock's provided way of
    # running query on multiple names.

    # results = {}
    # output_file = f"{names[0]}_name.json"
    # directory = os.path.join(BASE_DIR, "sherlock/sherlock/sherlock.py")
    # names = " ".join(str(name) for name in names)
    # command = f"{sys.executable} {directory} {names} --print-found"
    # output = subprocess.check_output(command, shell=True, text=True)
    # results = output.splitlines()

    # with open(output_file, "w") as f:
    #     json.dump(results, f, indent=4)
