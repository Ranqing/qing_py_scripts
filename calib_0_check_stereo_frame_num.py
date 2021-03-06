import sys
import os
import glob
import getopt

# run : "cmd": ["python", "$file", "-d", "../Calib"]
# check number of jpg files between stereo cameras for calibration
def check_num_between_stereo_cams(workdir):
    sub_dirs = sorted(os.listdir(workdir))

    folder_idx = -1
    for idx, sd in enumerate(sub_dirs):
        folder_path = workdir + '/' + sd
        if not os.path.isdir(folder_path):
            continue
        folder_idx = folder_idx + 1

        if folder_idx % 2 == 0:
            cam_0 = sub_dirs[idx]
            cam_1 = sub_dirs[idx + 1]
            sd_path_0 = workdir + '/' + cam_0
            sd_path_1 = workdir + '/' + cam_1
        else:
            continue

        jpg_files_0 = glob.glob(sd_path_0 + '/*.JPG')
        jpg_files_1 = glob.glob(sd_path_1 + '/*.JPG')
        if(len(jpg_files_0) == len(jpg_files_1)):
            print(cam_0, len(jpg_files_0), cam_1, len(jpg_files_1))
        else:
            print(cam_0, len(jpg_files_0), cam_1, len(jpg_files_1), 'not')


def main(argv):
    # print argv
    try:
        opts, args = getopt.getopt(argv, "hd:", ["dir="])
    except getopt.GetoptError:
        print('3-check-frame-num.py -d <workdir> ')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('3-check-frame-num.py -d <workdir>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            workdir = arg
        print('workdir =  ', workdir)

    check_num(workdir)

if __name__ == '__main__':
    main(sys.argv[1:])
