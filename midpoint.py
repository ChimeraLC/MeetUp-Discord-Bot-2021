import math
def midpointFailed(pair1, pair2):
    pair1 = pair1.split(",")
    pair2 = pair2.split(",")
    x1 = float(pair1[0])
    lon = float(pair1[1])
    lat2 = float(pair2[0])
    lon2 = float(pair2[0])
    y1 = float(pair1[1])
    x2 = float(pair2[0])
    y2 = float(pair2[1])
    return(str((x1+x2)/2)+','+str((y1+y2)/2))
    lat1 = math.radians(x1)
    lon1 = math.radians(x2)
    lat2 = math.radians(y1)
    lon2 = math.radians(y2)
    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), \
           math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) \
           + bx) + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + Bx)
    return [round(math.degrees(lat3), 2), round(math.degrees(lon3), 2)]
    
def midPoint(pair1, pair2):
    pair1 = pair1.split(",")
    pair2 = pair2.split(",")
    x1 = float(pair1[0])
    y1 = float(pair1[1])
    x2 = float(pair2[0])
    y2 = float(pair2[1])
    return(str((x1+x2)/2)+','+str((y1+y2)/2))
