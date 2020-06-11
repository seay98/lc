# import csv
from sqlalchemy import create_engine
import lines

# datapath = "/home/yh/data/lc/"

engine = create_engine('mysql+mysqldb://flmgr:a1b2c3d4e5@127.0.0.1:3307/flmgr', echo=False)

laccis = []
with engine.connect() as conn:
    result = conn.execute("select lac, ci1, mnc from flmgr.bsites_basesite group by lac, ci1, mnc")
    for row in result:
        laccis.append([row['lac'], row['ci1'], row['mnc']])

    for lacci in laccis:
        res = conn.execute("select latitude, longitude from flmgr.bsites_basesite where lac={0[0]} and ci1={0[1]} and mnc={0[2]}".format(lacci))
        points = []
        for row in res:
            p =  [round(float(row['latitude']), 6), round(float(row['longitude']), 6)]
            pw = lines.get_wgs84(p)
            points.append(pw)
        
        if len(points) < 3:
            continue
        coverpoints = lines.get_geocoverpoints(points)
        signalcov = ""
        for i in range(len(coverpoints)):
            tmp =lines.get_gcj02(coverpoints[i])
            if signalcov:
                signalcov = signalcov + ","
            signalcov = signalcov + "{0[1]:.6f},{0[0]:.6f}".format(tmp)
        # print(signalcov)
        rexist = conn.execute("select signalrange from flmgr.bsites_celllocation where lac={0[0]} and ci1={0[1]} and mnc={0[2]}".format(lacci))
        if rexist.rowcount == 0:
            sqlstr = "INSERT INTO flmgr.bsites_celllocation (mnc, lac, ci1, signalrange) VALUES ({0[2]}, {0[0]}, {0[1]}, '{1}')".format(lacci, signalcov)
            print(sqlstr)
            conn.execute(
                sqlstr
            )
        else:
            conn.execute(
                "update flmgr.bsites_celllocation set signalrange='{0}'".format(signalcov)
            )
        