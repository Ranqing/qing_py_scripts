from qing_operation import *

# dirname = 'shells_bu'
# out_sh_filename = '../run_rotate_calib_bu.sh'
# sh_files = sorted(glob.glob('../' + dirname + '/*.sh'))
# out = open(out_sh_filename, 'w')
# for f in sh_files:
# 	filename = os.path.basename(f)
# 	comand = 'sh ' + filename + '\n'
# 	out.write(comand)
# out.close()

dirname = 'shells_new'
out_sh_filename = '../run_rotate_new.sh'
sh_files = sorted(glob.glob('../' + dirname + '/*.sh'))
out = open(out_sh_filename, 'w')
for f in sh_files:
	filename = os.path.basename(f)
	comand = 'sh ' + filename + '\n'
	out.write(comand)
out.close()


# mv run_rotate_calib.sh ./shells




