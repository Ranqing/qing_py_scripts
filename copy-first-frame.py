from qing_operation import *
from collections import defaultdict

now = datetime.datetime.now()


def copy_first_frame(workdir):
    folders = sorted(os.listdir(workdir))
    outdir = './human_first_frame'
    qing_mkdir(outdir)
    for f in folders:
        folder_path = workdir + f
        if not os.path.isdir(folder_path):
            continue
        files = sorted(glob.glob(folder_path + '/*.JPG'))
        src = files[0]
        filename = os.path.basename(src)
        dst = outdir + '/' + f + '_00_' + filename
        shutil.copy(src, dst)
        datetime = qing_read_exif(src,  QING_EXIT_DATETIME)
        print(src, dst, datetime)
        time = qing_str_to_time(str(datetime))
        datetime = qing_time_to_datetime(time)
        durtime = now - datetime
        print(datetime, durtime.seconds)
    pass


def main():
    workdir = '../raw_human/'
    copy_first_frame(workdir)
    pass

if __name__ == '__main__':
    main()
