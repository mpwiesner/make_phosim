#!/usr/bin/python
import numpy as np
import sys
import csv
import math
import matplotlib.pyplot as plt
from numpy import zeros,abs,multiply,array,reshape
import os

file_image_list="list"
agn_list="sprinkled_agn_230.txt"
lens_list="sprinkled_lens_galaxies_230.txt"
the_directory="/Users/mwiesner/Documents/make_phosim/instance_files_r/"

#agn_id, agn_ra, agn_dec, agn_mag, agn_sed, agn_redshift, agn_twinkles_id, agn_img_num, agn_lens_galaxy_uID = np.loadtxt(
 #       file_lagn_cat, dtype="str", comments='#', delimiter=',',
 #       converters=None, skiprows=1, usecols=(1,2,3,4,5,6,17,18,19),
  #      unpack=True, ndmin=0)


#NOW READ IN THE LIST OF AGN
b=np.loadtxt(agn_list, dtype="str")

id_agn,ra_agn,dec_agn,mag_agn,sed_agn,z_agn,galacticAv_Agn,twinkles_system_agn,twinkles_img_num_agn,lens_galaxy_uID_agn = np.loadtxt(
        agn_list, dtype="str", comments='#', delimiter=',',
        converters=None, skiprows=1, usecols=(1,2,3,4,5,6,15,17,18,19),
        unpack=True, ndmin=0)

id_agn = id_agn.astype('int')
ra_agn = ra_agn.astype('double')
dec_agn = dec_agn.astype('double')
mag_agn = mag_agn.astype('double')
sed_agn = sed_agn.astype('str')
z_agn = z_agn.astype('double')
galacticAv_Agn = galacticAv_Agn.astype('double')
twinkles_system_agn = twinkles_system_agn.astype('double')
twinkles_img_num_agn = twinkles_img_num_agn.astype('double')
lens_galaxy_uID_agn = lens_galaxy_uID_agn.astype('double')


#NOW READ IN THE LIST OF LENSES
c=np.loadtxt(lens_list, dtype="str")

id_lens,ra_lens,dec_lens,mag_lens,sed_lens,z_lens,majoraxis_lens, minoraxis_lens, pa_lens, sindex_lens, internalAv_lens, internalRv_lens, galacticAv_lens = np.loadtxt(
        lens_list, dtype="str", comments='#', delimiter=',',
        converters=None, skiprows=1, usecols=(1,2,3,4,5,6,13,14,15,16,18,19,21),
        unpack=True, ndmin=0)

id_lens = id_lens.astype('int')
ra_lens = ra_lens.astype('double')
dec_lens = dec_lens.astype('double')
mag_lens = mag_lens.astype('double')
sed_lens = sed_lens.astype('str') 
z_lens = z_lens.astype('double')
majoraxis_lens = majoraxis_lens.astype('double')
minoraxis_lens = minoraxis_lens.astype('double')
pa_lens = pa_lens.astype('double')
sindex_lens = sindex_lens.astype('int')
internalAv_lens = internalAv_lens.astype('double')
internalRv_lens = internalRv_lens.astype('double')
galacticAv_lens = galacticAv_lens.astype('double')

#READ IN THE LIST OF FITS FILES OUTPUT BY THE LENSING PROGRAM

a=np.loadtxt(file_image_list, dtype="str")

#okk = len(id_lens)
#ok = range(okk)

