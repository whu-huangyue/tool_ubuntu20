import sys
from HaveFun import common
import cv2
import os

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

if __name__ == '__main__':
    search_dir = sys.argv[1]

    num_black = int(sys.argv[2])

    if len(sys.argv) != 2 + num_black*2 + 1:
        print("wrong parameters, please check")
        exit()

    black_start_times = []
    black_end_times = []
    black_duration = []
    for i in range(1,num_black*2,2):
        tmp_black_start_time = int(sys.argv[2+i])
        tmp_black_end_time = int(sys.argv[2+i+1])
        black_start_times.append(tmp_black_start_time)
        black_end_times.append(tmp_black_end_time)
        black_duration.append((tmp_black_end_time-tmp_black_start_time)/1e9)
    
    print("\nSummary Info:")
    print("Input Dir:", search_dir)
    print("Black Segment(s):")
    for i in range(len(black_start_times)):
        print("Segment ", i, ": start time:",black_start_times[i],", end time:", black_end_times[i], ", duration(sec):",black_duration[i])
    
    rst = input("\ncontinue?[y]/n")
    if rst == "" or rst == "y" or rst == "Y" or rst == "Yes" or rst == "YES":
        print("continue")
    else:
        exit()

    new_paths, new_names, new_files = common.findFiles(search_dir+"/mav0/cam0/data", ".png")
    new_paths1, new_names1, new_files1 = common.findFiles(search_dir+"/mav0/cam1/data", ".png")

    seq_duration = (int(new_names[-1].split(".")[0]) - int(new_names[0].split(".")[0]))/1e9

    for i in range(len(new_files)):
        cur_ts = int(new_names[i].split(".")[0])
        black_flag = False
        for j in range(len(black_start_times)):
            if black_start_times[j] <= cur_ts <= black_end_times[j]:
                black_flag = True
                continue
        if black_flag:
            cur_img = cv2.imread(new_files[i])
            cur_img[:,:,:] = 0
            cv2.imwrite(new_files[i], cur_img)
            cur_img = cv2.imread(new_files1[i])
            cur_img[:,:,:] = 0
            cv2.imwrite(new_files1[i], cur_img)
            
    
    fout_summary = open(search_dir+"/mav0/summary_image.txt", "w")
    fout_summary.write("Input Dir:" + search_dir + "\n")
    fout_summary.write("Number of Black Segments:" + str(len(black_start_times)) + "\n")
    for i in range(len(black_start_times)):
        fout_summary.write("Segment " + str(i).zfill(2) + ": start time:" + str(black_start_times[i]) + ", end time:" + str(black_end_times[i]) + ", duration(sec):" + str(black_duration[i]) + ", percent:" + str(round(100*black_duration[i]/seq_duration)) + "\n")
    
    fout_summary.close()