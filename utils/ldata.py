import json
import csv

jsonpath = "/home/yh/data/lc/c2565.json"
csvpath = "/home/yh/data/lc/c2565.csv"

with open(jsonpath) as jf:
    jsd = json.loads(jf.read())
    # print(jsd['data'])

    with open(csvpath, 'w+') as cf:
        data = jsd['data'][0]
        writer = csv.writer(cf)
        writer.writerow(data.keys())

        for data in jsd['data']:
            writer.writerow(data.values())

    cf.close()
jf.close()
