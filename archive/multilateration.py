from scanner import *
from config import *
import math
import numpy as np
import sys
import os

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def getDistance(PLd1, PLd2, PLd):
    '''
    Get Device Distance according to rssi value
    Input: PLd1: rssi value at 1m
           PLd2: rssi value at 2m
    Output: current AP distance
    '''
    yita = (PLd1-PLd2)/(10*math.log10(2))
    return 10**((PLd1-PLd)/(10*yita))


def insec(p1,r1,p2,r2):
    '''
    Two circles Insection Algorithm
    Input: position and radius of circles
    Output: intersection position
    '''
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

        x3 = x2 - h * (b - y) / d
        y3 = y2 + h * (a - x) / d
        x4 = x2 + h * (b - y) / d
        y4 = y2 - h * (a - x) / d

        c1=np.array([x3, y3])
        c2=np.array([x4, y4])

        return c1,c2


def locateAlgo(Apos, Bpos, Cpos, Adis, Bdis, Cdis):
    '''
    get current position 
    Input: three AP positions
    Output: current position
    '''
    Apos = [float(i) for i in Apos]
    Bpos = [float(i) for i in Bpos]
    Cpos = [float(i) for i in Cpos]

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


if __name__ == "__main__":
    repeatTime = 1
    test = Scanner(INIT_AP)
    print("---------------- Set-up Begin -------------------")

    # AP 1
    pos1 = input("Enter the position of "+INIT_AP[0]+" : ")
    pos1 = pos1.split(sep=" ")
    print("Place the device 1 meter away from " + INIT_AP[0], end="")
    input()
    temp = []
    while len(temp)<repeatTime:
        os.system("networksetup -setairportpower en0 on")
        a = test.scan_aim()
        if "ssid" in a[INIT_AP[0]].keys():
            print(a[INIT_AP[0]]["ssid"], a[INIT_AP[0]]["signal"], sep=" : ")
        else:
            continue
        temp.append(a[INIT_AP[0]]["signal"])
        os.system("networksetup -setairportpower en0 off")
    Pld1A = sum(temp)/len(temp)

    print("Place the device 2 meter away from " + INIT_AP[0], end="")
    input()
    temp = []
    while len(temp)<repeatTime:
        os.system("networksetup -setairportpower en0 on")
        a = test.scan_aim()
        if "ssid" in a[INIT_AP[0]].keys():
            print(a[INIT_AP[0]]["ssid"], a[INIT_AP[0]]["signal"], sep=" : ")
        else:
            continue
        temp.append(a[INIT_AP[0]]["signal"])
        os.system("networksetup -setairportpower en0 off")
    Pld2A = sum(temp)/len(temp)



    # AP2
    pos2 = input("Enter the position of "+INIT_AP[1]+" : ")
    pos2 = pos2.split(sep=" ")
    print("Place the device 1 meter away from "+INIT_AP[1], end="")
    input()
    temp = []
    while len(temp)<repeatTime:
        os.system("networksetup -setairportpower en0 on")
        a = test.scan_aim()
        if "ssid" in a[INIT_AP[1]].keys():
            print(a[INIT_AP[1]]["ssid"], a[INIT_AP[1]]["signal"], sep=" : ")
        else:
            continue
        temp.append(a[INIT_AP[1]]["signal"])
        os.system("networksetup -setairportpower en0 off")
    Pld1B = sum(temp)/len(temp)

    print("Place the device 2 meter away from "+INIT_AP[1], end="")
    input()
    temp = []
    while len(temp)<repeatTime:
        os.system("networksetup -setairportpower en0 on")
        a = test.scan_aim()
        if "ssid" in a[INIT_AP[1]].keys():
            print(a[INIT_AP[1]]["ssid"], a[INIT_AP[1]]["signal"], sep=" : ")
        else:
            continue
        temp.append(a[INIT_AP[1]]["signal"])
        os.system("networksetup -setairportpower en0 off")
    Pld2B = sum(temp)/len(temp)



    # AP3
    pos3 = input("Enter the position of "+INIT_AP[2]+" : ")
    pos3 = pos3.split(sep=" ")
    print("Place the device 1 meter away from "+INIT_AP[2], end="")
    input()
    temp = []
    while len(temp)<repeatTime:
        os.system("networksetup -setairportpower en0 on")
        a = test.scan_aim()
        if "ssid" in a[INIT_AP[2]].keys():
            print(a[INIT_AP[2]]["ssid"], a[INIT_AP[2]]["signal"], sep=" : ")
        else:
            continue
        temp.append(a[INIT_AP[2]]["signal"])
        os.system("networksetup -setairportpower en0 off")
    Pld1C = sum(temp)/len(temp)

    print("Place the device 2 meter away from "+INIT_AP[2], end="")
    input()
    temp = []
    while len(temp)<repeatTime:
        os.system("networksetup -setairportpower en0 on")
        a = test.scan_aim()
        if "ssid" in a[INIT_AP[2]].keys():
            print(a[INIT_AP[2]]["ssid"], a[INIT_AP[2]]["signal"], sep=" : ")
        else:
            continue
        temp.append(a[INIT_AP[2]]["signal"])
        os.system("networksetup -setairportpower en0 off")
    Pld2C = sum(temp)/len(temp)

    print("---------------- Set-up Done -------------------")

    # AP3
    print("Place the device at target location", end="")
    input()
    temp = [[],[],[]]
    while len(temp[0])<repeatTime or len(temp[1])<repeatTime or len(temp[2])<repeatTime:
        os.system("networksetup -setairportpower en0 on")
        a = test.scan_aim()
        for i in range(3):
            if "ssid" in a[INIT_AP[i]].keys():
                print(a[INIT_AP[i]]["ssid"], a[INIT_AP[i]]["signal"], sep=" : ", end = "     ")
                temp[i].append(a[INIT_AP[i]]["signal"])
        os.system("networksetup -setairportpower en0 off")
        print("")

    dis1 = getDistance(Pld1A, Pld2A, sum(temp[0])/len(temp[0]))
    dis2 = getDistance(Pld1B, Pld2B, sum(temp[1])/len(temp[1]))
    dis3 = getDistance(Pld1C, Pld2C, sum(temp[2])/len(temp[2]))

    print('The distance of AP1 is: ', dis1)
    print('The distance of AP2 is: ', dis2)
    print('The distance of AP3 is: ', dis3)

    x, y = locateAlgo(pos1, pos2, pos3, dis1, dis2, dis3)
    print("the location is ", x, y)

