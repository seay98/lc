from sqlalchemy import create_engine
import lines


engine = create_engine('mysql+mysqldb://flmgr:a1b2c3d4e5@127.0.0.1:3307/flmgr', echo=False)

def whichcis(point):
    cis = []
    with engine.connect() as conn:
        result = conn.execute("select lac, ci1, mnc, signalrange from flmgr.bsites_celllocation")
        for row in result:
            sgnrange = row['signalrange']
            points = sgnrange.split(',')
            points = [float(p) for p in points]
            path = [points[i:i+2] for i in range(0,len(points),2)]
            inornot = lines.is_inpolygon(point, path)
            if inornot:
                ci = {'lac':row['lac'], 'ci1':row['ci1'], 'mnc':row['mnc']}
                cis.append(ci)
    return cis