from qing_operation import *

def rename_cam_names(workdir):
	cam_names = os.listdir(workdir)
	for cam in cam_names:
		cam_dir = workdir + '/' + cam
		if not os.path.isdir(cam_dir):
			continue
		new_cam_dir = workdir + '/' + cam[:1] + cam[2:]
		print(cam_dir, ' -> ', new_cam_dir)
		os.rename(cam_dir, new_cam_dir)

def main():
	workdir = '../Calib_bu_bu'
	rename_cam_names(workdir)

if __name__ == '__main__':
	main()