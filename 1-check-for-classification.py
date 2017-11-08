from qing_operation import *


class ImageChecker(object):
    """docstring for ImageChecker: check number of cr2 files and first frames of each camera"""

    def __init__(self, workdir):
        super(ImageChecker, self).__init__()
        self.workdir = workdir

    def get_camera_names(self):
        cam_names = sorted(os.listdir(self.workdir))
        if cam_names[0].startswith('.'):
            self.cam_names = cam_names[1:]
        else:
            self.cam_names = cam_names
        print('%d cameras.' % (len(self.cam_names)))
        print(self.cam_names)

    def check_cr2_and_jpg_files(self):
        for cam in self.cam_names:
            cam_dir = self.workdir + '/' + cam
            num_cr2_files = len(glob.glob(cam_dir + '/*.CR2'))
            num_jpg_files = len(glob.glob(cam_dir + '/*.JPG'))

            if num_cr2_files == num_jpg_files:
                print('cam_dir : ', cam_dir, '%d cr2 files,' %
                      (num_cr2_files), '%d jpg files.' % (num_jpg_files))
            else:
                print('cam_dir : ', cam_dir, '%d cr2 files,' %
                      (num_cr2_files), '%d jpg files.' % (num_jpg_files), '!!!not!!!')

    def check_first_frame(self, first_frame_dir, first_frame_txt):
        qing_mkdir(first_frame_dir)
        outobj = open(first_frame_txt, 'w')

        for cam in self.cam_names:
            cam_dir = self.workdir + '/' + cam
            first_frame_name = sorted(glob.glob(cam_dir + '/*.JPG'))[0]
            first_frame_time = qing_str_to_datetime(
                str(qing_read_exif(first_frame_name, QING_EXIF_DATETIME)))
            first_frame_sec = qing_datetime_diff_seconds(first_frame_time)
            outstr = cam + '\t' + first_frame_name + '\t' + \
                str(first_frame_time) + '\t' + str(first_frame_sec) + '\n'
            outobj.write(outstr)
            new_first_frame_name = first_frame_dir + '/' + cam + \
                '_' + os.path.basename(first_frame_name)[:-4] + '_FRM_0000.JPG'
            shutil.copy(first_frame_name, new_first_frame_name)
            print('copy', new_first_frame_name)
        outobj.close()




def main():
    workdir = '../Humans_0'
    qing_checker = ImageChecker(workdir)
    qing_checker.get_camera_names()
    # qing_checker.check_cr2_and_jpg_files()
    first_frame_dir = workdir + '_first_frame'
    first_frame_txt = workdir + '_first_frame.txt'
    qing_checker.check_first_frame(first_frame_dir, first_frame_txt)


if __name__ == '__main__':
    main()
