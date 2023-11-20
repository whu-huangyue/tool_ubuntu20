# coding=utf-8
import os
import sys

import math

import numpy as np
import rosbag
import rospy
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from gnss_comm.msg import AlgoPVTSolMsg

import pyproj

def ecef2lla(x,y,z):

    '''
    x = 652954.1006
    y = 4774619.7919
    z = -4167647.7937
    '''

    #ecef转化为经纬高
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    lon, lat, alt = pyproj.transform(ecef, lla, x, y, z, radians=False)#radians否用弧度返回值

    # print ('纬度：',lat)
    # print ('经度：',lon)
    # print ('高度：',alt)

    return lat,lon,alt

def readGPS(gps_path):
    # GPSTs = []
    Years = []
    Times = []
    xecefs = []
    yecefs = []
    zecefs = []
    Qs = []
    nss = []
    sdxs = []
    sdys = []
    sdzs = []
    sdxys = []
    sdyzs = []
    sdzxs = []
    ages = []
    ratios = []
    ves = []
    vns = []
    vus = []
    vstats = []
    sdves = []
    sdvns = []
    sdvus = []
    rolls = []
    pitchs = []
    yaws = []
    sdrolls = []
    sdpitchs = []
    sdyaws = []
    totalInferSecs = []
    fin = open(gps_path, 'r')

    # 从第五行开始
    fin.readline()
    line = fin.readline().strip()
    line = fin.readline().strip()
    line = fin.readline().strip()
    line = fin.readline().strip()

    while line:
        parts = line.split()

        # GPST = float(parts[0])
        Year = parts[0]
        Time = parts[1]
        xecef = float(parts[2])
        yecef = float(parts[3])
        zecef = float(parts[4])
        Q = parts[5]
        ns = parts[6]
        sdx = float(parts[7])
        sdy = float(parts[8])
        sdz = float(parts[9])
        sdxy = float(parts[10])
        sdyz = float(parts[11])
        sdzx = float(parts[12])
        age = parts[13]
        ratio = parts[14]
        ve = parts[15]
        vn = parts[16]
        vu = parts[17]
        vstat = parts[18]
        sdve = parts[19]
        sdvn = parts[20]
        sdvu = parts[21]
        # roll = parts[22]
        # pitch = parts[23]
        # yaw = parts[24]
        # sdroll = parts[25]
        # sdpitch = parts[26]
        # sdyaw = parts[27]
        # totalInferSec = parts[28]
        totalInferSec = parts[22]

        # GPSTs.append(GPST)
        Years.append(Year)
        Times.append(Time)
        xecefs.append(xecef)
        yecefs.append(yecef)
        zecefs.append(zecef)
        Qs.append(Q)
        nss.append(ns)
        sdxs.append(sdx)
        sdys.append(sdy)
        sdzs.append(sdz)
        sdxys.append(sdxy)
        sdyzs.append(sdyz)
        sdzxs.append(sdzx)
        ages.append(age)
        ratios.append(ratio)
        ves.append(ve)
        vns.append(vn)
        vus.append(vu)
        vstats.append(vstat)
        sdves.append(sdve)
        sdvns.append(sdvn)
        sdvus.append(sdvu)
        # rolls.append(roll)
        # pitchs.append(pitch)
        # yaws.append(yaw)
        # sdrolls.append(sdroll)
        # sdpitchs.append(sdpitch)
        # sdyaws.append(sdyaw)
        totalInferSecs.append(totalInferSec)

        line = fin.readline().strip()
    return Years, Times, xecefs, yecefs, zecefs, Qs, nss, sdxs, sdys, sdzs, sdxys, sdyzs, sdzxs, ages, ratios, ves, vns, vus, vstats, sdves, sdvns, sdvus, rolls, pitchs, yaws, sdrolls, sdpitchs, sdyaws, totalInferSecs


