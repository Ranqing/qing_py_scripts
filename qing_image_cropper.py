from qing_operation import *
from collections import defaultdict
import getopt

# FRM_id
# frame_or_mask


class ImageCropper(object):
    """docstring for ImageCropper"""

    def __init__(self, workdir, frameid):
        super(ImageCropper, self).__init__()
        self.workdir = workdir
        self.frameid = frameid
        self.frm_workdir = self.workdir + '/Rectified_Humans_frame'
        self.msk_workdir = self.workdir + '/Rectified_Humans_mask'
        self.crp_workdir = self.workdir + '/Infos_crop_points'
        self.aligned_frm_out_dir = self.frm_workdir + '_aligned'
        self.aligned_msk_out_dir = self.msk_workdir + '_aligned'
        qing_mkdir(self.aligned_frm_out_dir)
        qing_mkdir(self.aligned_msk_out_dir)
        self.y_offset_fn = 'Y1-Y0-' + self.frameid + '.txt'
        self.is_initial = False

    def display(self):
        print('workdir:', self.workdir)
        print('frm_workdir: ', self.frm_workdir)
        print('msk_workdir: ', self.msk_workdir)
        print('crp_workdir: ', self.crp_workdir)
        print('aligned_out_frm_dir: ', self.aligned_frm_out_dir)
        print('aligned_out_msk_dir: ', self.aligned_msk_out_dir)
        print('y_offset_fn: ', self.y_offset_fn)
        if self.is_initial == False:
            pass
        else:
            print(self.frm_folders)
            print(self.msk_folders)
            print(self.crp_info_fns)

    def init(self):
        self.frm_folders = []
        self.msk_folders = []
        self.crp_info_fns = []
        if os.path.isdir(self.frm_workdir):
            folder_content = sorted(os.listdir(self.frm_workdir))
            for f in folder_content:
                if f.startswith('.'):
                    continue
                f_dir = self.frm_workdir + '/' + f
                self.frm_folders.append(f)
        if os.path.isdir(self.msk_workdir):
            folder_content = sorted(os.listdir(self.msk_workdir))
            for f in folder_content:
                if f.startswith('.'):
                    continue
                f_dir = self.msk_workdir + '/' + f
                self.msk_folders.append(f)
        # if os.path.isdir(self.crp_workdir):
        #     crp_files =
        #     folder_content = sorted(os.listdir(self.crp_workdir))
        #     for f in folder_content:
        #         f_dir = self.crp_workdir + '/' + f
        #         self.crp_info_fns.append(f)
        if os.path.isdir(self.crp_workdir):
            self.crp_info_fns = sorted(glob.glob(self.crp_workdir + '/*.txt'))

        self.is_initial = True
        self.frm_files = []
        self.frm_cnt = 0
        self.msk_files = []
        self.msk_cnt = []
        pass

    def read_in_y_offset(self):
        self.yoffset_dict = defaultdict(lambda: None)
        offset_fn = self.workdir + '/' + self.y_offset_fn
        with open(offset_fn) as f:
            for line in f:
                words = line.split(' ')
                self.yoffset_dict[words[0]] = int(words[1])
        print(self.yoffset_dict)

    def apply_y_offset_to_frm(self):
        self.read_in_y_offset()

        new_frm_dir = self.aligned_frm_out_dir + '/FRM_' + self.frameid
        new_msk_dir = self.aligned_msk_out_dir + '/FRM_' + self.frameid
        qing_mkdir(new_frm_dir)
        qing_mkdir(new_msk_dir)

        frm_dir = self.frm_workdir + '/FRM_' + self.frameid
        self.frm_files = sorted(glob.glob(frm_dir + '/*.png'))
        self.frm_cnt = len(self.frm_files)
        print(self.frm_cnt)
        print(self.frm_files)
        print(frm_dir, '->', new_frm_dir)
        self.apply_offset(self.frm_files, self.frm_cnt, frm_dir, new_frm_dir)

        msk_dir = self.msk_workdir + '/FRM_' + self.frameid
        self.msk_files = sorted(glob.glob(msk_dir + '/*.png'))
        self.msk_cnt = len(self.msk_files)
        print(self.msk_cnt)
        print(self.msk_files)
        print(msk_dir, '->', new_msk_dir)
        self.apply_offset(self.msk_files, self.msk_cnt, msk_dir, new_msk_dir)

    def apply_offset_to_file(self, f, new_f, affine_matrix):
        print(affine_matrix)
       
        img = cv2.imread(f)
        rows, cols, nchannels = img.shape
        new_img = cv2.warpAffine(img, affine_matrix, (cols, rows))
        cv2.imwrite(new_f, new_img)

    def apply_offset(self, files, cnt, in_dir, out_dir):
        for idx in range(0, cnt, 2):
            f_0 = files[idx]
            f_1 = files[idx + 1]
            f_0_name = os.path.basename(f_0)
            f_1_name = os.path.basename(f_1)
            cam_0 = f_0_name[0:3]
            cam_1 = f_1_name[0:3]
            cam_key = cam_0 + cam_1
            y_offset = int(self.yoffset_dict[cam_key]) * -1
            print('\n' + cam_key, y_offset)

            new_f_0 = out_dir + '/' + f_0_name
            new_f_1 = out_dir + '/' + f_1_name
            if 0 == y_offset:
                print('copy ', f_0, ' to ', new_f_0)
                print('copy ', f_1, ' to ', new_f_1)
                shutil.copy(f_0, new_f_0)
                shutil.copy(f_1, new_f_1)

            else:
                print('copy ', f_0, ' to ', new_f_0)
                print('affine  ', f_1, ' to ', new_f_1)
                affine_matrix = np.float32([[1, 0, 0], [0, 1, y_offset]])
                shutil.copy(f_0, new_f_0)
                self.apply_offset_to_file(f_1, new_f_1, affine_matrix)

    def crop_image_to_frm(self):
        self.cropped_frm_out_dir = self.aligned_frm_out_dir + '_cropped'
        qing_mkdir(self.cropped_frm_out_dir)
        crop_out_dir = self.cropped_frm_out_dir + '/FRM_' + self.frameid
        qing_mkdir(crop_out_dir)
        crop_fn = self.crp_workdir + '/crop_infos_frm_' + self.frameid + '.txt'
        print(crop_fn)
        print(crop_out_dir)

        in_frm_dir = self.workdir + '/FRM_' + self.frameid

        if 0 == self.frm_cnt:

            if os.path.isdir(self.aligned_frm_out_dir):
                in_frm_dir = self.aligned_frm_out_dir + '/FRM_' + self.frameid
                files = sorted(glob.glob(in_frm_dir + '/*.png'))
                if 0 == len(files):
                    in_frm_dir = self.frm_workdir + '/FRM_' + self.frameid

        print('in-frm_dir:', in_frm_dir)
        self.frm_files = sorted(glob.glob(in_frm_dir + '/*.png'))
        self.frm_cnt = len(self.frm_files)
        print(self.frm_files)
        print(self.frm_cnt)

        crop_points, crop_sizes = qing_read_crop_infos(crop_fn)
        print('crop_points: ', crop_points)
        print('crop_sizes: ', crop_sizes)
        for idx in range(0, self.frm_cnt, 2):
            fn_0 = self.frm_files[idx]
            fn_1 = self.frm_files[idx + 1]

            f_basename_0 = os.path.basename(fn_0)
            f_basename_1 = os.path.basename(fn_1)

            out_fn_0 = crop_out_dir + '/' + f_basename_0
            out_fn_1 = crop_out_dir + '/' + f_basename_1
            crop_pt_0 = crop_points[idx]
            crop_pt_1 = crop_points[idx + 1]
            crop_sz_0 = crop_sizes[idx]
            crop_sz_1 = crop_sizes[idx + 1]
            if crop_pt_0[1] != crop_pt_1[1]:
                print(self.frameid, f_basename_0,
                      f_basename_1, 'wrong crop points')
                continue
            if crop_sz_0 != crop_sz_1:
                print(self.frameid, f_basename_0,
                      f_basename_1, 'wrong crop sizes')
                continue

            mtx_0 = cv2.imread(fn_0)
            crop_mtx_0 = qing_crop_a_image(mtx_0, crop_pt_0, crop_sz_0)
            cv2.imwrite(out_fn_0, crop_mtx_0)
            mtx_1 = cv2.imread(fn_1)
            crop_mtx_1 = qing_crop_a_image(mtx_1, crop_pt_1, crop_sz_1)
            cv2.imwrite(out_fn_1, crop_mtx_1)
            print(fn_0, '->', out_fn_0, crop_pt_0,
                  crop_sz_0, mtx_0.shape, crop_mtx_0.shape)
            print(fn_1, '->', out_fn_1, crop_pt_1,
                  crop_sz_1, mtx_1.shape, crop_mtx_1.shape)


def main(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "hd:f:", ["help", "dir=", "frm="])
    except getopt.GetoptError:
        print('qing_image_cropper.py -d <workdir> -f <frameid>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('qing_image_cropper.py -d <workdir> -f <frameid>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            workdir = arg
        elif opt in ("-f", "--frm"):
            frameid = arg

    qing_cropper = ImageCropper(workdir, frameid)
    qing_cropper.init()
    qing_cropper.display()
    qing_cropper.apply_y_offset_to_frm()
    # qing_cropper.crop_image_to_frm()


if __name__ == '__main__':
    main(sys.argv[1:])
