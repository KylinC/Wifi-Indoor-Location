import math

'''
PLd1: 1米处的rssi值
PLd2: 2米处的rssi值
'''
def getDistance(PLd1, PLd2, PLd):
    yita = (PLd1-PLd2)/(10*math.log10(2))
    return 10^((PLd1-PLd)/(10*yita))



def locateAlgo(Apos, Bpos, Cpos, Adis, Bdis, Cdis):
    AB1, AB2 = insec(Apos, Adis, Bpos, Bdis)
    if(abs(dist(AB1, Cpos)-Cdis) < abs(dist(AB2, Cpos)-Cdis)):
        x1 = AB1[0]
        y1 = AB1[1]
    else:
        x1 = AB2[0]
        y1 = AB2[1]
    
    BC1, BC2 = insec(Cpos, Cdis, Bpos, Bdis)
    if(abs(dist(BC1, Apos)-Adis) < abs(dist(BC2, Apos)-Adis)):
        x2 = BC1[0]
        y2 = BC1[1]
    else:
        x2 = BC2[0]
        y2 = BC2[1]

    AC1, AC2 = insec(Cpos, Cdis, Apos, Adis)
    if(abs(dist(AC1, Bpos)-Bdis) < abs(dist(AC2, Bpos)-Bdis)):
        x3 = AC1[0]
        y3 = AC1[1]
    else:
        x3 = AC2[0]
        y3 = AC2[1]

    x = (x1/(Adis+Bdis)+x2/(Bdis+Cdis)+x3/(Cdis+Adis))/(1/(Adis+Bdis)+1/(Bdis+Cdis)+1/(Cdis+Adis))
    y = (y1/(Adis+Bdis)+y2/(Bdis+Cdis)+y3/(Cdis+Adis))/(1/(Adis+Bdis)+1/(Bdis+Cdis)+1/(Cdis+Adis))
    return x,y



def insec(p1,r1,p2,r2):
    x = p1[0]
    y = p1[1]
    R = r1
    a = p2[0]
    b = p2[1]
    S = r2
    d = math.sqrt((abs(a-x))**2 + (abs(b-y))**2)
    if d > (R+S) or d < (abs(R-S)):
        print ("Two circles have no intersection")
        return None
    elif d == 0 and R==S :
        print ("Two circles have same center!")
        return None
    else:
        A = (R**2 - S**2 + d**2) / (2 * d)
        h = math.sqrt(R**2 - A**2)
        x2 = x + A * (a-x)/d
        y2 = y + A * (b-y)/d
        x3 = round(x2 - h * (b - y) / d,2)
        y3 = round(y2 + h * (a - x) / d,2)
        x4 = round(x2 + h * (b - y) / d,2)
        y4 = round(y2 - h * (a - x) / d,2)
        print (x3, y3)
        print (x4, y4)
        c1=np.array([x3, y3])
        c2=np.array([x4, y4])
        return c1,c2



def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])^2+(p1[1]-p2[1])^2)