from qing_operation import *

dirname = 'shells'
out_sh_filename = '../run_rotate_calib.sh'
sh_files = sorted(glob.glob('../' + dirname + '/*.sh'))
out = open(out_sh_filename, 'w')
for f in sh_files:
	filename = os.path.basename(f)
	comand = 'sh ' + filename + '\n'
	out.write(comand)
out.close()

# mv run_rotate_calib.sh ./shells




