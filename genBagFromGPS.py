# coding=utf-8
import os
import sys

import math

import numpy as np
import rosbag
import rospy
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Imu
from gnss_comm.msg import AlgoPVTSolMsg

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
        xecef = parts[2]
        yecef = parts[3]
        zecef = parts[4]
        Q = parts[5]
        ns = parts[6]
        sdx = parts[7]
        sdy = parts[8]
        sdz = parts[9]
        sdxy = parts[10]
        sdyz = parts[11]
        sdzx = parts[12]
        age = parts[13]
        ratio = parts[14]
        ve = parts[15]
        vn = parts[16]
        vu = parts[17]
        vstat = parts[18]
        sdve = parts[19]
        sdvn = parts[20]
        sdvu = parts[21]
        roll = parts[22]
        pitch = parts[23]
        yaw = parts[24]
        sdroll = parts[25]
        sdpitch = parts[26]
        sdyaw = parts[27]
        totalInferSec = parts[28]

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
        rolls.append(roll)
        pitchs.append(pitch)
        yaws.append(yaw)
        sdrolls.append(sdroll)
        sdpitchs.append(sdpitch)
        sdyaws.append(sdyaw)
        totalInferSecs.append(totalInferSec)

        line = fin.readline().strip()
    return Years, Times, xecefs, yecefs, zecefs, Qs, nss, sdxs, sdys, sdzs, sdxys, sdyzs, sdzxs, ages, ratios, ves, vns, vus, vstats, sdves, sdvns, sdvus, rolls, pitchs, yaws, sdrolls, sdpitchs, sdyaws, totalInferSecs


if __name__ == '__main__':
    gps_path = sys.argv[1]  # GPS数据文件路径
    gps_topic_name = sys.argv[2]    # Topic名称
    bag_path = sys.argv[3]  # 输出Bag路径

    bag_out = rosbag.Bag(bag_path, 'w')

    Years, Times, xecefs, yecefs, zecefs, Qs, nss, sdxs, sdys, sdzs, sdxys, sdyzs, sdzxs, ages, ratios, ves, vns, vus, vstats, sdves, sdvns, sdvus, rolls, pitchs, yaws, sdrolls, sdpitchs, sdyaws, totalInferSecs = readGPS(gps_path)
    nian, yue, ri = Years[0].split("/")
    shi, fen, miao = Times[0].split(":")

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

    # print(algo_secs[0])
    # print(algo_secs[len(algo_secs) - 1])

    for i in range(len(algo_weeks)):
        algo_msg.week = algo_weeks[i]
        algo_msg.sec = algo_secs[i]
        algo_msg.X = float(xecefs[i])
        algo_msg.Y = float(yecefs[i])
        algo_msg.Z = float(zecefs[i])
        algo_msg.stat = int(Qs[i])
        algo_msg.ns = int(nss[i])
        algo_msg.stdX = float(sdxs[i])
        algo_msg.stdY = float(sdys[i])
        algo_msg.stdZ = float(sdzs[i])
        algo_msg.stdXY = float(sdxys[i])
        algo_msg.stdYZ = float(sdyzs[i])
        algo_msg.stdZX = float(sdzxs[i])
        algo_msg.age = float(ages[i])
        algo_msg.ratio = float(ratios[i])
        algo_msg.vel_e = float(ves[i])
        algo_msg.vel_n = float(vns[i])
        algo_msg.vel_u = float(vus[i])
        algo_msg.vstat = int(vstats[i])
        algo_msg.stdvel_e = float(sdves[i])
        algo_msg.stdvel_n = float(sdvns[i])
        algo_msg.stdvel_u = float(sdvus[i])
        algo_msg.roll = float(rolls[i])
        algo_msg.pitch = float(pitchs[i])
        algo_msg.yaw = float(yaws[i])
        algo_msg.stdroll = float(sdrolls[i])
        algo_msg.stdpitch = float(sdpitchs[i])
        algo_msg.stdyaw = float(sdyaws[i])
        algo_msg.totalInferSec = float(totalInferSecs[i])
        ros_ts = rospy.rostime.Time.from_sec(algo_secs[i])
        
        bag_out.write(gps_topic_name, algo_msg, ros_ts)
        print('gps:', i, '/', len(algo_weeks))

    bag_out.close()