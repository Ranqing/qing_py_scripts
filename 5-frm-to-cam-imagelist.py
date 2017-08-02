from qing_operation import *

camera_names = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16',
                'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16',
                'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
                'L01', 'L02', 'L03', 'L04', 'L05', 'L06', 'R01', 'R02', 'R03', 'R04', 'R05', 'R06', 'N03', 'N04', 'N05', 'N06']


def imagelist_generator(dir_path, out_path):
    frm_names = os.listdir(dir_path)
    for idx, camname in enumerate(camera_names):
        name = out_path + '/imagelist_' + camname + '.txt'
        obj = open(name, 'w')
        obj.close()

    for frm in frm_names:
        frm_path = dir_path + '/' + frm
        if not os.path.isdir(frm_path):
            continue
        files = sorted(glob.glob(frm_path + '/*.JPG'))
        for f in files:
            fname = os.path.basename(f)
            camname = fname[0:3]
            filename = out_path + '/imagelist_' + camname + '.txt'
            fileobj = open(filename,'a')
            fileobj.write(f + '\n')
            fileobj.close()

def main():
    dir_path = '../Humans_frame'
    out_path = '../Humans_frame_imagelists'
    qing_mkdir(out_path)
    imagelist_generator(dir_path, out_path)


if __name__ == '__main__':
    main()
