from sqlalchemy import create_engine
import lines


engine = create_engine('mysql+mysqldb://flmgr:a1b2c3d4e5@127.0.0.1:3306/flmgr', echo=False)

def whichcis(point):
    cis = []
    with engine.connect() as conn:
        result = conn.execute("select id, lac, ci1, mnc, signalrange from flmgr.bsites_celllocation")
        for row in result:
            sgnrange = row['signalrange']
            points = sgnrange.split(',')
            points = [float(p) for p in points]
            path = [points[i:i+2] for i in range(0,len(points),2)]
            inornot = lines.is_inpolygon(point, path)
            if inornot:
                res = conn.execute("select rs, latitude, longitude from flmgr.bsites_basesite where lac={} and ci1={};".format(row['lac'], row['ci1']))
                mds = 9999
                rs = -999
                for pt in res:
                    p = [float(pt['latitude']), float(pt['longitude'])]
                    ds = lines.get_geodistance(point, p)
                    if ds < mds:
                        mds = ds
                        rs = int(pt['rs'])
                ci = {'id':row['id'], 'lac':row['lac'], 'ci1':row['ci1'], 'mnc':row['mnc'], 'rs':rs}
                cis.append(ci)
    return cis

def findci(lac, ci):
    cif = {}
    with engine.connect() as conn:
        sql = "select id, lac, ci1, mnc from flmgr.bsites_celllocation where lac={} and ci1={}".format(lac, ci)
        result = conn.execute(sql)
        print(sql)
        for row in result:
            cif = {'id':row['id'], 'lac':row['lac'], 'ci1':row['ci1'], 'mnc':row['mnc']}
    return cif

def whichlacs(point):
    lacs = []
    with engine.connect() as conn:
        result = conn.execute("select id, lac, mnc, coverage from flmgr.bsites_lac")
        for row in result:
            sgnrange = row['coverage']
            points = sgnrange.split(',')
            points = [float(p) for p in points]
            path = [points[i:i+2] for i in range(0,len(points),2)]
            inornot = lines.is_inpolygon(point, path)
            if inornot:
                lac = {'id':row['id'], 'lac':row['lac'], 'mnc':row['mnc']}
                lacs.append(lac)
    return lacs

