#!/bin/bash
# Processing many subjects written in the command: bash topup_bet.sh Cont_## Cont_## etc... (or Sourd_##)
#
# subjects take the value of $1, then $2 and so on: the sequences of words after topup_bet.sh
for subject in $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} ${21} ${22} ${23} ${24} ${25} ${26} ${27} ${28} ${29} ${30} ${31} ${32} ${33} ${34}	# in this example, the value of the variable subject is Cont_## then shifts to another Cont_## and so on (or Sourd_##)
do

# $subject inserts the value of the variable subject
# the '...' indicates to take literally what is between the two

# Adding a path to be able to use the bash program from any directory and shorterning commands through the use of variables
path='/home/fsluser/Documents/Connectivity_2018/Sourds/'$subject'/'
DWI64=$path$subject'_DWI_b0_64dirs_AP.nii.gz'
b0AP=$path$subject'_b0_AP.nii.gz'
b0PA=$path$subject'_DWI_b0_PA.nii.gz'
b0APPA=$path$subject'_b0_AP_PA.nii.gz'
b0APPAextra=$path$subject'_b0_AP_PA_extra.nii.gz'
b0APextra=$path$subject'_DWI_b0_64dirs_AP_extra.nii.gz'
outtopup=$path$subject'_topup'
iouttopup=$path$subject'_topup_b0.nii.gz'
brain=$path$subject'_topup_b0_brain'
#
# Extract b0 from main dw file with all the directions
fslroi $DWI64 $b0AP 0 1
#
# Combine b0 Anterior-Posterior with b0 Posterior-Anterior
fslmerge -t $b0APPA $b0AP $b0PA
#
# Add an extra layer to combined b0's to have an even number
fslroi $b0APPA $b0APPAextra 0 -1 0 -1 0 66
#
# Add an extra layer to main dw file to have an even number
fslroi $DWI64 $b0APextra 0 -1 0 -1 0 66
#
# Signal the start time
BEGIN=$(date +%s)
echo
echo Topup correction started "for" $subject at
date
#
# Running topup
topup --imain=$b0APPAextra --datain=acq_param_Sourds.txt --config=b02b0.cnf --out=$outtopup --iout=$iouttopup
#
# Apply Brain Extraction Tool
bet $iouttopup $brain -m -f 0.3
#
# Results on time interval
NOW=$(date +%s)
let DIFF=$(($NOW - $BEGIN))
let MINS=$(($DIFF / 60))
let SECS=$(($DIFF % 60))
let HOURS=$(($DIFF / 3600))
let DAYS=$(($DIFF / 86400))

if [ $MINS -ge 60 ]; then # Correct the amount of minutes
let MINS=$(($MINS - $HOURS * 60))
fi

if [ $HOURS -ge 24 ]; then # Correct the amount of hours
let HOURS=$(($HOURS - $DAYS * 24))
fi

echo Total run time "for" $subject is #/Display total time
printf "\n\r%3d Days, %02d:%02d:%02d\n" $DAYS $HOURS $MINS $SECS
echo
#
done
