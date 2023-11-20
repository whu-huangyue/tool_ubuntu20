import sys

if __name__ == '__main__':
    path = sys.argv[1]  # 数据文件路径
    out_path = sys.argv[2]
    fin = open(path, 'r')
    l0s = []
    l1s = []
    l2s = []
    l3s = []
    l4s = []
    l5s = []
    l6s = []
    l7s = []

    line = fin.readline()
    while line:
        parts = line.split(" ")
        l0 = float(parts[0]) * 1000000000
        l1 = float(parts[1])
        l2 = float(parts[2])
        l3 = float(parts[3])
        l4 = float(parts[4])
        l5 = float(parts[5])
        l6 = float(parts[6])
        l7 = float(parts[7])

        l0s.append(l0)
        l1s.append(l1)
        l2s.append(l2)
        l3s.append(l3)
        l4s.append(l4)
        l5s.append(l5)
        l6s.append(l6)
        l7s.append(l7)

        line = fin.readline().strip()
    
    with open(out_path, 'w+') as f_out:
        for i in range(len(l0s)):
            print('zhuanhuan: ', i+1 , '/' , len(l0s))
            f_out.write("{:.6f}".format(l0s[i]) + ' ')
            f_out.write("{:.9f}".format(l1s[i]) + ' ')
            f_out.write("{:.9f}".format(l2s[i]) + ' ')
            f_out.write("{:.9f}".format(l3s[i]) + ' ')
            f_out.write("{:.9f}".format(l4s[i]) + ' ')
            f_out.write("{:.9f}".format(l5s[i]) + ' ')
            f_out.write("{:.9f}".format(l6s[i]) + ' ')
            f_out.write("{:.9f}".format(l7s[i]) + '\n')
            # f_out.write(' ' + str(l1s[i]) + ' ' + str(l2s[i]) + ' ' + str(l3s[i]) + ' ' + str(l4s[i]) + ' ' + str(l5s[i]) + ' ' + str(l6s[i]) + ' ' + str(l7s[i]) + '\n')
