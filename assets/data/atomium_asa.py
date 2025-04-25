"""
RETRIEVAL OF ATOMIUM IMAGE AND RELATED DATA PRODUCTS

1) Fill in details below ######### Variables ##########
Compact, mid, extended, combined configurations are ~1", 0".3, 0".03, 0".05 resolution

Types of image: 
cont   line-free continuum
cubeXX where XX is any number from 00 to 15, 

see the ALMA landing page  http://almascience.org/alma-data/lp/ATOMIUM/ for spectral coverage and links to READMEs (can also be downloaded below).
and a link to a list of file sizes (some are tens GB, or hundreds GB for visibility data).

2) Run 
to run script:
in CASA <=5 or python 2
execfile('atomium_asa.py')      

In CASA 6 or python 3
exec(open('atomium_asa.py').read())

(replace atomium_asa.py if you have renamed this file).
NB If a data file of the same name already exists it will not be downloaded again, to avoid multiple downloads.
Partial downloads should be overwritten but if in doubt delete the problem file and re-download.

3) Practicality
The script will allow multiple stars and/or image products to be downloaded but please do not attempt to download all the image cubes for all the stars at once! Only one configuration data can be requested at one time. The script will not allow more than 34 image products to be downloaded at once.

4) Other files
This script does not cover downloading visibility data but this can be achieved by identifying the desired product for the star (from the README or description) and (on the command line, or in python as below) typing
 wget  https://almascience.eso.org/dataPortal/ + visibility product, e.g. 
 wget  https://almascience.eso.org/dataPortal/group.uid___A001_X133d_X131f.lp_ldecin.AH_Sco_mid_cont.ms.tgz

Primary beam corrected cubes are provided here; for naming of uncorrected cubes and masks to use in wget see the documentation.

"""
############### Variables ##################
# Enter one or more ALMA star names from
# AH_Sco GY_Aql IRC+10011 IRC-10529 KW_Sgr pi1_Gru RW_Sco R_Aql
# R_Hya SV_Aqr S_Pav T_Mic U_Del U_Her VX_Sgr V_PsA W_Aql

instar=['VX_Sgr']        # example ['AH_Sco','KW_Sgr']  

# Enter True or False (no '')
getdocs=True             # get README and more detailed description of data processing and products
getspec=True             # get spectra extracted as outlined in the description.pdf
getscript=True           # get scripts as described in the description.pdf

# ** Select desired data products or leave blank for documentation/spectra/scripts only **

# Enter configuration 
# compact mid extended combined 
cfg='compact'            # example 'mid' (just one per run of the script)

# enter type of image
# cont (=continuum); cube00 ... cube15
ims=['cont']             # examples ['cont'] or ['cube00','cube01']

# Now run the script

#################################
import os as os

if (len(instar))*(len(ims)) > 34:
    print('*** You have requested more than 34 image products, which is likely to place a high burden on the archive. ***\n*** Please reduce the number of stars or image products ***\n')
    raise SystemExit(0)
    
stars={'AH_Sco':'group.uid___A001_X133d_X131f',
       'GY_Aql':'group.uid___A001_X133d_X1237',
       'IRCp10011':'group.uid___A001_X133d_X1293',
       'IRC-10529':'group.uid___A001_X133d_X1298',
       'KW_Sgr':'group.uid___A001_X133d_X1307',
       'pi1_Gru':'group.uid___A001_X133d_X1254',
       'RW_Sco':'group.uid___A001_X133d_X12bf',
       'R_Aql':'group.uid___A001_X133d_X1210',
       'R_Hya':'group.uid___A001_X133d_X127b',
       'SV_Aqr':'group.uid___A001_X133d_X11c6',
       'S_Pav':'group.uid___A001_X133d_X12ef',
       'T_Mic':'group.uid___A001_X133d_X120b',
       'U_Del':'group.uid___A001_X133d_X11b7',
       'U_Her':'group.uid___A001_X133d_X124f',
       'VX_Sgr':'group.uid___A001_X133d_X12e9',
       'V_PsA':'group.uid___A001_X133d_X11c1',
       'W_Aql':'group.uid___A001_X133d_X11bc'}
        
gd='';gs='';gc='';products='';st='';prods=''
for s in instar: st=st+ s +', '
for p in ims:
    if p == 'cont' : p='continuum'
    prods=prods+p+', '
prods=prods[:-2]
if getdocs: gd= 'Documentation '
if getspec: gs= 'Spectra '
if getscript: gc= 'Scripts'
if len(cfg)>0 and len(ims)>0:
    products=prods+' images in configuration '+cfg+' for stars '+st
    products=products[:-2]

print('*** You have requested: '+gd+gs+gc+' *** \n*** ' +products+' ***\n')

ncom=['cube02','cube03' or'cube06','cube07' or'cube10','cube11' or'cube14','cube15']

for star in instar:
    if star =='IRC+10011':
        star='IRCp10011'
        print('*** Some products for IRC+10011 have name replaced as IRCp10011 ***')
    if star not in stars.keys():
        print('*** '+star+' not found. Check star name is exactly as in list under ### Variables ### ***\n')
        raise SystemExit(0)

    gid=stars[star]
    print('*** Files for '+star+' will be prefixed '+gid +' *** \n')

    
    if getdocs:
        os.system('wget -c -q https://almascience.eso.org/dataPortal/'+gid+'.lp_ldecin.README.txt')
        os.system('wget -c -q https://almascience.eso.org/dataPortal/'+gid+'.lp_ldecin.description.pdf')

    if getspec:
        os.system('wget -c -q https://almascience.eso.org/dataPortal/'+gid+'.lp_ldecin.'+star+'_spec.tgz')
    if getscript:
        os.system('wget -c -q https://almascience.eso.org/dataPortal/'+gid+'.lp_ldecin.'+star+'_scripts.tgz')

    if cfg=='compact':
        if star in ['AH_Sco','KW_Sgr']:
            print('Compact configuration data not observed for AH_Sco and KW_Sgr, please change selection.\n')
            raise SystemExit(0)
        for im in ims:
            for n in ncom:
                if n == im:
                    print('*** '+n+' not observed in compact configuration, please change selection. ***\n')
                    raise SystemExit(0)

    if len(cfg) > 0:
        if cfg not in ['cont', 'compact','mid','extended','combined']:
            print('*** No images downloaded. If you want images enter in script one value for cfg. ***\n')
            print('*** cont, compact, mid , extended or combined are allowed. ***\n')
            raise SystemExit(0)
        else:
            for im in ims:
                if im == 'cont':
                    os.system('wget -c https://almascience.eso.org/dataPortal/'+gid+'.lp_ldecin.'+star+'_'+cfg+'_'+im+'_mfs.fin.fits')
                else:
                    os.system('wget -c https://almascience.eso.org/dataPortal/'+gid+'.lp_ldecin.'+star+'_'+cfg+'_'+im+'.pbcor.fits') 




