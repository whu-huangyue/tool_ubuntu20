# coding=utf-8
import rosbag
import sys
import os
import numpy as np
import csv

def readIMU(imu_path):
    timestamps = []
    wxs = []
    wys = []
    wzs = []
    axs = []
    ays = []
    azs = []
    fin = open(imu_path, 'r')
    fin.readline()
    line = fin.readline().strip()
    while line:
        parts = line.split(",")
        ts = float(parts[0])
        wx = float(parts[1])
        wy = float(parts[2])
        wz = float(parts[3])
        ax = float(parts[4])
        ay = float(parts[5])
        az = float(parts[6])
        timestamps.append(ts)

        wxs.append(wx)
        wys.append(wy)
        wzs.append(wz)
        axs.append(ax)
        ays.append(ay)
        azs.append(az)
        line = fin.readline().strip()
    return timestamps, wxs, wys, wzs, axs, ays, azs


if __name__ == '__main__':
    imu_path = sys.argv[1]  # IMU数据文件路径
    # 指令：python3 imuchuli.py .../data.csv 然后依次输出修改数据的起始时间和结束时间，注意时间19位，不带小数点。

    arr = input()
    arr = arr.split(" ")
    mylength = int(len(arr) / 2)

    imu_ts, wxs, wys, wzs, axs, ays, azs = readIMU(imu_path)

    dir_path = os.path.dirname(imu_path)
    save_path = dir_path + '/newdata.csv'
    file = open(save_path, 'w')
    writer = csv.writer(file)
    
    for i in range(len(imu_ts)):
        for j in range(mylength):
            if (imu_ts[i] >= float(arr[j*2]) and imu_ts[i] <= float(arr[j*2+1])):
                data = ["{:.0f}".format(imu_ts[i]), 0, 0, 0, 0, 0, 0]
            else:
                data = ["{:.0f}".format(imu_ts[i]), wxs[i], wys[i], wzs[i],axs[i], ays[i], azs[i]]
        writer.writerow(data)
    file.close()
