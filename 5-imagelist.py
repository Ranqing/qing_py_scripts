from qing_operation import *


def imagelist_generator(dir_path, out_path):
    cam_names = os.listdir(dir_path)
    for cam in cam_names:
    	cam_path = dir_path + '/' + cam
    	if not os.path.isdir(cam_path):
    		continue
    	list_name = out_path + '/imagelist_' + cam + '.txt'
    	print(list_name)
    	qing_imagelist_generator(list_name, cam_path, 'JPG')


def main():
    dir_path = '../Humans_rotated'
    #out_path = '../Humans_rotated_imagelists'
    out_path = '../Humans_rotated'
    qing_mkdir(out_path)
    imagelist_generator(dir_path, out_path)


if __name__ == '__main__':
    main()
