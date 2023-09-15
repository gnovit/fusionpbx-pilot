import timeit


from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX
import csv

browser = Firefox()
# wdw = WebDriverWait(browser, 10)
url = "http://45.79.223.247"
user = "admin"
password = "S3nh4C0mpl3x4$"


f = FusionPBX(browser, url, user, password)
# d = f.domain


def do_thing(row):
    e = f.domain.extension(row['extension'])
    if not e.voicemail_mail_to:
        print(f"Setting  {e.name}: {row['mailbox']}")
        e.voicemail_mail_to = row['mailbox']
        e.voicemail_enabled = True
    else:
        print(f"Skipping {e.name}: {e.voicemail_mail_to}")


with open(r'stuff/extensions.csv') as extensions:
    reader = csv.DictReader(extensions)
    for row in reader:
        if row['extension'] and row['mailbox']:
            print("----------------------------------------------")
            print(f"Trying   {row['extension']}: {row['mailbox']}")
            print("Time taken   :", timeit.timeit(lambda: do_thing(row), number=1))

