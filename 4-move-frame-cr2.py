from qing_operation import *


def copy_frame(workdir, outdir):
    framenames = os.listdir(workdir)

    for frame in framenames:
        frame_dir = workdir + '/' + frame
        out_framedir = outdir + '/' + frame
        qing_mkdir(out_framedir)
        cr2_files = sorted( glob.glob(frame_dir + '/*.CR2'))
        for cr2 in cr2_files:
            cr2name = os.path.basename(cr2)
            new_cr2 = out_framedir + '/' + cr2name
            print(cr2, new_cr2)
            shutil.move(cr2, new_cr2)

def main():
    workdir = '../Humans_frame'
    outdir = '../Humans_frame_cr2'
    qing_mkdir(outdir)
    copy_frame(workdir, outdir)

if __name__ == '__main__':
    main()
