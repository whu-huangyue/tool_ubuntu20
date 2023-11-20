import sys
import cv2
import numpy as np

def readSeqDuration(file_path):
    fin = open(file_path, "r")
    fin.readline()
    fin.readline()
    seq_start_time = int(fin.readline().strip().split(":")[1])
    seq_end_time = int(fin.readline().strip().split(":")[1])
    fin.close()
    return seq_start_time, seq_end_time

def readImgBlack(file_path):
    fin = open(file_path, "r")
    fin.readline()
    black_num = int(fin.readline().strip().split(":")[1])

    black_start_times = []
    black_end_times = []
    for i in range(black_num):
        parts = fin.readline().strip().split(",")
        cur_start_time = int(parts[0].split(":")[-1])
        cur_end_time = int(parts[1].split(":")[-1])
        black_start_times.append(cur_start_time)
        black_end_times.append(cur_end_time)
    return black_start_times, black_end_times

def readIMUBlack(file_path):
    fin = open(file_path, "r")
    fin.readline()
    black_num = int(fin.readline().strip().split(":")[1])

    black_start_times = []
    black_end_times = []
    for i in range(black_num):
        parts = fin.readline().strip().split(",")
        cur_start_time = int(parts[0].split(":")[-1])
        cur_end_time = int(parts[1].split(":")[-1])
        black_start_times.append(cur_start_time)
        black_end_times.append(cur_end_time)
    return black_start_times, black_end_times

if __name__ == '__main__':
    search_dir = sys.argv[1]

    seq_start_time, seq_end_time = readSeqDuration(search_dir+"/mav0/summary_cut.txt")

    seq_duration = (seq_end_time - seq_start_time)/1e9

    img_black_start_times, img_black_end_times = readImgBlack(search_dir+"/mav0/summary_image.txt") 

    imu_black_start_times, imu_black_end_times = readIMUBlack(search_dir+"/mav0/summary_imu.txt")

    bk_width = 1000
    bk_height = 70
    bk_margin = 30
    img_bk_img = np.zeros([bk_height+bk_margin, bk_width, 3], np.uint8)+230
    img_bk_imu = np.zeros([bk_height+bk_margin, bk_width, 3], np.uint8)+230

    for i in range(len(img_black_start_times)):
        cur_start_time = img_black_start_times[i]
        cur_end_time = img_black_end_times[i]
        cur_duration = round((cur_end_time - cur_start_time)/1e9,2)
        
        cur_x = int(bk_width * (cur_start_time - seq_start_time)/(seq_end_time - seq_start_time))
        cur_width = int(bk_width * (cur_end_time - cur_start_time)/(seq_end_time - seq_start_time))

        img_bk_img = cv2.rectangle(img_bk_img, (cur_x, bk_margin),(cur_x+cur_width, bk_height+bk_margin),(53,130,84), -1)
        cv2.putText(img_bk_img, str(cur_duration)+" s", (int(cur_x+cur_width/2-25), int(bk_height+bk_margin-30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.putText(img_bk_img, "Vision Black", (int(bk_width/2)-80, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    for i in range(len(imu_black_start_times)):
        cur_start_time = imu_black_start_times[i]
        cur_end_time = imu_black_end_times[i]
        cur_duration = round((cur_end_time - cur_start_time)/1e9,2)
        
        cur_x = int(bk_width * (cur_start_time - seq_start_time)/(seq_end_time - seq_start_time))
        cur_width = int(bk_width * (cur_end_time - cur_start_time)/(seq_end_time - seq_start_time))

        img_bk_imu = cv2.rectangle(img_bk_imu, (cur_x, bk_margin),(cur_x+cur_width, bk_height+bk_margin),(182,117,46), -1)
        cv2.putText(img_bk_imu, str(cur_duration)+" s", (int(cur_x+cur_width/2-25), int(bk_height+bk_margin-30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


    cv2.putText(img_bk_imu, "IMU Black", (int(bk_width/2)-60, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    img_bk = np.vstack((img_bk_img, img_bk_imu))
    cv2.imwrite(search_dir+"/mav0/summary.png", img_bk)