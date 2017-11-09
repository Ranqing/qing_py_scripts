from qing_operation import *
from collections import defaultdict
import getopt
import copy


class RotateSheller(object):
    """docstring for RotateSheller: a class to generate rotate shell for each frame of each camera"""

    stand_cam_names = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08',
                       'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16',
                       'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08',
                       'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16',
                       'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08',
                       'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
                       'L01', 'L02', 'L03', 'L04', 'L05', 'L06', 'N03', 'N04',
                       'N05', 'N06', 'R01', 'R02', 'R03', 'R04', 'R05', 'R06']

    rotate_angles = [270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270,
                     270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270,
                     270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270,
                     270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270,
                     180, 180, 180, 180, 180, 180,   0,   0,   0,   0, 180, 180,
                     0,   0,   0,   0]

    stand_cam_idx_dict = defaultdict(lambda: None)

    @staticmethod
    def static_method_example():
        print("static_method")

    @classmethod
    def class_method_example(cls):
        print("class method")

    def __init__(self, camdir, workdir):
        super(RotateSheller, self).__init__()
        self.camdir = camdir           # cams directory
        self.frmdir = workdir          # frames directory

    @classmethod
    def get_cam_idx_dict(cls):
        for idx, cam in enumerate(RotateSheller.stand_cam_names):
            RotateSheller.stand_cam_idx_dict[cam] = idx

    def display(self):
        print('cameras directory: ', self.camdir)
        print('frames directory: ', self.frmdir)
        print('standard cameras: ', self.stand_cam_names)
        print('standard camera-idx dict: ', self.stand_cam_idx_dict)

    def get_num_of_frms(self):
        if not os.path.isdir(self.frmdir):
            self.frm_num = 0
            print('no classified frames directory.',
                  str(self.frm_num) + ' frames.')
            sys.exit()
        else:
            frame_names = sorted(os.listdir(self.frmdir))
            if frame_names[0].startswith('.'):
                self.frame_names = copy.deepcopy(frame_names[1:])
            else:
                self.frame_names = copy.deepcopy(frame_names)
            self.frm_num = len(self.frame_names)
            print('frames directory: ', self.frmdir,
                  str(self.frm_num) + ' frames.')

    def get_num_of_cams(self):
        self.frm_files_vec = []
        if not os.path.isdir(self.camdir):
            if 0 == self.frm_num:
                self.get_num_of_frms()
            max_num_of_files = 0
            for frm_idx, frm_name in enumerate(self.frame_names):
                frm_dir = self.frmdir + '/' + frm_name
                frm_files = sorted(glob.glob(frm_dir + '/*.JPG'))
                frm_num_of_files = len(frm_files)
                self.frm_files_vec.append(frm_files)
                if frm_num_of_files > max_num_of_files:
                    max_num_of_files = frm_num_of_files
            self.cam_num = max_num_of_files
            print('no cameras diectory. number of cameras equal to max number of files.', str(
                self.cam_num) + ' cameras.')
        else:
            cam_names_in_dir = sorted(os.listdir(self.camdir))
            if cam_names_in_dir[0].startswith('.'):
                self.cam_names = copy.deepcopy(cam_names_in_dir[1:])
                self.cam_num = len(self.cam_names)
            else:
                self.cam_names = copy.deepcopy(cam_names_in_dir)
                self.cam_num = len(self.cam_names)
            print('cameras directory: ', self.camdir,
                  str(self.cam_num) + ' cameras.')

    def generate_rotate_shells_frame(self):
        self.shells_dir = self.frmdir + '_rotate_shells'
        self.rotate_dir = self.frmdir + '_rotated'
        qing_mkdir(self.shells_dir)
        qing_mkdir(self.rotate_dir)

        self.shells_names_vec = []
        # self.run_shell_filename = '../run_rotate_' + os.path.basename(self.frmdir) + '.sh'
        # print(self.run_shell_filename)

        self.get_num_of_frms()
        self.get_num_of_cams()

        for frm_idx, frm_name in enumerate(self.frame_names):
            frm_dir = self.frmdir + '/' + frm_name
            frm_files = self.frm_files_vec[frm_idx]
            frm_len = len(frm_files)

            if frm_len != self.cam_num:
                print(frm_name, '%d files. not complete.' % (frm_len))
                continue

            frm_shell_name = self.shells_dir + '/' + frm_name + '.sh'
            new_frm_dir = self.rotate_dir + '/' + frm_name
            qing_mkdir(new_frm_dir)
            print(frm_name, frm_shell_name, new_frm_dir)

            cmd_strs = []
            for idx, frm_file in enumerate(frm_files):
                frm_file_basename = os.path.basename(frm_file)
                cam_name = frm_file_basename[:3]
                cam_idx = RotateSheller.stand_cam_idx_dict[cam_name]
                rotate_angle = RotateSheller.rotate_angles[cam_idx]

                new_frm_file = new_frm_dir + '/' + frm_file_basename
                if 0 == rotate_angle:
                    command = 'cp ' + frm_file[1:] + \
                        ' ' + new_frm_file[1:] + '\n'
                else:
                    command = 'convert -rotate %d' % (
                        rotate_angle) + ' ' + frm_file[1:] + ' ' + new_frm_file[1:] + '\n'
                # print(frm_file, cam_name, cam_idx, rotate_angle)
                # print(command)
                cmd_strs.append(command)

            qing_write_strings_into_file(frm_shell_name, cmd_strs)
            self.shells_names_vec.append('sh ' + frm_shell_name[1:] + '\n')

        self.workdir = self.frmdir
        pass

    def generate_run_rotate_shell(self):
        run_shell_filename = '../run_rotate_' + \
            os.path.basename(self.workdir) + '.sh'
        qing_write_strings_into_file(run_shell_filename, self.shells_names_vec)
        print('generating ' + run_shell_filename + ' done.')
        # for idx, content in enumerate(self.shells_names_vec):
        # 	print(idx, content)

    def generate_rotate_shells_camera(self):
        self.shells_dir = self.camdir + '_rotate_shells'
        self.rotate_dir = self.camdir + '_rotated'
        qing_mkdir(self.shells_dir)
        qing_mkdir(self.rotate_dir)

        self.get_num_of_cams()
        self.shells_names_vec = []

        for cam_idx, cam_name in enumerate(self.cam_names):
            cam_dir = self.camdir + '/' + cam_name
            rotate_angle = self.rotate_angles[cam_idx]
            shell_name = self.shells_dir + '/' + cam_name + '.sh'
            new_cam_dir = self.rotate_dir + '/' + cam_name
            qing_mkdir(new_cam_dir)

            print(cam_name, shell_name, new_cam_dir)
            files = sorted(glob.glob(cam_dir + '/*.JPG'))
            cmd_strs = []
            for idx, file in enumerate(files):
                file_basename = os.path.basename(file)
                new_file = new_cam_dir + '/' + file_basename
                if 0 == rotate_angle:
                    command = 'cp ' + file[1:] + ' ' + new_file[1:] + '\n'
                else:
                    command = 'convert -rotate %d' % (rotate_angle) + ' ' + file[
                        1:] + ' ' + new_file[1:] + '\n'
                cmd_strs.append(command)
            qing_write_strings_into_file(shell_name, cmd_strs)
            self.shells_names_vec.append('sh ' + shell_name[1:] + '\n')

        self.workdir = self.camdir
        pass

# "cmd": ["python", "$file", "-c", "../Humans_one", "-d", "../Humans_one_frame"]
def main(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "hc:d:", ["help", "cam=", "dir="])
    except getopt.GetoptError:
        print('3-generate-rotate-shell-for-frame.py -c <camdir> -d <workdir> ')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('3-generate-rotate-shell-for-frame.py -c <camdir> -d <workdir>')
            sys.exit()
        elif opt in ("-c", "--cam"):
            camdir = arg
        elif opt in ("-d", "--dir"):
            workdir = arg

    RotateSheller.get_cam_idx_dict()
    qing_rotate_sheller = RotateSheller(camdir, workdir)
    # qing_rotate_sheller.display()
    qing_rotate_sheller.generate_rotate_shells_frame()
    # qing_rotate_sheller.generate_rotate_shells_camera()
    qing_rotate_sheller.generate_run_rotate_shell()


if __name__ == '__main__':
    main(sys.argv[1:])
