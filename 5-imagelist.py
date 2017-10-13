from qing_operation import *
import getopt


def imagelist_generator(dir_path, out_path):
    cam_names = os.listdir(dir_path)
    for cam in cam_names:
    	cam_path = dir_path + '/' + cam
    	if not os.path.isdir(cam_path):
    		continue
    	list_name = out_path + '/imagelist_' + cam + '.txt'
    	print(list_name)
    	qing_imagelist_generator(list_name, cam_path, 'JPG')


def main(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "hd:o:", ["dir=", "out="])
    except getopt.GetoptError as e:
        print('5-imagelist.py -d <workdir> -o <outdir>')
        sys.exit()        
    
    for opt, arg in opts:
        if opt == '-h':
            print('5-imagelist.py -d <workdir> -o <outdir>')
            sys.exit()
        elif opt in ('-d', '--dir'):
            workdir = arg
        elif opt in ('-o', '--out'):
            outdir = arg

    print('workdir = ', workdir)
    print('outdir = ', outdir)
    qing_mkdir(outdir)
    imagelist_generator(workdir, outdir)

# def main():
#     dir_path = '../Humans_rotated'
#     #out_path = '../Humans_rotated_imagelists'
#     out_path = '../Humans_rotated'
#     qing_mkdir(out_path)
#     imagelist_generator(dir_path, out_path)


if __name__ == '__main__':
    main(sys.argv[1:])
