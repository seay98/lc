import time
import datetime
import os
from sqlalchemy import create_engine
import lines


engine = create_engine('mysql+mysqldb://flmgr:a1b2c3d4e5@127.0.0.1:3307/flmgr', echo=False)

with engine.connect() as conn:
    result = conn.execute("SELECT deviceId, latitude, longitude, creatTime FROM flmgr.bsites_basesite order by creatTime;")
    
    # 找出工作时间段
    spans = []
    starttime = {}
    prevtime = {}
    endtime = {}
    for rec in result:
        ct = rec['creatTime']
        did = rec['deviceId']
        if did in starttime:
            prev = prevtime[did]
            inv = ct - prev
            # print(inv.total_seconds())
            if inv.seconds > 180:
                endtime[did] = ct
                spans.append([did, starttime[did]-datetime.timedelta(seconds=1), endtime[did]])
                # print([did, starttime[did], endtime[did]])
                starttime[did] = ct
            prevtime[did] = ct
        else:
            starttime[did] = ct
            prevtime[did] = ct
    for did in starttime:
        spans.append([did, starttime[did]-datetime.timedelta(seconds=1), prevtime[did]+datetime.timedelta(seconds=1)])
        # print([did, starttime[did], prevtime[did]])

    # 找出时间段内漂移点
    pgroup = []
    for span in spans:
        sql = "SELECT id, deviceId, latitude, longitude, creatTime FROM flmgr.bsites_basesite where deviceId='{0[0]}' and creatTime>'{0[1]}' and creatTime<'{0[2]}' order by creatTime;".format(span)
        # print(sql)
        result = conn.execute(sql)
        pgroup.clear()
        for row in result:
            cp = [round(float(row['latitude']),6), round(float(row['longitude']),6)]
            ct = row['creatTime']
            alone = True
            for g in pgroup:
                ds = lines.get_geodistance(cp, g['lastpoint'])
                inv = row['creatTime'] - g['lasttime']
                if ds < 500:
                    g['lastpoint'] = cp
                    g['lasttime'] = ct
                    g['ids'].append(row['id'])
                    alone = False
                    break
            if alone:
                newg = {'ids':[row['id']], 'lastpoint':cp, 'lasttime':ct}
                pgroup.append(newg)
        # 删除漂移点
        plen = 0
        for i, pg in enumerate(pgroup):
            l = len(pg['ids'])
            if l > plen:
                plen = l
                index = i
        pgroup.pop(index)
        for pg in pgroup:
            for rid in pg['ids']:
                sql = "delete from flmgr.bsites_basesite where id='{}'".format(rid)
                # res = conn.execute(sql)
                print(sql)


