from qing_operation import *
from collections import defaultdict
import getopt


class ImageCropper(object):
    """docstring for ImageCropper"""

    def __init__(self, workdir):
        super(ImageCropper, self).__init__()
        self.workdir = workdir
        self.frm_workdir = self.workdir + '/Humans_Frame'
        self.crop_workdir = self.workdir + '/Infos_crop_points'
        self.outdir  = self.frm_workdir + '_aligned'
        self.y_offset_fn = 'Y1-Y0.txt'
        qing_mkdir(self.outdir)

    def display(self):
        print('workdir:' , self.workdir)
        print('frm_workdir: ', self.frm_workdir)
        print('crop_workdir: ', self.crop_workdir)
        print('out_dir: ', self.outdir)
        print('y_offset_fn: ' , self.y_offset_fn)
        print('after initialization: ')
        print(self.frm_folders)
        print(self.crop_infos)

    def init(self):
        self.frm_folders = []
        self.crop_infos = []
        folder_content = sorted(os.listdir(self.frm_workdir))
        for f in folder_content:
            if f.startswith('.'):
                continue
            f_dir = self.frm_workdir + '/' + f
            self.frm_folders.append(f)
        folder_content = sorted(os.listdir(self.crop_workdir))
        for f in folder_content:
            f_dir = self.crop_workdir + '/' + f
            self.crop_infos.append(f)

    def read_in_y_offset(self):
        self.yoffset_dict = defaultdict(lambda: None)
        offset_fn = self.workdir + '/' + self.y_offset_fn
        with open(offset_fn) as f:
            for line in f:
                words = line.split(' ')
                self.yoffset_dict[words[0]] = int(words[1])

    def apply_y_offset(self):
        self.read_in_y_offset()
        print(self.yoffset_dict)

        for folder in self.frm_folders:
            if 'aligned_' in folder:
                continue

            folder_dir = self.frm_workdir + '/' + folder
            new_folder_dir = self.outdir + '/' + folder
            qing_mkdir(new_folder_dir)

            image_files = sorted(glob.glob(folder_dir + '/*.png'))
            image_cnt = len(image_files)
            print(folder_dir, '->', new_folder_dir)
            for idx in range(0, image_cnt, 2):
                f_0 = image_files[idx]
                f_1 = image_files[idx + 1]
                f_0_name = os.path.basename(f_0)
                f_1_name = os.path.basename(f_1)
                # print(idx, f_0, '<->', f_1)
                cam_0 = f_0_name[0:3]
                cam_1 = f_1_name[0:3]
                cam_key = cam_0 + cam_1
                y_offset = int(self.yoffset_dict[cam_key]) * -1
                print(cam_key, y_offset, f_0, f_1)

                image_0 = cv2.imread(f_0)
                image_1 = cv2.imread(f_1)

                new_f_0 = new_folder_dir + '/' + f_0_name
                new_f_1 = new_folder_dir + '/' + f_1_name

                # affine_matrx = np.empty([2,3],dtype = int)
                # print("affine_matrx: ", affine_matrx)
                # break
                rows, cols, nchannels = image_1.shape
                affine_matrix = np.float32([[1, 0, 0], [0, 1, y_offset]])
                if 0 == y_offset:
                    shutil.copy(f_0, new_f_0)
                    shutil.copy(f_1, new_f_1)
                    print('copy ', f_0, ' to ', new_f_0)
                    print('copy ', f_1, ' to ', new_f_1)
                else:
                    print(affine_matrix)
                    new_image_1 = cv2.warpAffine(
                        image_1, affine_matrix, (cols, rows))
                    shutil.copy(f_0, new_f_0)
                    cv2.imwrite(new_f_1, new_image_1)
                    print('copy ', f_0, ' to ', new_f_0)
                    print('affine ', f_0, ' to ', new_f_0)

                # new_image_1 = cv2.warpAffine(image_1,affine_matrix,(cols,rows))

            break

        pass

        def crop_image(self):
        	pass


def main(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "hd:", ["dir="])
    except getopt.GetoptError:
        print('qing_image_cropper.py -d <workdir> ')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('1-classify-frame.py -d <workdir>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            workdir = arg

    qing_cropper = ImageCropper(workdir)
    qing_cropper.init()
    qing_cropper.display()
    qing_cropper.apply_y_offset()
    # qing_cropper.corp_image()


if __name__ == '__main__':
    main(sys.argv[1:])