for p in range (0, len(a)):
#for p in range (0, 3):

	text=a[p]
	id_host,num_host,ra_host,dec_host,mag_host,sed_host_name,sed_host,z_host,scale_host = text.split('_')

	id_host = int(id_host)
	num_host = int(num_host)
	ra_host = float(ra_host)
	dec_host = float(dec_host)
	mag_host = float(mag_host)
	z_host = float(z_host)

	tt = np.where(id_agn == id_host) 

	agn_lens_id = lens_galaxy_uID_agn[tt]

	fine = np.where(id_lens == agn_lens_id)

	phile = open(the_directory+"system"+str(p)+".instance_r","w")
	
	if num_host == 0:
		print >> phile, "Unrefracted_RA_deg", str(ra_lens[fine])[1:-1]
		print >> phile, "Unrefracted_Dec_deg", str(dec_lens[fine])[1:-1]
		print >> phile, "Opsim_filter 2"
		print >> phile, "SIM_NSNAP 1"
		print >> phile, "SIM_VISTIME 30.0"
	#print the parameters for the lensed host
		print >> phile, "object 1", ra_host, dec_host, mag_host, "galaxySED/"+sed_host, z_host, "0 0 0 0 0", a[p], "0.01 0"
	#print the parameters for the lens
		print >> phile, "object 2", str(ra_lens[fine])[1:-1], str(dec_lens[fine])[1:-1], str(mag_lens[fine])[1:-1], str(sed_lens[fine])[2:-2], str(z_lens[fine])[1:-1], "0 0 0 0 0 sersic2d", str(majoraxis_lens[fine])[1:-1],str(minoraxis_lens[fine])[1:-1],str(pa_lens[fine])[1:-1], str(sindex_lens[fine])[1:-1], "CCM",str(internalAv_lens[fine])[1:-1], str(internalRv_lens[fine])[1:-1],"CCM",str(galacticAv_lens[fine])[1:-1],"3.1"

	#print the parameters for the agn
	#	for ab in range (0, )
	#	for ab in range (0, len(dist)):
		dd =int(tt[0][0])
		if twinkles_img_num_agn[dd] == 0 and twinkles_img_num_agn[dd+1] == 1 and twinkles_img_num_agn[dd+2] == 2 and twinkles_img_num_agn[dd+3] == 3:
			print >> phile, "object 3", str(ra_agn[dd])[0:-1], str(dec_agn[dd])[0:-1], str(mag_agn[dd])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd])[0:-1], "3.1"   
			print >> phile, "object 4", str(ra_agn[dd+1])[0:-1], str(dec_agn[dd+1])[0:-1], str(mag_agn[dd+1])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd+1])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd+1])[0:-1], "3.1"   
			print >> phile, "object 5", str(ra_agn[dd+2])[0:-1], str(dec_agn[dd+2])[0:-1], str(mag_agn[dd+2])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd+2])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd+2])[0:-1], "3.1"   
			print >> phile, "object 6", str(ra_agn[dd+3])[0:-1], str(dec_agn[dd+3])[0:-1], str(mag_agn[dd+3])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd+3])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd+3])[0:-1], "3.1"   

		if twinkles_img_num_agn[dd] == 0 and twinkles_img_num_agn[dd+1] == 1 and twinkles_img_num_agn[dd+2] == 2 and twinkles_img_num_agn[dd+3] != 3:
			print >> phile, "object 3", str(ra_agn[dd])[0:-1], str(dec_agn[dd])[0:-1], str(mag_agn[dd])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd])[0:-1], "3.1"   
			print >> phile, "object 4", str(ra_agn[dd+1])[0:-1], str(dec_agn[dd+1])[0:-1], str(mag_agn[dd+1])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd+1])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd+1])[0:-1], "3.1"   
			print >> phile, "object 5", str(ra_agn[dd+2])[0:-1], str(dec_agn[dd+2])[0:-1], str(mag_agn[dd+2])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd+2])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd+2])[0:-1], "3.1"   
		
		if twinkles_img_num_agn[dd] == 0 and twinkles_img_num_agn[dd+1] == 1 and twinkles_img_num_agn[dd+2] != 2 and twinkles_img_num_agn[dd+3] != 3:
			print >> phile, "object 3", str(ra_agn[dd])[0:-1], str(dec_agn[dd])[0:-1], str(mag_agn[dd])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd])[0:-1], "3.1"   
			print >> phile, "object 4", str(ra_agn[dd+1])[0:-1], str(dec_agn[dd+1])[0:-1], str(mag_agn[dd+1])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd+1])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd+1])[0:-1], "3.1"   
		
		if twinkles_img_num_agn[dd] == 0 and twinkles_img_num_agn[dd+1] != 1 and twinkles_img_num_agn[dd+2] != 2 and twinkles_img_num_agn[dd+3] != 3:
			print >> phile, "object 3", str(ra_agn[dd])[0:-1], str(dec_agn[dd])[0:-1], str(mag_agn[dd])[0:-1], "agnSED/agn.spec.gz", str(z_agn[dd])[0:-1], "0 0 0 0 0 point none CCM", str(galacticAv_Agn[dd])[0:-1], "3.1"   
		
		phile.close()

	#if there is more than one image for the lensed host, print its parameters
	if num_host == 1:
		phile = open(the_directory+"system"+str(p-1)+".instance","a")
		print >> phile, "object 7", ra_host, dec_host, mag_host, "galaxySED/"+sed_host, z_host, "0 0 0 0 0", a[p], "0.01 0"
		phile.close()	
	#	os.remove(the_directory+"system"+str(p)+".instance_r")

