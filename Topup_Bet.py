###########################################################################################################
######## IMPORTANT - Make sure to have moved your subjects into your ".dipy" directory - IMPORTANT ########
###########################################################################################################
import nibabel as nib # Enables us to read and write neuroimaging-specific file formats
import numpy as np # The fundamental package for scientific computing with Python
import matplotlib.pyplot as plt # For visualizing results
import shutil # Moving files in the right directory
import dcmstack.dcmstack # Allows the conversion of DICOM to nii
import dcmstack, dicom #
from os.path import expanduser, join # Allows for path manipulation
from dipy.io.gradients import read_bvals_bvecs # Enables us to load the bvals and bvecs
from dipy.core.gradients import gradient_table # Enables use of GradientTable
from dipy.segment.mask import median_otsu # To create brain masks
from dipy.core.histeq import histeq # Look at a slice
from dcmstack.dcmmeta import NiftiWrapper # Enables us to use Dicom and Nifti files and modify them

counter = 0 # Variable counting the number of subjects
totalsub = 1 # Change this value according to the amount of subjects being tested + 1
home = expanduser('~') # The home variable contains the path in which the .dipy folder is located

while counter < totalsub: # The loop keeps repeating itself until all subjects have been processed
	print ("Please enter the subject for which you would like to have the procedure affect: ")
    subject = raw_input() # Enter your subject here through the terminal (Only input() for python 3.6 or higher)
    dname = join(home, '.dipy', subject) # The directory name is saved under this variable
    #############################################################
    #			  Converting DICOM images to nii.gz				#
    #############################################################
    src_dcms = join(dname, subject + '_dcm', '*.dcm')
    stack = dcmstack.DicomStack()
    for src_path in src_dcms:
      src_dcm = dicom.read_file(src_path)
      stack.add_dcm(src_dcm)

    stack_data = stack.get_data() # Get the array of voxel data
    stack_affine = stack.get_affine() # Get the affine transform
    nii = stack.to_nifti(stack, 'LAS', True) # Create a NIFTI image, function to_nifti syntax -> to_nifti(self, voxel_order, embed_meta)

    ############################ Li check this out ################################# Li check this out ########################################################
     					# I've imported a new method from one of the scripts in dcmstack #
     						# The missing parameter is known as 'voxel_order' #
        varAP = DicomStack.to_nifti( , LAS, True) # voxel_order -> (l)eft, (r)ight, (a)nterior, (p)osterior, (s)uperior, and (i)nferior
     		# I've listed the different letters that can put for that parameter, three letters can be placed (in uppercase) #
     				# It is found in this directory -> .../site-packages/dcmstack/dcmstack.py #
    ############################ Li check this out ################################# Li check this out ########################################################

    #############################################################
	#  Identifying starting files and extracting the b0 volume  #
	#############################################################
	fdwi = join(dname, subject+'_DWI_b0_64dirs_AP.nii.gz') # The Nifti image is saved in this variable
	print(fdwi) # Printing on console
	fbval = join(dname, subject+'_DWI_b0_64dirs_AP.bval') # The bval file is saved in this variable
	print(fbval) # Printing on console
	fbvec = join(dname, subject+'_DWI_b0_64dirs_AP.bvec') # The bvec file is saved in this variable
	print(fbvec) # Printing on console


	img = nib.load(fdwi) # Saving the Nifti image in this variable
	data = img.get_data() # Saving the information of the Nifti image in this variable

	print(data.shape) # Size of data
	print(img.header.get_zooms()[:3]) # Checking dimensions of each voxel

	#############################################################
	#						  Plotting						    #
	#############################################################
	axial_middle = data.shape[2]//2
	plt.figure('Showing the datasets')
	plt.subplot(1, 2, 1).set_axis_off()
	plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
	plt.subplot(1, 2, 2).set_axis_off()
	plt.imshow(data[:, :, axial_middle, 10].T, cmap='gray', origin='lower')
	plt.show()

	bvals, bvecs = read_bvals_bvecs(fbval, fbvec) # Reading bvals and bvecs
	gtab = gradient_table(bvals, bvecs) # Table which will hold all acquisition specific parameters
	print(gtab.info) # Show information about table
	print(gtab.bvals) # Printing bvals on console
	print(gtab.bvecs) # Printing bvecs on console

	S0s = data[:, :, :, gtab.b0s_mask] # Used to tell which part of the data contains b0s
	print(S0s.shape) # Verifying the dimensions of S0s to determine the number of b0s
	nib.save(nib.Nifti1Image(S0s, img.affine), subject+'_b0_AP.nii.gz') # Just for necessary
	src = join(home, '.dipy', subject + '_b0_AP.nii.gz') # Where the source file is
	dst = join(dname, subject + "_b0_AP.nii.gz") # The new destination for the file
	shutil.move(src, dst) # Moving the file to the right directory

	#############################################################
	#                        Merging                            #
	#############################################################
	fb0AP = join(dname, subject + '_b0_AP.nii.gz') # The b0AP image is saved in this variable
	fb0PA = join(dname, subject + '_DWI_b0_PA.nii.gz') # The b0PA image is saved in this variable
	b0AP = NiftiWrapper.from_filename(fb0AP) # Loading the image in this variable
	b0PA = NiftiWrapper.from_filename(fb0PA) # Loading the image in this variable
	print(b0AP.nii_img.get_shape()) # Size of data
	print(b0PA.nii_img.get_shape()) # Size of data
	print(b0AP.get_meta('EchoTime')) # Echo time
	print(b0PA.get_meta('EchoTime')) # Echo time
	b0APPA = NiftiWrapper.from_sequence([b0AP, b0PA]) # Merging of the two b0 files
	print(b0APPA.nii_img.get_shape()) # Size of data
	print(b0APPA.get_meta('EchoTime', index = (0, 0, 0, 0))) # Echo time
	print(b0APPA.get_meta('EchoTime', index = (0, 0, 0, 1))) # Echo time

	#############################################################
	# 						Topup								#
	#############################################################


	#############################################################
	#	 		 	  Brain Extraction Tool (BET)				#
	#############################################################
	topb0 = join(dname, subject + '_topup_b0.nii.gz') # The topup_b0 file is saved in this variable
	img = nib.load (topb0) # Saving the nifti image in this variable

	#############################################################
	data = img.get_data() # **squeeze or no squeeze**
	#############################################################

	b0_mask, mask = median_otsu(data, , , , , ) # Creating the binary mask and the mask
	mask_img = nib.Nifti1Image(mask.astype(np.float32), img.affine) # Number of bits used, in this case 32, it is saved as float32
	b0_img = nib.Nifti1Image(b0_mask.astype(np.float32), img.affine) # Number of bits used, in this case 32, it is saved as float32
	nib.save(mask_img, subject + '_binary_mask.nii.gz') # Just for necessary
	nib.save(b0_img, subject + '_mask.nii.gz') # Just for necessary
	src = join(home, '.dipy', subject + '_binary_mask.nii.gz') # Where the source file is
	dst = join(dname, subject + "_binary_mask.nii.gz") # The new destination for the file
	shutil.move(src, dst) # Moving the file to the right directory
	src = join(home, '.dipy', subject + '_mask.nii.gz') # Where the source file is
	dst = join(dname, subject + "_mask.nii.gz") # The new destination for the file
	shutil.move(src, dst) # Moving the file to the right directory

	#############################################################
	# 				Plotting					#
	#############################################################
	sli = data.shape[2] // 2
	plt.figure('Brain segmentation')
	plt.subplot(1, 2, 1).set_axis_off()
	plt.imshow(histeq(data[:, :, sli].astype('float')).T,
    cmap='gray', origin='lower')

	plt.subplot(1, 2, 2).set_axis_off()
	plt.imshow(histeq(b0_mask[:, :, sli].astype('float')).T,
    cmap='gray', origin='lower')

  b0_mask_crop, mask_crop = median_otsu(data, 4, 4, autocrop=True) # Crop the outputs to remove the largest possible number of background voxels
  # May save files once decided

  counter+=1 # An additional subject is completed