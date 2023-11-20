import cv2

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
        if timestamp >= 1403636957000000000 and timestamp <= 1403636959000000000:
         timestamps.append(timestamp)
         filenames.append(filename)
        line = fin.readline().strip()
    return filenames, timestamps

if __name__ == '__main__':
    path = "/home/hy/下载/Sequence73/mav0/cam1/data.csv"
    filenames, timestamps = readDescription(path)
    print(len(timestamps))

    # imagepath = "/home/hy/下载/MH_03黑5s/MH_03_medium/mav0/cam0/data/" + filenames[0]
    # print(imagepath)
    # img1 = cv2.imread(imagepath)
    # img1[:,:] = 0
    # # cv2.imshow("test!", img1)
    # # cv2.waitKey()
    # cv2.imwrite(imagepath, img1)

    
    for i in range(len(filenames)):
        imagepath = "/home/hy/下载/Sequence73/mav0/cam1/data/" + filenames[i]
        img1 = cv2.imread(imagepath)
        img1[:,:] = 0
        cv2.imwrite(imagepath, img1)
