from qing_operation import *
from collections import defaultdict

CR2 = False
CMD = True

# raw_human -> Human_frames
# value of interval is calculated according the datetime of the first frame in each camera

def get_files_datetime(folder_path):
    files = sorted(glob.glob(folder_path + '/*.JPG'))
    # fdict = {}
    fdict = defaultdict(lambda: None)
    for f in files:
        ftime = qing_read_exif(f, QING_EXIF_DATETIME)
        fdatetime = qing_str_to_datetime(str(ftime))
        fdict[f] = fdatetime
    return fdict


# def get_same_time_frame(file_times_vec, interval):
#     same_time_frame = []
#     for idx, file_times in enumerate(file_times_vec):
#         file_times = file_times_vec[idx]
#         cur_interval = qing_datetime_diff_seconds(file_times[0][1])
#         if abs(cur_interval - interval) < QING_CLASSIFIED_INTERVAL:
#             same_time_frame.append(file_times[0][0])
#             file_times.remove(file_times[0])
#         elif cur_interval - interval < -QING_CLASSIFIED_INTERVAL:
#             temp = file_times[0]
#             file_times.append(temp)
#     return same_time_frame
#     pass

def get_same_time_frame(file_times_vec, interval):
    same_time_frame = []
    for idx, file_times in enumerate(file_times_vec):
        file_times = file_times_vec[idx]
        cur_interval = qing_datetime_diff_seconds(file_times[0][1])
        # picture shooten at the same time
        if abs(cur_interval - interval) <= QING_CLASSIFIED_INTERVAL:
            same_time_frame.append(file_times[0])
            file_times.remove(file_times[0])
        # picture shooten before the same time, find the neareast
        elif cur_interval - interval < -QING_CLASSIFIED_INTERVAL:
            while len(file_times):
                tem_interval = qing_datetime_diff_seconds(file_times[0][1])
                if abs(tem_interval - interval) <= QING_CLASSIFIED_INTERVAL:
                    same_time_frame.append(file_times[0])
                    file_times.remove(file_times[0])
                    break
                elif tem_interval - interval > QING_CLASSIFIED_INTERVAL:
                    break
                elif tem_interval - interval < -QING_CLASSIFIED_INTERVAL:
                    file_times.remove(file_times[0])
            pass
    return same_time_frame
    pass


def classify_frame(workdir):
    folders = sorted(os.listdir(workdir))
    outdir = './raw_human_datetime'
    qing_mkdir(outdir)
    file_names_vec = []                 # filename vector
    file_times_vec = []                 # filename-datetime dictionary
    # classified result directory
    classified_dir = '../Humans_classified'
    qing_mkdir(classified_dir)
    # classified result
    classified_results = []

    benchidx = 0
    minsec = 100000
    for idx, f in enumerate(folders):
        folder_path = workdir + f
        if not os.path.isdir(folder_path):
            continue

        # new directory to store classified frame
        classified_path = classified_dir + '/' + f
        qing_mkdir(classified_path)

        # read datetime of all files
        files = sorted(glob.glob(folder_path + '/*.JPG'))
        # sorted by key then return a tuple
        file_times = qing_sort_dict(get_files_datetime(folder_path), 0)

        file_times_vec.append(file_times)
        file_names_vec.append(files)

        firstsec = qing_datetime_diff_seconds(file_times_vec[idx][0][1])
        benchidx = idx if firstsec < minsec else benchidx
        minsec = firstsec if firstsec < minsec else minsec

        print(folder_path, '%d' %
              (len(file_times)) + ' files', files[0], firstsec)

    # set the earliest camera as the anchor-point
    print('bench_idx = %d' % benchidx, 'camera_name = %s' %
          folders[benchidx], 'start_sec = %d' % minsec)

    # get all interval
    # for idx, key in enumerate(file_names_vec[benchidx]):
    #     interval = qing_datetime_diff_seconds(file_times_vec[benchidx][idx][1])
    #     print('FRM_%04d' % idx, 'interval = %d' % interval)
    # sys.exit()

    # traverse files in the bench camera
    # for each file find the similar time files in other cameras
    # if similar time file exists then delete that file
    # else delete that file then re-join the files in the end of the files vec
    # file_times_vec:
    outfile = workdir + 'classfied_result.txt'
    outobj = open(outfile, 'w')
    # interval = qing_datetime_diff_seconds(file_times_vec[benchidx][0][1])
    # idx: frm idx
    # key: frm name
    for idx, key in enumerate(file_names_vec[benchidx]):
        # pre_interval = interval
        interval = qing_datetime_diff_seconds(file_times_vec[benchidx][0][1])
        print('FRM_%04d' % idx, 'interval = %d' % interval)

        # if interval - pre_interval <= 3:
        #     file_times_vec[benchidx].remove(file_times_vec[benchidx][0])
        #     continue

        outobj.write('FRM_%04d' % idx + '\tinterval = %d' % interval)
        traverse_frm = get_same_time_frame(file_times_vec, interval)  # dict
        outobj.write('\t%d files\n' % len(traverse_frm))
       
        traverse_frm_names = []
        for f in traverse_frm:
            fname = f[0]
            finterval = qing_datetime_diff_seconds(f[1])
            traverse_frm_names.append(f[0])
            outobj.write(f[0] + '\t' + str(f[1]) + '\t%d' %
                         (finterval) + '\t%d\n' % (finterval - interval))
            print(f[0])
        classified_results.append(traverse_frm_names)
        outobj.write('\n')
        print()
    outobj.close()

    print('\nafter classification: %d files in ' %
          len(file_times_vec[benchidx]), '%s' % folders[benchidx])
    print('\n')
    # sys.exit()

    # classified

    cmdfile = workdir + 'classified_cmd.txt'
    cmdobj = open(cmdfile, 'w')
    cmdoutdir = '../Humans_frame'
    qing_mkdir(cmdoutdir)

    for idx, frms in enumerate(classified_results):
        print('FRM_%04d' % idx, len(frms))
        cmdobj.write('FRM_%04d' % idx + '\t%d files\n' % len(frms))

        frm_str = 'FRM_%04d' % idx
        cmdfrmdir = cmdoutdir + '/' + frm_str
        qing_mkdir(cmdfrmdir)

        for f in frms:
            dirname = os.path.dirname(f)
            jpgname = os.path.basename(f)
            cam_nam = os.path.basename(dirname)

            jpgprefix = jpgname[:-4]
            jpgsuffix = jpgname[-4:]
            new_f = classified_dir + '/' + cam_nam + \
                '/' + jpgprefix + '_' + frm_str + jpgsuffix
            print(f, new_f)
            # os.rename(f, new_f)
            shutil.copy(f, new_f)

            new_cmd_f = cmdfrmdir + '/' + cam_nam + '_' + jpgprefix + '_' + frm_str + jpgsuffix
            cmd = 'cp ' + f + '\t' + new_cmd_f + '\n'
            cmdobj.write(cmd)
            #shutil.copy(f, new_cmd_f)
            
            if CR2:
                cr2name = jpgprefix + '.CR2'
                cr2_f = dirname + '/' + cr2name
                new_cr2_f = classified_dir + '/' + cam_nam + \
                    '/' + jpgprefix + '_' + frm_str + '.CR2'
                print(cr2_f, new_cr2_f)
                # os.rename(cr2_f, new_cr2_f)
                # shutil.copy(cr2_f, new_cr2_f)
        cmdobj.write('\n')
    cmdobj.close()
    pass


def main():
    workdir = '../raw_human_jpg/'
    classify_frame(workdir)
    pass

if __name__ == '__main__':
    main()
