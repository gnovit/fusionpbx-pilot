import timeit


from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX
import csv

browser = Firefox()
# wdw = WebDriverWait(browser, 10)
url = "http://45.79.223.247"
user = "admin"
password = "S3nh4C0mpl3x4$"

extens = []


def do_thing(row):
    e = f.domain.extension(row["extension"])
    if not e.voicemail_mail_to:
        print(f"Setting  {e.name}: {row['mailbox']}")
        e.voicemail_mail_to = row["mailbox"]
        e.voicemail_enabled = True
    else:
        print(f"Skipping {e.name}: {e.voicemail_mail_to}")


def read_froms_csv(csv_file):
    with open(csv_file) as csv_extens:
        reader = csv.DictReader(csv_extens)
        for row in reader:
            if str(row["extension"]) in str(extens):
                if row["mailbox"]:
                    print("----------------------------------------------")
                    print(f"Trying   {row['extension']}: {row['mailbox']}")
                    print("Time taken   :", timeit.timeit(lambda: do_thing(row), number=1))


f = FusionPBX(browser, url, user, password)
# print(f.domains.list)])
