import json
import csv


ypath = "/home/yh/data/CSC44F33252565_20200601000.csv"
csvpath = "/home/yh/data/csc44t.csv"

with open(ypath) as f:
    # cnt = 0
    # while True:
    #     rf = f.readline()
    #     if not rf:
    #         break
    #     cnt = cnt + 1
    #     print(cnt)
    lines = f.readlines()

    with open(csvpath, 'w+') as cf:
        writer = csv.writer(cf)
        writer.writerow(['mnc', 'lac', 'ci1', 'ci2', 'ch', 'pci', 'rs', 'longitude', 'latitude', 'addresses', 'deviceId', 'createTime', 'nonce'])
        for line in lines:
            items = line.strip(',\n').split(',')
            print(items)
            if len(items) == 13:
                if items[0].split(':')[0] == 'lat_':
                    continue
                items[0] = 'opt:0'
                if items[0].split(':')[1] == 'lt':
                    items[0] = 'opt:1'
                elif items[0].split(':')[1] == 'dx':
                    items[0] = 'opt:11'
                writer.writerow([item.split(':',1)[1] for item in items])

