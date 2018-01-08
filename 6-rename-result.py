from qing_operation import *
from collections import defaultdict
from datetime import datetime, timedelta
import getopt
import copy


def rename_initial_rigid_extrinsics_once(tf_folder):
    files = sorted(glob.glob(tf_folder + '/*.tf'))
    for f in files[1:]:
        fn = os.path.basename(f)
        new_f = tf_folder + '/' + fn[0:3] + fn[8:]
        print(f, new_f)
        os.rename(f, new_f)
    # sys.exit()


def copy_ply_files(src_dir, dst_dir):
    folders = sorted(os.listdir(src_dir))
    src_ply_files = []
    dst_ply_files = []
    for f in folders:
        if f.startswith('.'):
            continue
        f_dir = src_dir + '/' + f
        ply_fn = glob.glob(f_dir + '/*.ply')
        for ply in ply_fn:
            src_ply_files.append(ply)
    for ply in src_ply_files:
        ply_fn = os.path.basename(ply)
        new_ply = dst_dir + '/' + ply_fn
        dst_ply_files.append(new_ply)
        print(ply, new_ply)
        shutil.copy(ply, new_ply)

    return dst_ply_files


def rename_ply_files(ply_files):
    for idx, ply in enumerate(ply_files):
        ply_fn = os.path.basename(ply)
        ply_dir = os.path.dirname(ply)
        new_ply_fn = '%02d_' % (idx) + ply_fn
        new_ply = ply_dir + '/' + new_ply_fn
        print(ply, new_ply)
        os.rename(ply, new_ply)


def copy_and_rename_ply(re_folder, re_frm_folder, re_ply_folder):
    qing_mkdir(re_ply_folder)
    ply_files = sorted(glob.glob(re_ply_folder + '/*.ply'))
    if 0 == len(ply_files):
        ply_files = copy_ply_files(re_frm_folder, re_ply_folder)
    else:
        print('HAHAHA')
        # print(ply_files)
    rename_ply_files(ply_files)


def copy_tf_files(src_dir, dst_dir):
    src_tf_files = sorted(glob.glob(src_dir + '/*.tf'))
    dst_tf_files = []
    for tf in src_tf_files:
        tf_fn = os.path.basename(tf)
        new_tf = dst_dir + '/' + tf_fn
        dst_tf_files.append(new_tf)
        print(tf, new_tf)
        shutil.copy(tf, new_tf)
    return dst_tf_files


def rename_tf_files(tf_files, frameid):
    for idx, tf in enumerate(tf_files):
        tf_fn = os.path.basename(tf)
        tf_dir = os.path.dirname(tf)
        new_tf_fn = tf_fn[0:3] + frameid + tf_fn[7:]
        new_tf = tf_dir + '/' + new_tf_fn
        print(tf, new_tf)
        os.rename(tf, new_tf)


def copy_and_rename_tf(tf_folder, out_folder, frameid):
    print('tf_folder: ', tf_folder)
    print('out_folder: ', out_folder)
    qing_mkdir(out_folder)
    tf_files = sorted(glob.glob(out_folder + '/*.tf'))
    if 0 == len(tf_files):
        tf_files = copy_tf_files(tf_folder, out_folder)
    else:
        print('HAHAHA')
    rename_tf_files(tf_files, frameid)

#"cmd": ["python", "$file", "-d", "..", "-f", "0248"]


def main(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "hd:f:t:", ["help", "dir=", "frm=","time="])
    except getopt.GetoptError:
        print('6-rename-result.py -d <workdir> -f <frameid> -t <timestr>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('6-rename-result.py -d <workdir> -f <frameid> -t <timestr>' )
            sys.exit()
        elif opt in ("-d", "--dir"):
            workdir = arg
        elif opt in ("-f", "--frm"):
            frmid = arg
        elif opt in ("-t", "--time"):
        	timestr = arg

    print('workdir = ', workdir)
    print('frameid = ', frmid)
    print('timestr = ', timestr)
   
    # tf_folder = workdir + '/Initial_Rigid_Extrinsics'
    # rename_initial_rigid_extrinsics_once(tf_folder)

    # workdir = workdir + '/' + timestr
    # re_folder = workdir + '/Result_scanner'
    # re_frm_folder = re_folder + '/FRM_' + frmid
    # re_ply_folder = re_frm_folder + '_PLY'
    # copy_and_rename_ply(re_folder, re_frm_folder, re_ply_folder)
    
    tf_folder = workdir + 'Human_Extrinsic_Rigid/' + timestr
    frm_folder = timestr + '_FRM_' + frmid + '_PLY'
    out_folder = workdir + 'Human_Pointcloud_Registration/' + frm_folder
    # re_ply_folder = workdir + '/' + frm_folder
    copy_and_rename_tf(tf_folder, out_folder, frmid)


if __name__ == '__main__':
    main(sys.argv[1:])
