import sys
import shutil
import os
from HaveFun import common

def readTXT(file_path):
    timestamps = []
    lines = []
    fin = open(file_path, "r")
    line = fin.readline()
    line = fin.readline()
    while line:
        tmp_ts = int(line.split(",")[0])
        timestamps.append(tmp_ts)
        lines.append(line)

        line = fin.readline()
    
    fin.close()
    return timestamps, lines

def readTimestamp(file_path):
    timestamps = []
    lines = []
    fin = open(file_path, "r")
    line = fin.readline()
    while line:
        tmp_ts = int(line)
        timestamps.append(tmp_ts)
        lines.append(line)

        line = fin.readline()
    
    fin.close()
    return timestamps, lines


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
    search_dir = sys.argv[1]
    output_dir = sys.argv[2]
    seq_start_time = int(sys.argv[3])
    seq_end_time = int(sys.argv[4])
    seq_duration = (seq_end_time - seq_start_time)/1e9

    
    print("\nSummary Info:")
    print("Input Dir:", search_dir)
    print("Output Dir:", output_dir)
    print("Subsequence Start Time(ns):", seq_start_time)
    print("Subsequence End Time(ns):", seq_end_time)
    print("Subsequence Duration(sec):", seq_duration)
    
    rst = input("\ncontinue?[y]/n")
    if rst == "" or rst == "y" or rst == "Y" or rst == "Yes" or rst == "YES":
        print("continue")
    else:
        print("exit")
    
    if search_dir != output_dir:
        print("\nCopying files ...")

        source_left_img_dir = search_dir + os.path.sep + "/mav0/cam0/data"
        source_right_img_dir = search_dir + os.path.sep + "/mav0/cam1/data"
        source_imu_path = search_dir + os.path.sep + "/mav0/imu0/data.csv"
        source_gt_path = search_dir + os.path.sep + "/mav0/state_groundtruth_estimate0/data.csv"
        source_ts_path = search_dir + os.path.sep + "/mav0/timestamps.txt"

        target_left_img_dir = output_dir + os.path.sep + "/mav0/cam0/data"
        target_right_img_dir = output_dir + os.path.sep + "/mav0/cam1/data"
        target_imu_path = output_dir + os.path.sep + "/mav0/imu0/data.csv"
        target_gt_path = output_dir + os.path.sep + "/mav0/state_groundtruth_estimate0/data.csv"
        target_ts_path = output_dir + os.path.sep + "/mav0/timestamps.txt"
        
        common.isDirExist(target_left_img_dir)
        common.isDirExist(target_right_img_dir)
        common.isDirExist(output_dir + os.path.sep + "/mav0/imu0")
        common.isDirExist(output_dir + os.path.sep + "/mav0/state_groundtruth_estimate0")


        imu_ts, imu_data = readTXT(source_imu_path)
        gt_ts, gt_data = readTXT(source_gt_path)
        ori_ts, ori_data = readTimestamp(source_ts_path)

        fout_imu = open(target_imu_path, "w")
        fout_gt = open(target_gt_path, "w")
        fout_ts = open(target_ts_path, "w")

        _, names, _ = common.findFiles(source_left_img_dir, ".png")
        process_files = []
        for i in range(len(names)):
            if seq_start_time <= int(names[i].split(".")[0]) <= seq_end_time:
                process_files.append(names[i])
                shutil.copy2(source_left_img_dir + "/" + names[i], target_left_img_dir+"/"+names[i])
                shutil.copy2(source_right_img_dir + "/" + names[i], target_right_img_dir+"/"+names[i])
        
        for i in range(len(imu_ts)):
            if seq_start_time-1 <= imu_ts[i] <= seq_end_time+1:
                fout_imu.write(imu_data[i])
        fout_imu.close()

        for i in range(len(gt_ts)):
            if seq_start_time-1 <= gt_ts[i] <= seq_end_time+1:
                fout_gt.write(gt_data[i])
        fout_gt.close()

        for i in range(len(ori_ts)):
            if seq_start_time <= ori_ts[i] <= seq_end_time:
                fout_ts.write(ori_data[i])
        fout_ts.close()
        print("Copied files!\n")
    
        fout_summary = open(output_dir + os.path.sep + "/mav0/summary_cut.txt", "w")
        fout_summary.write("Input Dir:" + search_dir + "\n")
        fout_summary.write("Output Dir:" + output_dir + "\n")
        fout_summary.write("Subsequence Start Time(ns):" + str(seq_start_time) + "\n")
        fout_summary.write("Subsequence End Time(ns):" + str(seq_end_time) + "\n")
        fout_summary.write("Subsequence Duration(sec):" + str(seq_duration) + "\n")
        fout_summary.write("Frame Number:" + str(len(process_files)) + "\n")
        fout_summary.close()