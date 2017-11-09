from qing_operation import *

def run_rotate_shell(workdir):
	shellname = workdir + '/run_rotate.sh'
	if os.path.exists(shellname):
		os.remove(shellname)
	shellname = workdir + '/run_rotate'
	files = sorted(glob.glob(workdir + '/*.sh'))
	fileobj = open(shellname, 'w')
	for f in files:
		command = 'sh ' + f + '\n'
		fileobj.write(command)
	fileobj.close()
	new_shellname = shellname + '.sh'
	os.rename(shellname, new_shellname)


def main():
	workdir = '../shells'
	run_rotate_shell(workdir)

if __name__ == '__main__':
	main()