"""
This program resets a sandbox, creates a webview, asks a user to login to
that webview, retrieves the locks they own, unlocks and relocks a lock.
"""
from seamapi import Seam
from dotenv import load_dotenv
from examples.utils import bcolors, yes_strings
from pprint import pprint
import sys

load_dotenv()

if input("This will reset your workspace sandbox, continue? (Y/n) ") not in yes_strings:
    raise Exception("Stopped by user")

seam = Seam()

print("Reseting sandbox...")
seam.workspaces.reset_sandbox()

print("Creating a Connect Webview...")
webview = seam.connect_webviews.create(accepted_providers=["august"])

print("This is my webview:")
pprint(webview)

print(
    bcolors.OKCYAN
    + f"\nGo to the URL below and login\n\n{webview.url}\n\n\tjane@example.com\n\t1234\n\n"
    + bcolors.ENDC
)

input("Press enter when you're done:")

updated_webview = seam.connect_webviews.get(webview.connect_webview_id)

print("This is my updated webview:")
pprint(updated_webview)

if updated_webview.login_successful:
    print(bcolors.OKGREEN + "Successfully logged in!" + bcolors.ENDC)
else:
    print(
        bcolors.FAIL
        + "\nWebview wasn't logged in, did you forget to log in?\n"
        + bcolors.ENDC
    )
    sys.exit(1)


print("Listing all the connected locks for our new account:")
locks = seam.locks.list()
pprint(locks)

# We can probably replace this with seam.locks.get and a filter
garage_lock = next(
    lock
    for lock in locks
    if lock.properties["august_metadata"]["lock_name"] == "GARAGE"
)

print(f"GARAGE LOCK LOCKED: {garage_lock.properties['locked']}")

print("Locking garage_lock...")
seam.locks.lock_door(garage_lock)

print("Getting updated garage lock...")
updated_garage_lock = seam.locks.get(garage_lock)

print(
    bcolors.OKGREEN
    + f"GARAGE LOCK LOCKED: {updated_garage_lock.properties['locked']}"
    + bcolors.ENDC
)
