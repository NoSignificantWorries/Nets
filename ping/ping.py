import os
import csv

import re


def read_output(domain):
    with open("tmp.txt", "r") as file:
        lines = file.readlines()
        ip = re.search(r'\d+.\d+.\d+.\d+', lines[0])
        loss = re.search(r'\d+%', lines[3])
        time = re.search(r'\d+ms', lines[3])
        return [domain,
                ip[0] if ip else None, 
                int(loss[0][:-1]) if loss else None, 
                float(time[0][:-2]) if time else None, 
                lines[4][:-1]]


domains = ["google.com", "archlinux.org", "123.0.0.1"]

result_file = open("res.csv", "w")
writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(["Domain", "IP", "Lost pakages", "Time", "rtt"])

for domain in domains:
    print(f"Pinging {domain}")
    response = os.system(f"ping -c 3 -q {domain} > tmp.txt")
    if response == 0:
        out = read_output(domain)
        writer.writerow(out)
    else:
        writer.writerow([domain, None, None, None, None])

result_file.close()

