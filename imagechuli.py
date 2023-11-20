import cv2
import sys
import os

# 读取时间戳
def readDescription(path):
    timestamps = []
    filenames = []
    fin = open(path, 'r')
    fin.readline()
    line = fin.readline().strip()
    while line:
        parts = line.split(",")
        timestamp = float(parts[0])
        filename = parts[1]
        timestamps.append(timestamp)
        filenames.append(filename)
        line = fin.readline().strip()
    return filenames, timestamps

if __name__ == '__main__':
    # 指令：python3 imagechuli.py '/home/hy/下载/testmav0/cam0/data.csv' 注意：输入cam0的data.csv
    # 然后依次输入摸黑image的起始时间和结束时间，用空格分割
    img_path = sys.argv[1] # img data.csv 的路径
    filenames, timestamps = readDescription(img_path)
    path = os.path.dirname(img_path)
    img_src = path + '/data'
    img1temp = os.path.dirname(path)
    img1_src = img1temp + '/cam1/data'

    arr = input()
    arr = arr.split(" ")
    mylength = int(len(arr) / 2)
    
    for i in range(len(filenames)):
        for j in range(mylength):
            if (timestamps[i] >= float(arr[j*2]) and timestamps[i] <= float(arr[j*2+1])):
                imagepath = img_src + '/' + filenames[i]
                img1 = cv2.imread(imagepath)
                img1[:,:] = 0
                cv2.imwrite(imagepath, img1)
                imagepath = img1_src + '/' + filenames[i]
                img1 = cv2.imread(imagepath)
                img1[:,:] = 0
                cv2.imwrite(imagepath, img1)