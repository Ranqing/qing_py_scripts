python 1-classify-frame.py
echo 'end of classification, interval = 5'
python 6-rotate-shell.py
echo 'end of rotate shell generation'
python 7-run-rotate-shell.py
cd ../shells
sh run_rotate.sh
echo 'end of rotation'
python 5-imagelist.py
echo 'end of generation of imagelist for rectification '
mkdir ../Humans_rectified
cd /media/ranqing/Work/RQProjects/ZJU/3-Rectification/build
cur_Dir=$(pwd)
echo $cur_Dir
sh run_rectification_a.sh
echo 'end of rectification and move of cam-A and cam-B'
sh run_rectification_c.sh
echo 'end of recitfication and move of cam-C and cam-L and cam-R'
cd /media/ranqing/Qing-WD-New/20170618/py_scripts
cur_Dir=$(pwd)
echo $cur_Dir
python 8-move-frame.py
mv ../Humans_rectified ../../MyTrash  