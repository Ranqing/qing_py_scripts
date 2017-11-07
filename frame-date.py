from qing_operation import *


def frame_dates(workdir, outdir):
    folders = sorted(os.listdir(workdir))
    for f in folders:
        fdir = workdir + f
        if not os.path.isdir(fdir):
            continue
        outfile = outdir + 'date_' + f + '.txt'
        outobj = open(outfile, 'w')
        jpgfiles = sorted(glob.glob(fdir + '/*.JPG'))
        for jpg in jpgfiles:
            date = qing_read_exif(jpg, QING_EXIF_DATETIME)
            print(jpg, date)
            outobj.write(jpg + ' ' + str(date) + '\n')
        outobj.close()


def main():
    workdir = '../raw_human_jpg/'
    outdir = '../raw_human_dates/'
    qing_mkdir(outdir)
    frame_dates(workdir, outdir)

if __name__ == '__main__':
    main()
