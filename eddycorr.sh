#!/bin/bash
# Processing many subjects written in the command: bash eddycorr.sh Cont_## Cont_## etc... (or Sourd_##)
# subjects take the value of $1, then $2 and so on: the sequences of words after eddycorr.sh
for subject in $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} ${21} ${22} ${23} ${24} ${25} ${26} ${27} ${28} ${29} ${30} ${31} ${32} ${33} ${34}	# in this example, the value of the variable subject is Cont_## then shifts to another Cont_## and so on (or Sourd_##)
do
# $subject inserts the value of the variable subject
#
# the '...' indicates to take literally what is between the two
# adding a path to be able to use the bash program from any directory and shortening commands through the use of variables
path='/home/fsluser/Documents/Connectivity_2018/Sourds/'$subject'/'
b0APextra=$path$subject'_DWI_b0_64dirs_AP_extra.nii.gz'
brainmask=$path$subject'_topup_b0_brain_mask.nii.gz'
vecs=$path$subject'_DWI_b0_64dirs_AP.bvec'
vals=$path$subject'_DWI_b0_64dirs_AP.bval'
outtopup=$path$subject'_topup'
outeddy=$path$subject'_eddy_corrected_data'
# Signal the start time
BEGIN=$(date +%s)
echo
echo Eddy Correction started "for" $subject at
date
# Undertake Eddy Correction procedure
eddy_openmp --imain=$b0APextra --mask=$brainmask --index=index_Sourds.txt --acqp=acq_param_Sourds.txt --bvecs=$vecs --bvals=$vals --topup=$outtopup --repol --out=$outeddy
#
# Total time of procedure
NOW=$(date +%s)
let DIFF=$(($NOW - $BEGIN))
let MINS=$(($DIFF / 60))
let SECS=$(($DIFF % 60))
let HOURS=$(($DIFF / 3600))
let DAYS=$(($DIFF / 86400))

if [ $MINS -ge 60 ]; then
let MINS=$(($MINS - $HOURS * 60))
fi

if [ $HOURS -ge 24 ]; then
let HOURS=$(($HOURS - $DAYS * 24))
fi

echo Total run time "for" $subject is
printf "\n\r%3d Days, %02d:%02d:%02d\n" $DAYS $HOURS $MINS $SECS
echo
#
done
