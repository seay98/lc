# import csv
from sqlalchemy import create_engine
import lines

# datapath = "/home/yh/data/lc/"

engine = create_engine('mysql+mysqldb://flmgr:a1b2c3d4e5@127.0.0.1:3307/flmgr', echo=False)

laccis = []
with engine.connect() as connection:
    result = connection.execute("select lac, ci1 from flmgr.bsites_basesite group by lac, ci1")
    for row in result:
        laccis.append([row['lac'], row['ci1']])

    for lacci in laccis:
        res = connection.execute("select latitude, longitude from flmgr.bsites_basesite where lac={} and ci1={}".format(lacci[0], lacci[1]))
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
        break