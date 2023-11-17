import timeit


from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX
import csv

browser = Firefox()

url = "https://<url>"
user = "admin"
password = "pass"

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
                    print(
                        "Time taken   :", timeit.timeit(lambda: do_thing(row), number=1)
                    )


f = FusionPBX(browser, url, user, password)

forget = ["45.79.223.247", "dev.gnovit.net", "confianca.dev.gnovit.net"]
all_domains = f.domains.list()
for d in all_domains:
    if d['name'] not in forget:
        print(f"Deleting Domain: {d['name']}")
        domain = f.domain(d['name'])
        del domain.name
    else:
        print(f"Skipping Domain: {d['name']}")

# d = f.domain('dressler.gnovit.net')
# l = d.extensions.list()
# count = 0 
# extensions_enabled=[]
# for e in l:
#     if eval(e['enabled']):
#         # count += 1
#         extensions_enabled.append(e['name'])
# print(f"Ramais ativos: {extensions_enabled}")
# print(f"Total: {extensions_enabled.__len__()}")
