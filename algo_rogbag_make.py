# coding=utf-8
import rosbag
import sys
import os
import numpy as np
import cv2
from sensor_msgs.msg import Image, Imu
from cv_bridge import CvBridge
import rospy
from geometry_msgs.msg import Vector3

# IMU数据读取
def algoreadIMU(imu_path):
    timestamps = []
    wxs = []
    wys = []
    wzs = []
    axs = []
    ays = []
    azs = []
    fin = open(imu_path, 'r')
    line = fin.readline()
    while line:
        parts = line.split(",")
        symbol = parts[0]
        ts = float(parts[2])
        wx = float(parts[3]) * 0.0174532925
        wy = float(parts[4]) * 0.0174532925
        wz = float(parts[5]) * 0.0174532925
        ax = float(parts[6]) * 9.80665
        ay = float(parts[7]) * 9.80665
        az = float(parts[8]) * 9.80665

        if symbol == "$ALGOIMU" :
            timestamps.append(ts)
            wxs.append(wx)
            wys.append(wy)
            wzs.append(wz)
            axs.append(ax)
            ays.append(ay)
            azs.append(az)
        line = fin.readline().strip()
    return timestamps, wxs, wys, wzs, axs, ays, azs

# 读取description的路径和时间戳
def readDescription(imu_path):
    timestamps = []
    filenames = []
    fin = open(imu_path, 'r')
    fin.readline()
    line = fin.readline().strip()
    while line:
        parts = line.split(" ")
        filename = parts[0]
        ts = float(parts[2])
        timestamps.append(ts)
        filenames.append(filename)
        line = fin.readline().strip()
    return filenames, timestamps

if __name__ == '__main__':
    description = sys.argv[1]  # description文件路径
    img_topic_name = sys.argv[2]    # 影像Toc名称
    imu_path = sys.argv[3]  # IMU文件路径
    imu_topic_name = sys.argv[4]    # IMU Topic名称
    bag_path = sys.argv[5]  # Bag文件输出路径

    cam_files, cam_timestamps = readDescription(description)

    algoPath=os.path.dirname(description)
    for i in range(len(cam_files)):
        cam_files[i] = algoPath + "/" + cam_files[i]
    cam_files = np.array(cam_files)
    index = np.argsort(cam_files)
    cam_files = cam_files[index]
    cam_files = list(cam_files)
    # print(cam_files[0])
    # print(cam_timestamps[0])

    bag_out = rosbag.Bag(bag_path,'w')

    imu_ts, wxs, wys, wzs, axs, ays, azs = algoreadIMU(imu_path)
    imu_msg = Imu()
    angular_v = Vector3()
    linear_a = Vector3()

    cb = CvBridge()
    j = 0

    for i in range(len(imu_ts)):
        imu_ts_ros = rospy.rostime.Time.from_sec(imu_ts[i])
        imu_msg.header.stamp = imu_ts_ros
        
        angular_v.x = wxs[i]
        angular_v.y = wys[i]
        angular_v.z = wzs[i]

        linear_a.x = axs[i]
        linear_a.y = ays[i]
        linear_a.z = azs[i]

        imu_msg.angular_velocity = angular_v
        imu_msg.linear_acceleration = linear_a

        bag_out.write(imu_topic_name, imu_msg, imu_ts_ros)
        print('imu:',i,'/',len(imu_ts))

        # 判断时间条件
        while (j < len(cam_files) and i + 1 < len(imu_ts) and float(imu_ts[i]) <= float(cam_timestamps[j]) and float(cam_timestamps[j]) < float(imu_ts[i + 1])):
            print('image:',j,'/',len(cam_files))

            frame_img = cv2.imread(cam_files[j])
            timestamp = cam_timestamps[j]

            ros_ts = rospy.rostime.Time.from_sec(timestamp)
            ros_img = cb.cv2_to_imgmsg(frame_img,encoding='bgr8') 
            ros_img.header.stamp = ros_ts
            bag_out.write(img_topic_name,ros_img,ros_ts)
            j = j + 1
    
    bag_out.close()
