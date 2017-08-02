import sys
import os
import glob


def check_num(workdir):
    sub_dirs = sorted(os.listdir(workdir))
    for sd in sub_dirs:
        sd_path = workdir + '/' + sd
        if not os.path.isdir(sd_path):
            continue
        cr2_files = glob.glob(sd_path + '/*.CR2')
        jpg_files = glob.glob(sd_path + '/*.JPG')
        if(len(cr2_files) == len(jpg_files)):
            print(sd, len(cr2_files), len(jpg_files))
        else:
            print(sd, sub_dirs[i], sub_dirs[i + 1],
                  len(l_jpg_files), len(r_jpg_files), 'not')


def main():
    workdir = '../Humans_frame'
    check_num(workdir)

if __name__ == '__main__':
    main()
