import sys
import os
import glob
import shutil

start_frm = 124


def check_num(dir):
    sub_dirs = sorted(os.listdir(dir))
    for sd in sub_dirs:
        sd_path = dir + sd
        if not os.path.isdir(sd_path):
            continue
        cr2_files = sorted(glob.glob(sd_path + '/*.CR2'))
        jpg_files = sorted(glob.glob(sd_path + '/*.JPG'))
        if(len(cr2_files) == len(jpg_files)):
            print(sd, len(cr2_files), len(jpg_files))

        for idx in range(0, len(cr2_files)):
            jpg_f = jpg_files[idx]
            cr2_f = cr2_files[idx]
            jpg_fname = os.path.basename(jpg_f)
            cr2_fname = os.path.basename(cr2_f)
            new_jpg_fname = jpg_fname[
                :-4] + ('_FRM_%04d' % (start_frm + idx)) + jpg_fname[-4:]
            new_cr2_fname = cr2_fname[
                :-4] + ('_FRM_%04d' % (start_frm + idx)) + cr2_fname[-4:]
            new_jpg_f = sd_path + '/' + new_jpg_fname
            new_cr2_f = sd_path + '/' + new_cr2_fname
            os.rename(jpg_f, new_jpg_f)
            print(jpg_f, new_jpg_f)
            os.rename(cr2_f, new_cr2_f)
            print(cr2_f, new_cr2_f)


def main():
    check_num('./')

if __name__ == '__main__':
    main()
