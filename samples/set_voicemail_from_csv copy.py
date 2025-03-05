"""
This script will change the voicemail settings for a list of extensions loaded from a exported csv file, printing Time taken for each extension.
"""

import timeit
from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX
import csv
from dotenv import dotenv_values


browser = Firefox()
config = dotenv_values(".env")


def set_voicemail(row):
    e = d.extension(row["extension"])
    if not e.voicemail_mail_to:
        print(f"Setting  {e.name}: {row['mailbox']}")
        e.voicemail_mail_to = row["mailbox"]
        e.voicemail_enabled = True
    else:
        print(f"Skipping {e.name}: {e.voicemail_mail_to}")


def read_from_csv(csv_file):
    with open(csv_file) as csv_extens:
        reader = csv.DictReader(csv_extens)
        for row in reader:
            if row["mailbox"]:
                print("----------------------------------------------")
                print(f"Trying   {row['extension']}: {row['mailbox']}")
                print(
                    "Time taken   :",
                    timeit.timeit(lambda: set_voicemail(row), number=1),
                )


f = FusionPBX(browser, config["URL"], config["USER"], config["PASSWORD"])
d = f.domain("domain.com")

read_from_csv("samples/csv/extensions.csv")
