import random
import csv

charset = '0123456789abcdef'
type = ['Virus', 'Worm', 'Trojan']

data = []

for t in range(10**3):
    a = [charset[random.randint(0, len(charset) - 1)] for i in range(32)]
    signature = ''.join(a)
    malware_type = random.choice(type)
    data.append([signature, malware_type])

data.append(['6dd0db7de00fb745e89801c025ffff00', 'Virus'])

fields = ['Signature', 'Type']

with open('database.csv', 'w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(fields)
    csvwriter.writerows(data)