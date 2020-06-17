# import csv
from sqlalchemy import create_engine
import lines

# datapath = "/home/yh/data/lc/"

engine = create_engine('mysql+mysqldb://flmgr:a1b2c3d4e5@127.0.0.1:3307/flmgr', echo=False)

lacs = []
with engine.connect() as conn:
    # LAC覆盖
    # 获取所有lac-mnc
    result = conn.execute("select lac, mnc from flmgr.bsites_celllocation group by lac, mnc")
    for row in result:
        lacs.append([row['lac'], row['mnc']])
    # 获取lac-mnc内的外围点
    for lac in lacs:
        res = conn.execute("select signalrange from flmgr.bsites_celllocation where lac={0[0]} and mnc={0[1]}".format(lac))
        for row in res:
            points = row['signalrange'].split(',')
            points = [float(p) for p in points]
            pts = [points[i:i+2] for i in range(0,len(points),2)]
            points = []
            for p in pts:
                pw = lines.get_wgs84([p[1],p[0]])
                points.append(pw)
        # 获得lac-mnc外围点
        coverpoints = lines.get_geocoverpoints(points)
        if len(coverpoints) < 3:
            continue
        # 整理为入库格式，入库
        signalcov = ""
        for i in range(len(coverpoints)):
            tmp =lines.get_gcj02(coverpoints[i])
            if signalcov:
                signalcov = signalcov + ","
            signalcov = signalcov + "{0[1]:.6f},{0[0]:.6f}".format(tmp)
        # print(signalcov)
        rexist = conn.execute("select coverage from flmgr.bsites_lac where lac={0[0]} and mnc={0[1]}".format(lac))
        if rexist.rowcount == 0:
            sqlstr = "INSERT INTO flmgr.bsites_lac (mnc, lac, coverage) VALUES ({0[1]}, {0[0]}, '{1}')".format(lac, signalcov)
            print(sqlstr)
            conn.execute(sqlstr)
        else:
            sqlstr = "update flmgr.bsites_lac set coverage='{0}' where lac={1[0]} and mnc={1[1]}".format(signalcov, lac)
            print(sqlstr)
            conn.execute(sqlstr)
