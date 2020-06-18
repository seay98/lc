import time
import datetime
import os
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqldb://flmgr:a1b2c3d4e5@127.0.0.1:3307/flmgr', echo=False)

devicetime = {}
delstarttime = {}
sqls = []
with engine.connect() as conn:
    result = conn.execute("SELECT deviceId, creatTime FROM flmgr.bsites_basesite order by creatTime;")
    
    for rec in result:
        ct = rec['creatTime']
        did = rec['deviceId']
        if did in devicetime:
            last = devicetime[did]
            inv = ct - last
            # print(inv.total_seconds())
            if inv.seconds > 180:
                if did in delstarttime:
                    delinv = ct - delstarttime[did]
                    if delinv.total_seconds() > 300:
                        sql = "delete from flmgr.bsites_basesite where deviceId='{}' and creatTime>'{}' and creatTime<'{}'".format(did, last, ct)
                        sqls.append(sql)
                        devicetime[did] = ct
                        delstarttime.pop(did)
                        # break
                else:
                    delstarttime[did] = ct
            else:
                devicetime[did] = ct
        else:
            devicetime[did] = datetime.datetime(2020,6,11,0,0,0)
    for sql in sqls:
        # r = conn.execute(sql)
        print(sql)
print(len(sqls))