if __name__ == '__main__':
    gps_path = sys.argv[1]  # GPS数据文件路径
    # gps_topic_name = sys.argv[2]    # Topic名称
    # bag_path = sys.argv[3]  # 输出Bag路径

    # bag_out = rosbag.Bag(bag_path, 'w')

    Years, Times, xecefs, yecefs, zecefs, Qs, nss, sdxs, sdys, sdzs, sdxys, sdyzs, sdzxs, ages, ratios, ves, vns, vus, vstats, sdves, sdvns, sdvus, rolls, pitchs, yaws, sdrolls, sdpitchs, sdyaws, totalInferSecs = readGPS(gps_path)
    nian, yue, ri = Years[0].split("/")
    shi, fen, miao = Times[0].split(":")

    # # ecef2pos python实现
    # for i in range(len(xecefs)):
    # lat, lon, h = ecef2pos(xecefs[0], yecefs[0], zecefs[0])
    # print(xecefs[0], yecefs[0], zecefs[0])
    # lat, lon, h = ecef2pos(652954000, 47746000, -41676000)
    # print(lat, lon, h)
    # lat, lon, h = ecef2pos(0, 0, 0.0001)
    # print(lat, lon, h)

    lats = []
    lons = []
    alts = []

    for i in range(len(xecefs)):
        lat,lon,alt = ecef2lla(xecefs[i], yecefs[i], zecefs[i])
        lats.append(lat)
        lons.append(lon)
        alts.append(alt)
    
    nians = []
    yues = []
    ris = []
    shis = []
    fens = []
    miaos = []
    algo_weeks = []
    algo_secs = []

    algo_msg = AlgoPVTSolMsg()

    # 按照月份递增天数
    doy = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]

    t0day = (1980 - 1970) * 365 + math.floor((1980- 1969) / 4) + doy[1 - 1] + int(6) - 2 + (1 if int(1980) % 4 == 0 and int(1) >= 3 else 0)
    t0tempsec = math.floor(float(0))
    t0time = t0day * 86400 + 0 * 3600 + 0 * 60 + t0tempsec
    t0sec = 0 - t0tempsec

    for i in range(len(Years)):
        nian, yue, ri = Years[i].split("/")
        shi, fen, miao = Times[i].split(":")

        nians.append(nian)
        yues.append(yue)
        ris.append(ri)
        shis.append(shi)
        fens.append(fen)
        miaos.append(miao)

        # epoch2time time2gpst python实现
        algoday = (int(nians[i]) - 1970) * 365 + math.floor((int(nians[i]) - 1969) / 4) + doy[int(yues[i]) - 1] + int(ris[i]) - 2 + (1 if int(nians[i]) % 4 == 0 and int(yues[i]) >= 3 else 0)
        tempsec = math.floor(float(miaos[i]))

        algotime = algoday * 86400 + int(shis[i]) * 3600 + int(fens[i]) * 60 + tempsec
        algosec = float(miaos[i]) - tempsec

        sec = algotime - t0time
        algo_week = math.floor(sec / (86400 * 7))
        algo_sec = sec - algo_week * 86400 * 7 + algosec

        algo_weeks.append(algo_week)
        algo_secs.append(algo_sec)

    Nav_msg = NavSatFix()

    print(len(algo_secs))
    print(algo_secs)

    # for i in range(len(algo_weeks)):
    #     ros_ts = rospy.rostime.Time.from_sec(algo_secs[i])
    #     Nav_msg.header.stamp = ros_ts
    #     Nav_msg.latitude = lats[i]
    #     Nav_msg.longitude = lons[i]
    #     Nav_msg.altitude = alts[i]
    #     # Nav_msg.position_covariance = {sdxs[i]*sdxs[i], sdxys[i]*sdxys[i], sdzxs[i]*sdzxs[i], sdxys[i]*sdxys[i], sdys[i]*sdys[i], sdyzs[i]*sdyzs[i], sdzxs[i]*sdzxs[i], sdyzs[i]*sdyzs[i], sdzs[i]*sdzs[i]}
    #     Nav_msg.position_covariance[0] = sdxs[i]*sdxs[i]
    #     Nav_msg.position_covariance[1] = sdxys[i]*sdxys[i]
    #     Nav_msg.position_covariance[2] = sdzxs[i]*sdzxs[i]
    #     Nav_msg.position_covariance[3] = sdxys[i]*sdxys[i]
    #     Nav_msg.position_covariance[4] = sdys[i]*sdys[i]
    #     Nav_msg.position_covariance[5] = sdyzs[i]*sdyzs[i]
    #     Nav_msg.position_covariance[6] = sdzxs[i]*sdzxs[i]
    #     Nav_msg.position_covariance[7] = sdyzs[i]*sdyzs[i]
    #     Nav_msg.position_covariance[8] = sdzs[i]*sdzs[i]
    #     bag_out.write(gps_topic_name, Nav_msg, ros_ts)
    #     print('gps(icgvins):', i, '/', len(algo_weeks))

    # bag_out.close()

    # print(algo_secs[0])
    # print(algo_secs[len(algo_secs) - 1])

    # for i in range(len(algo_weeks)):
    #     algo_msg.week = algo_weeks[i]
    #     algo_msg.sec = algo_secs[i]
    #     algo_msg.X = float(xecefs[i])
    #     algo_msg.Y = float(yecefs[i])
    #     algo_msg.Z = float(zecefs[i])
    #     algo_msg.stat = int(Qs[i])
    #     algo_msg.ns = int(nss[i])
    #     algo_msg.stdX = float(sdxs[i])
    #     algo_msg.stdY = float(sdys[i])
    #     algo_msg.stdZ = float(sdzs[i])
    #     algo_msg.stdXY = float(sdxys[i])
    #     algo_msg.stdYZ = float(sdyzs[i])
    #     algo_msg.stdZX = float(sdzxs[i])
    #     algo_msg.age = float(ages[i])
    #     algo_msg.ratio = float(ratios[i])
    #     algo_msg.vel_e = float(ves[i])
    #     algo_msg.vel_n = float(vns[i])
    #     algo_msg.vel_u = float(vus[i])
    #     algo_msg.vstat = int(vstats[i])
    #     algo_msg.stdvel_e = float(sdves[i])
    #     algo_msg.stdvel_n = float(sdvns[i])
    #     algo_msg.stdvel_u = float(sdvus[i])
    #     algo_msg.roll = float(rolls[i])
    #     algo_msg.pitch = float(pitchs[i])
    #     algo_msg.yaw = float(yaws[i])
    #     algo_msg.stdroll = float(sdrolls[i])
    #     algo_msg.stdpitch = float(sdpitchs[i])
    #     algo_msg.stdyaw = float(sdyaws[i])
    #     algo_msg.totalInferSec = float(totalInferSecs[i])
    #     ros_ts = rospy.rostime.Time.from_sec(algo_secs[i])
        
    #     bag_out.write(gps_topic_name, algo_msg, ros_ts)
    #     # print('gps:', i, '/', len(algo_weeks))

    # bag_out.close()