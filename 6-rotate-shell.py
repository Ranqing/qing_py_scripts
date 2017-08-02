from qing_operation import *

camera_names = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16',
                'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16',
                'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
                'L01', 'L02', 'L03', 'L04', 'L05', 'L06', 'N03', 'N04', 'N05', 'N06', 'R01', 'R02', 'R03', 'R04', 'R05', 'R06']

angles = [270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270,
          270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270,
          270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270,
          180, 180, 180, 180, 180, 180, 0,   0,   0,   0,   180, 180, 0,   0,   0,   0  ]


def write_file(filename, files, outdir, angle):
    fileobj = open(filename, 'w')
    for f in files:
        filename = os.path.basename(f)
        new_f = outdir + '/' + filename
        if angle:
            command = 'convert -rotate  %d' % angle + ' ' + f + ' ' + new_f
        else:
            command = 'cp ' + f + ' ' + new_f
        print command
        fileobj.write(command + '\n')
    pass


def rotate(workdir, outdir, shelldir):
    # cams = sorted(os.listdir(workdir))
    for idx, cam in enumerate(camera_names):
        cam_path = workdir + '/' + cam
        if not os.path.isdir(cam_path):
            continue
        out_path = outdir + '/' + cam
        qing_mkdir(out_path)
        print(cam_path, out_path)
        jpgfiles = sorted(glob.glob(cam_path + '/*.JPG'))
        cr2files = sorted(glob.glob(cam_path + '/*.CR2'))
        jpg_file_name = shelldir + '/rotate_jpg_' + cam + '.sh'
        cr2_file_name = shelldir + '/rotate_cr2_' + cam + '.sh'
        write_file(jpg_file_name, jpgfiles, out_path, angles[idx])
        # write_file(cr2_file_name, cr2files, out_path,  angles[idx])
        print(idx, cam, jpg_file_name, cr2_file_name, angles[idx])


def main():
    workdir = '../Humans_classified'
    outdir = '../Humans_rotated'
    shelldir = '../shells'
    qing_mkdir(outdir)
    qing_mkdir(shelldir)
    rotate(workdir, outdir, shelldir)
    pass


if __name__ == '__main__':
    main()


# if not os.path.exists(dst_folder):
#     os.makedirs(dst_folder)

# for i in range(0, len(camera_names)):
#     src_camera_dir = src_folder + '/' + camera_names[i]
#     new_camera_dir = dst_folder + '/' + camera_names[i]
#     if not os.path.exists(new_camera_dir):
#         os.makedirs(new_camera_dir)
#     print('%s' % (src_camera_dir + '/*.JPG ' + new_camera_dir))
#     files = glob.glob(src_camera_dir + '/*.JPG')
#     print len(files)
#     for f in files:
#         basename = os.path.basename(f)
#         jpgname = new_camera_dir + '/' + basename
#         command = 'convert -rotate ' + \
#             '%d' % angles[i] + ' ' + f + ' ' + jpgname
#         out_file_object.write(command + '\n')

# sys.exit()
