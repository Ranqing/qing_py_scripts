from qing_operation import *
from collections import defaultdict
from datetime import datetime, timedelta
import getopt
import copy

# get datetime from exif info and the datetime saved in a dict data-structure


def get_files_datetime(folder_path):
    # add for 20171018/Humans_one: L01,L02
    cam_name = os.path.basename(folder_path)
    manual_frm_idx = 3
    manual_interval = 51
    # end

    files = sorted(glob.glob(folder_path + '/*.JPG'))
    # fdict = {}
    fdict = defaultdict(lambda: None)
    for frm_idx, f in enumerate(files):
        ftime = qing_read_exif(f, QING_EXIF_DATETIME)
        fdatetime = qing_str_to_datetime(str(ftime))

        if cam_name == 'L01' or cam_name == 'L02':
            if frm_idx >= manual_frm_idx:
                fdatetime = fdatetime + timedelta(seconds=manual_interval)
        fdict[f] = fdatetime
    return fdict


def traverse_datetime_infos(file_times_dict):
    size = len(file_times_dict)
    file_times_vec = []
    for times in file_times_dict:
        times_vec = qing_traverse_dict_to_vec(times, 1)
        file_times_vec.append(times_vec)
    return file_times_vec


class ImageClassifier(object):
    """ImageClassifier"""
    # bench_type = 0        # earliest camera
    # bench_type = 1        # most and earliest camera

    CR2 = True

    def __init__(self, workdir):
        super(ImageClassifier, self).__init__()
        self.workdir = workdir

    def display(self):
        print('Image Classifier workdir :' + self.workdir +
              '.\t' + str(self.cam_num) + ' cameras.')
        print(self.cam_names)
        pass

    def ret_frm_names(self, cam_idx):
        return self.frames_names_vec[cam_idx]

    def get_cameras(self):
        cam_names = sorted(os.listdir(self.workdir))
        if cam_names[0].startswith('.'):
            self.cam_names = cam_names[1:]
        else:
            self.cam_names = cam_names
        self.cam_num = len(self.cam_names)

    def save_names_and_datetimes(self):
        tempfile = self.workdir + '_all_times.txt'
        tempobj = open(tempfile, 'w')
        for cam_idx, frame_dict in enumerate(self.frames_times_dict):
            tempobj.write(self.cam_names[cam_idx] + '\t' +
                          str(len(frame_dict)) + ' files' + '\n')
            for frm_idx, frm_pair in enumerate(frame_dict):
                frm_sec = qing_datetime_diff_seconds(frm_pair[1])
                # frm_interval = frm_sec - self.first_frame_secs[cam_idx]
                frm_interval = frm_sec - self.first_frame_secs[cam_idx]
                tempobj.write(frm_pair[0] + '\t' + str(frm_pair[1]) +
                              '\t' + str(frm_sec) + '\t' + str(frm_interval) + '\n')
            tempobj.write('\n')
        print('saving ' + tempfile)

    def get_frames_names_and_datetimes(self):
        self.frames_names_vec = []            # frame names vector of each camera
        self.frames_times_dict = []           # list of frame names and datetimes pair
        self.first_frame_secs = []            # first frame seconds vector
        # empty dictionary: camera_name <-> first_frame_sec
        self.first_frame_secs_dict = {}

        print('get_frame_names_and_datetimes:')
        for idx, f in enumerate(self.cam_names):
            cam_dir = self.workdir + '/' + f
            print(cam_dir)
            if not os.path.isdir(cam_dir):
                continue

            names_vec = sorted(glob.glob(cam_dir + '/*.JPG'))
            times_dict = qing_sort_dict(get_files_datetime(cam_dir), 0)

            self.frames_names_vec.append(names_vec)
            self.frames_times_dict.append(times_dict)

        # print log to check
        print('get_frames_names_and_datetimes: ')
        for cam_idx, frame_dict in enumerate(self.frames_times_dict):
            cam_name = self.cam_names[cam_idx]
            firstsec = qing_datetime_diff_seconds(frame_dict[0][1])
            # add for 20171018/Humans_one
            manual_first_sec_offset = -150
            if cam_name == 'C15' or cam_name == 'C16':
                firstsec = firstsec + manual_first_sec_offset  # check by human
            # end

            self.first_frame_secs.append(firstsec)
            self.first_frame_secs_dict[self.cam_names[cam_idx]] = firstsec
            print(self.cam_names[cam_idx], '%d files' % len(frame_dict), frame_dict[
                  0][0],  frame_dict[0][1], self.first_frame_secs[-1])

        self.save_names_and_datetimes()
        # sys.exit(1)
        # self.calc_classified_result_gt()

    def get_earliest_camera(self):
        self.bench_cam_idx = 0
        self.bench_first_sec = self.first_frame_secs[0]

        for cam_idx, first_sec in enumerate(self.first_frame_secs):
            if first_sec < self.bench_first_sec:
                self.bench_cam_idx = cam_idx
                self.bench_first_sec = first_sec
        self.bench_frm_idx = 0
        self.bench_frm_num = len(self.frames_names_vec[self.bench_cam_idx])
        print('\nafter get earliest camera:')
        print('bench_cam_idx = ', self.bench_cam_idx, ', bench_cam_name = ', self.cam_names[self.bench_cam_idx],
              ', bench_first_sec = ', self.bench_first_sec, ', bench_frm_num = ', self.bench_frm_num)

        pass

    def get_most_and_earliest_camera(self):
        self.bench_cam_idx = 0
        self.bench_first_sec = self.first_frame_secs[0]
        self.bench_frm_num = len(self.frames_names_vec[0])

        print('\nbefore:')
        print('bench_cam_idx = ', self.bench_cam_idx, ', bench_cam_name = ', self.cam_names[
              self.bench_cam_idx], ', bench_first_sec = ', self.first_frame_secs[self.bench_cam_idx],
              ', bench_frm_num = ', self.bench_frm_num)

        for cam_idx, frame_names in enumerate(self.frames_names_vec):
            frm_num = len(frame_names)
            first_sec = self.first_frame_secs[cam_idx]

            if frm_num > self.bench_frm_num:
                self.bench_frm_num = frm_num
                self.bench_cam_idx = cam_idx
                self.bench_first_sec = first_sec
            elif frm_num == self.bench_frm_num:
                if first_sec <= self.bench_first_sec:
                    self.bench_frm_num = frm_num
                    self.bench_cam_idx = cam_idx
                    self.bench_first_sec = first_sec

        self.bench_frm_idx = 0
        print('after get most and earliest camera:')
        print('bench_cam_idx = ', self.bench_cam_idx, ', bench_cam_name = ', self.cam_names[self.bench_cam_idx],
              ', bench_first_sec = ', self.bench_first_sec, ', bench_frm_num = ', self.bench_frm_num)

    def get_same_time_frame_between(self, bench_frame_sec):
        epsilon = 1.0
        same_frame_dict = []

        for idx, frame_dict in enumerate(self.frames_times_dict):
            frame_sec = qing_datetime_diff_seconds(frame_dict[0][1])
            frame_interval = frame_sec - bench_frame_sec
            interval_threshold = self.bench_frame_intervals[idx]

            if abs(frame_interval - interval_threshold) <= epsilon:
                same_frame_dict.append(frame_dict[0])
                frame_dict.remove(frame_dict[0])
            elif frame_interval - interval_threshold < -epsilon:
                while(len(frame_dict)):
                    ttt_frame_sec = qing_datetime_diff_seconds(
                        frame_dict[0][1])
                    ttt_frame_interval = ttt_frame_sec - bench_frame_sec
                    if abs(ttt_frame_interval - interval_threshold) <= epsilon:
                        same_frame_dict.append(frame_dict[0])
                        frame_dict.remove(frame_dict[0])
                        break
                    elif ttt_frame_interval - interval_threshold < -epsilon:
                        frame_dict.remove(frame_dict[0])
                    elif ttt_frame_interval - interval_threshold > epsilon:
                        break
            elif frame_interval - interval_threshold > epsilon:
                continue

        return same_frame_dict
        pass

    def calc_bench_frm_intervals(self):
        print('calculate bench frame intervals between cameras')
        self.bench_frame_intervals = []
        for cam_idx, frame_dict in enumerate(self.frames_times_dict):
            cur_bench_frame_sec = qing_datetime_diff_seconds(
                frame_dict[self.bench_frm_idx][1])
            self.bench_frame_intervals.append(
                cur_bench_frame_sec - self.bench_first_sec)
            print(self.cam_names[cam_idx], self.bench_frame_intervals[-1])

    def classify_via_intervals_between_cameras(self, result_file):
        outobj = open(result_file, 'w')
        self.calc_bench_frm_intervals()
        self.classified_results = []

        print('frames in bench camera', self.cam_names[
              self.bench_cam_idx], ': ')
        for frm_idx, frame_time in enumerate(self.frames_times_vec[self.bench_cam_idx]):
            bench_cur_frm_sec = qing_datetime_diff_seconds(frame_time)
            same_frame_dict = self.get_same_time_frame_between(
                bench_cur_frm_sec)

            out_str = 'FRM_%04d' % (frm_idx) + '\tinterval = %d' % (
                bench_cur_frm_sec) + '\t%d files' % (len(same_frame_dict))
            print(out_str)
            outobj.write(out_str + '\n')

            same_frame_names = []
            for f in same_frame_dict:
                f_name = f[0]
                f_interval = qing_datetime_diff_seconds(f[1])
                same_frame_names.append(f_name)
                print(f_name)
                outobj.write(f_name + '\t' +
                             str(f[1]) + '\t' + str(f_interval) + '\n')
            self.classified_results.append(same_frame_names)
            print()
            outobj.write('\n')
        outobj.close()
        pass

    def get_same_time_frame_within(self, bench_cur_frm_interval):
        epsilon = 3.0
        same_frame_dict = []
        missed_cams_list = []

        for cam_idx, frame_dict in enumerate(self.frames_times_dict):
            is_cam_missed = True
            cur_frm_interval = qing_datetime_diff_seconds(
                frame_dict[0][1]) - self.bench_frame_secs[cam_idx]
            if abs(cur_frm_interval - bench_cur_frm_interval) <= epsilon:
                same_frame_dict.append(frame_dict[0])
                is_cam_missed = False
                frame_dict.remove(frame_dict[0])
            elif cur_frm_interval - bench_cur_frm_interval < -epsilon:
                frame_dict.remove(frame_dict[0])
                while len(frame_dict):
                    ttt_cur_frm_interval = qing_datetime_diff_seconds(
                        frame_dict[0][1]) - self.bench_frame_secs[cam_idx]
                    if abs(ttt_cur_frm_interval - bench_cur_frm_interval) <= epsilon:
                        same_frame_dict.append(frame_dict[0])
                        is_cam_missed = False
                        frame_dict.remove(frame_dict[0])
                        break
                    elif ttt_cur_frm_interval - bench_cur_frm_interval < -epsilon:
                        frame_dict.remove(frame_dict[0])
                    elif ttt_cur_frm_interval - bench_cur_frm_interval > epsilon:
                        break
            elif cur_frm_interval - bench_cur_frm_interval > epsilon:
                pass

            if is_cam_missed:
                missed_cams_list.append(self.cam_names[cam_idx])

        return same_frame_dict, missed_cams_list
        pass

    def calc_bench_frame_secs(self):
        print('calculate bench frame seconds within each camera')
        self.bench_frame_secs = copy.deepcopy(self.first_frame_secs)
        # self.bench_frame_secs = []  # i.e. frame secs of first frame of each camera.
        # for cam_idx, frame_times in enumerate(self.frames_times_vec):
        #     cam_name = self.cam_names[cam_idx]
        #     frame_sec = qing_datetime_diff_seconds(
        #         frame_times[self.bench_frm_idx])

        #     # add for 20171018/Humans_one
        #     if cam_name == 'C15' or cam_name == 'C16':
        #         frame_sec = frame_sec - 150
        #     # end
        #     self.bench_frame_secs.append(frame_sec)

    def classify_via_intervals_within_cameras(self, result_file):
        outobj = open(result_file, 'w')
        self.classified_results = []
        self.missed_cameras = []
        self.calc_bench_frame_secs()

        print('frames in bench camera', self.cam_names[
              self.bench_cam_idx], ': ')

        for frm_idx, frame_time in enumerate(self.frames_times_vec[self.bench_cam_idx]):
            bench_cur_frm_interval = qing_datetime_diff_seconds(
                frame_time) - self.bench_frame_secs[self.bench_cam_idx]
            same_frame_dict, missed_cams_list = self.get_same_time_frame_within(
                bench_cur_frm_interval)

            out_str = 'FRM_%04d' % (frm_idx) + '\tinterval = %d' % (
                bench_cur_frm_interval) + '\t%d files' % (len(same_frame_dict))
            if len(missed_cams_list):
                out_str = out_str + '\n'
                for m_cam in missed_cams_list:
                    out_str = out_str + m_cam + '\t'
            print(out_str)
            outobj.write(out_str + '\n')

            same_frame_names = []
            for f in same_frame_dict:
                f_name = f[0]
                c_name = f_name[-16:-13]
                f_interval = qing_datetime_diff_seconds(f[1])
                f_interval_within = f_interval - \
                    self.first_frame_secs_dict[c_name]
                same_frame_names.append(f_name)
                print(f_name + '\t' + str(f_interval_within))
                outobj.write(f_name + '\t' +
                             str(f[1]) + '\t' + str(f_interval) + '\t' + str(f_interval_within) + '\n')
            self.classified_results.append(same_frame_names)
            self.missed_cameras.append(missed_cams_list)
            print('\n')
            outobj.write('\n')
        outobj.close()
        pass

    def classify_via_bench_camera(self, bench_type):
        if bench_type == 0:
            result_file = self.workdir + '_classified_result_e.txt'
            cmd_file = self.workdir + '_classified_cmd_e.txt'
            self.get_earliest_camera()
        else:
            result_file = self.workdir + '_classified_result_m.txt'
            cmd_file = self.workdir + '_classified_cmd_m.txt'
            self.get_most_and_earliest_camera()

        self.frames_times_vec = traverse_datetime_infos(self.frames_times_dict)
        # self.classify_via_intervals_between_cameras(result_file)
        self.classify_via_intervals_within_cameras(result_file)

        # return

        self.result_dir = self.workdir + '_frame'
        self.result_cr2_dir = self.result_dir + '_cr2'
        qing_mkdir(self.result_dir)
        qing_mkdir(self.result_cr2_dir)
        # self.classified_dir = self.workdir + '_classified'
        # qing_mkdir(self.classified_dir)
        self.get_classified_commands(cmd_file)
        pass

    def get_classified_commands(self, cmd_file):
        cmdobj = open(cmd_file, 'w')

        # for cam_idx, cam_name in enumerate(self.cam_names):
        #     cam_dir = self.classified_dir + '/' + cam_name
        #     qing_mkdir(cam_dir)
        #     pass

        for idx, frm_names in enumerate(self.classified_results):
            frm_idx = 'FRM_%04d' % (idx)
            frm_dir = self.result_dir + '/' + frm_idx
            qing_mkdir(frm_dir)
            print('frm_dir = ', frm_dir)

            if ImageClassifier.CR2:
                frm_cr2_dir = self.result_cr2_dir + '/' + frm_idx
                qing_mkdir(frm_cr2_dir)
                print('frm_cr2_dir = ', frm_cr2_dir)

            for f in frm_names:
                dir_name = os.path.dirname(f)
                jpg_name = os.path.basename(f)
                cam_name = os.path.basename(dir_name)

                jpg_prefix = jpg_name[:-4]
                jpg_suffix = jpg_name[-4:]

                # classified_f = self.classified_dir + '/' + cam_name + \
                #     '/' + jpg_prefix + '_' + frm_idx + jpg_suffix
                # print('cp ', f, classified_f)
                # shutil.copy(f, classified_f)

                result_f = frm_dir + '/' + cam_name + '_' + \
                    jpg_prefix + '_' + frm_idx + jpg_suffix
                print('cp ', f, result_f)
                shutil.copy(f, result_f)
               
                if ImageClassifier.CR2:
                    cr2_name = jpg_prefix + '.CR2'
                    cr2_f = dir_name + '/' + cr2_name
                    result_cr2_f = frm_cr2_dir + '/' + cam_name + \
                        '_' + jpg_prefix + '_' + frm_idx + '.CR2'
                    print('cp ', cr2_f, result_cr2_f)
                    cmdstr = 'cp ' + f + '\t' + result_cr2_f + '\n'
                    cmdobj.write(cmdstr)
                    # shutil.copy(cr2_f, result_cr2_f)
            cmdobj.write('\n')
        cmdobj.close()
        print('saving ' + cmd_file)
        pass

    # this function is for testing classification correctness with several
    # frames
    # def calc_classified_result_gt(self):
    #     tempfile = '../classified_results_ground_truth.txt'
    #     tempobj = open(tempfile, 'w')
    #     frames_times_dict = self.frames_times_dict.copy()
    #     frm_num = len(frames_times_dict[0])
    #     self.gt_classified_results_dict = [[] for k in range(frm_num)]
    #     # print(len(classified_results_dict))

    #     for frm_idx in range(0, frm_num):
    #         for cam_idx, frame_dict in enumerate(frames_times_dict):
    #             cam_name = self.cam_names[cam_idx]
    #             if frm_idx == 3 and cam_name == 'C06':
    #                 continue
    #             if frm_idx == 4 and cam_name == 'R05':
    #                 continue
    #             if frm_idx == 5 and (cam_name == 'R06' or cam_name == 'C05'):
    #                 continue
    #             print('frm_idx = ', frm_idx, 'cam_idx = ', cam_idx, 'cam_name = ', cam_name,
    #                   '%d files remain.' % (len(frame_dict)))
    #             self.gt_classified_results_dict[frm_idx].append(frame_dict[0])
    #             frame_dict.remove(frame_dict[0])

    #     for frm_idx in range(0, frm_num):
    #         same_frame_dict = self.gt_classified_results_dict[frm_idx]
    #         out_str = 'FRM_%04d' % (frm_idx) + \
    #             '\t%d files' % (len(same_frame_dict))
    #         print(out_str)
    #         tempobj.write(out_str + '\n')
    #         for cam_idx, frm_pair in enumerate(same_frame_dict):
    #             frm_name = frm_pair[0]
    #             frm_time = frm_pair[1]
    #             frm_interval = qing_datetime_diff_seconds(frm_time)
    #             out_str = frm_name + '\t' + \
    #                 str(frm_time) + '\t' + str(frm_interval)
    #             print(out_str)
    #             tempobj.write(out_str + '\n')
    #         tempobj.write('\n')
    #     print('saving ', tempfile)

    # def diff_classified_results(self):
    #     # difference between classified result and groundtruth of classified
    #     # result
    #     c_len = len(self.classified_results)
    #     g_len = len(self.classified_results_ground_truth)
    #     diff_file = '../difference.txt'
    #     diff_obj = open(diff_file, 'w')
    #     diff_obj.write('calc: %d files.' % (c_len) +
    #                    '\tground_truth: %d files.\n' % (g_len))

    #     for frm_idx in range(self.bench_frm_num):
    #         frm_idx_str = 'FRM_%04d' % (frm_idx)
    #         c_frame_dict = self.classified_results[frm_idx]
    #         g_frame_dict = self.classified_results_ground_truth[frm_idx]
    #         diff_obj.write(frm_idx_str + '\n')


def main(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "hd:", ["dir="])
    except getopt.GetoptError:
        print('1-classify-frame.py -d <workdir> ')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('1-classify-frame.py -d <workdir>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            workdir = arg
        # print('workdir =  ', workdir)
    # classify_frame_via_earliest_cam(workdir)

    qing_classifier = ImageClassifier(workdir)
    cam_names = qing_classifier.get_cameras()
    qing_classifier.display()
    qing_classifier.get_frames_names_and_datetimes()
    qing_classifier.classify_via_bench_camera(1)

    # qing_classifier.diff_classified_results()

    pass

if __name__ == '__main__':
    main(sys.argv[1:])
