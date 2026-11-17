# Test program for the Runtime Database microservice
# Run this:  python test_database.py
# It starts the Runtime Database microservice by itself, tests it, then shuts it down.
# Needs Node.js installed.

import json
import os
import shutil
import signal
import subprocess
import sys
import time
import requests

DB_URL = "http://127.0.0.1:5001/items"


def find_service_dir(name, key_file):
    # looks for the microservice in this folder, or in a folder next to this one, e.g. Runtime-Database_Microservice
    # (also works if it was downloaded as a zip and ends in -main)
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.isfile(os.path.join(tests_dir, key_file)):
        return tests_dir  # this test is inside the microservice's own folder
    parent = os.path.dirname(tests_dir)
    for folder in sorted(os.listdir(parent)):
        path = os.path.join(parent, folder)
        if folder.lower().startswith(name.lower()) and os.path.isfile(os.path.join(path, key_file)):
            return path
    raise SystemExit(f"Could not find the {name} folder. Put it in the same folder as {os.path.basename(tests_dir)}.")


SERVICE_DIR = find_service_dir("Runtime-Database_Microservice", "RuntimeDb.js")


# ---------------- Terminal output ----------------

if os.name == "nt":
    os.system("")  # turns on colors in the Windows terminal
USE_COLOR = sys.stdout.isatty()
test_number = 0
next_part = None


def color(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def part(title):
    global next_part
    next_part = title


def test(title):
    global test_number, next_part
    test_number += 1
    upcoming = f"TEST {test_number}: {title}"
    if next_part:
        upcoming = f"{next_part}  >  {upcoming}"
    print(color("\n  Next up: ", "2") + color(upcoming, "1;33"))
    input(color("  Press Enter to start...", "2"))

    if next_part:
        print("\n\n" + color("#" * 60, "1;35"))
        print(color(f"   {next_part}", "1;35"))
        print(color("#" * 60, "1;35"))
        next_part = None
    print("\n" + color("-" * 60, "36"))
    print(color(f" TEST {test_number}: {title}", "1;36"))
    print(color("-" * 60, "36"))


def result(text):
    print(color(f"  => {text}", "1;32"))


def check_rejected(status):
    if status is not None and 400 <= status < 500:
        result(f"PASS: the microservice rejected the bad input ({status}), no crash")
    else:
        print(color(f"  => UNEXPECTED: got status {status}", "1;31"))


# ---------------- Starting / stopping the microservice ----------------

def check_service():
    try:
        return requests.get(DB_URL, timeout=2).status_code
    except requests.exceptions.ConnectionError:
        return None


def start_service():
    status = check_service()
    if status == 200:
        print(color("[setup] Runtime Database microservice is already running, using that one.", "2"))
        return None
    if status is not None:
        raise SystemExit("Port 5001 is being used by something else. Stop it first.")

    if shutil.which("node") is None:
        raise SystemExit("Node.js is not installed - it's needed to run the Runtime Database microservice.")
    if not os.path.isdir(os.path.join(SERVICE_DIR, "node_modules")):
        print(color("[setup] Installing the microservice's packages (npm install)...", "2"))
        subprocess.run([shutil.which("npm"), "install"], cwd=SERVICE_DIR, check=True)

    print(color("[setup] Starting the Runtime Database microservice (node RuntimeDb.js)...", "2"))
    proc = subprocess.Popen(["node", "RuntimeDb.js"], cwd=SERVICE_DIR,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=(os.name != "nt"))
    for _ in range(30):
        if check_service() == 200:
            print(color("[setup] Runtime Database microservice is running!", "2"))
            return proc
        time.sleep(0.5)
    stop_service(proc)
    raise SystemExit("The Runtime Database microservice did not start. Try running npm start by itself to see the error.")


def stop_service(proc):
    if proc is None:
        return
    print(color("\n[setup] Shutting down the Runtime Database microservice...", "2"))
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
    else:
        os.killpg(proc.pid, signal.SIGTERM)


# ---------------- Talking to the microservice ----------------

def send(method, url, **kwargs):
    # REQUEST: send an HTTP request (POST / GET / DELETE) to the microservice
    print(color("  -> REQUEST ", "1;34") + f"  {method} {url}")
    if "json" in kwargs:
        print(f"     Body: {json.dumps(kwargs['json'])}")
    if "data" in kwargs:
        print(f"     Body: {kwargs['data']}")
    try:
        response = requests.request(method, url, timeout=5, **kwargs)
    except requests.exceptions.ConnectionError:
        print(color("  X  Could not connect to the Runtime Database microservice.", "1;31"))
        return None, None

    # RECEIVE: every endpoint sends back JSON with a "success" field
    try:
        data = response.json()
        shown = json.dumps(data, indent=2)
    except ValueError:
        data = None
        shown = "(response was an error page, not JSON - the server rejected the request)"

    code = response.status_code
    code_color = "1;32" if code < 300 else "1;33" if code < 500 else "1;31"
    print(color(f"  <- RESPONSE  {code} {response.reason}", code_color))
    for line in shown.splitlines():
        print("     " + line)
    return code, data


# ---------------- The tests ----------------

def run_tests():
    part("PART 1: NORMAL USE")

    test("Save a player")
    player = {"name": "Alex", "level": 3, "hp": 85}
    send("POST", DB_URL, json={"key": "player1", "value": player})

    test("Save some settings")
    settings = {"difficulty": "hard", "music": True}
    send("POST", DB_URL, json={"key": "settings", "value": settings})

    test("Get the player back by its key")
    status, data = send("GET", f"{DB_URL}/player1")
    if status == 200:
        result(f"Player name: {data['data']['name']}, level: {data['data']['level']}")

    test("Update the player to level 4 (save the same key again)")
    player["level"] = 4
    send("POST", DB_URL, json={"key": "player1", "value": player})
    status, data = send("GET", f"{DB_URL}/player1")
    if status == 200:
        result(f"Player level is now: {data['data']['level']}")

    test("Get every item")
    status, data = send("GET", DB_URL)
    if status == 200:
        result(f"Keys currently stored: {list(data['data'].keys())}")

    test("Delete the settings")
    send("DELETE", f"{DB_URL}/settings")

    part("PART 2: FAIL CASES (bad input)")

    test("Get an item that was deleted")
    status, _ = send("GET", f"{DB_URL}/settings")
    check_rejected(status)

    test("Delete an item that doesn't exist")
    status, _ = send("DELETE", f"{DB_URL}/ghost")
    check_rejected(status)

    test("Save with no value")
    status, _ = send("POST", DB_URL, json={"key": "broken"})
    check_rejected(status)

    test("Save with no key")
    status, _ = send("POST", DB_URL, json={"value": {"hp": 10}})
    check_rejected(status)

    test("Save with an empty body")
    status, _ = send("POST", DB_URL, json={})
    check_rejected(status)

    test("Send broken JSON")
    status, _ = send("POST", DB_URL, data='{"key": "oops", "value": ', headers={"Content-Type": "application/json"})
    check_rejected(status)

    part("PART 3: IS IT STILL RUNNING AFTER THE BAD CALLS?")

    test("Normal call after all the bad ones")
    status, data = send("GET", DB_URL)
    if status == 200:
        result(f"Yes! It still works. Keys still stored: {list(data['data'].keys())}")


print(color("\n========== Runtime Database Microservice Test ==========\n", "1"))
service = start_service()
try:
    run_tests()
finally:
    stop_service(service)
print(color("\n========== Done testing Runtime Database microservice ==========", "1"))
