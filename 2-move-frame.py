from qing_operation import *


def move_frame(workdir, outdir, framecnt):
    folders = sorted(os.listdir(workdir))

    for idx in range(0, framecnt):
        framestr = 'FRM_%04d' % idx
        out_framedir = outdir + '/' + framestr
        qing_mkdir(out_framedir)
        for f in folders:
            folderdir = workdir + '/' + f
            if not os.path.isdir(folderdir):
                continue
            files = sorted(glob.glob(folderdir + '/' + framestr + '*'))
            for file in files:
                filename = os.path.basename(file)
                new_filename = f + '_' + filename
                new_file = out_framedir + '/' + new_filename
                print('move\t' + file + '\t' + new_file)
               # shutil.move(file, new_file)
                shutil.copy(file, new_file)


def main():
    workdir = '../Humans_classified'
    outdir = '../Humans_frame'
    qing_mkdir(outdir)
    framecnt = 159
    move_frame(workdir, outdir, framecnt)

if __name__ == '__main__':
    main()
