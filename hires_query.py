import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack
from astropy import units as u
from astropy.coordinates import SkyCoord
from pykoa.koa import Koa
from tqdm.auto import tqdm

sample_infile = 'Gr8stars_GaiaeDR3_TIC.tsv'
sample_outfile = 'Gr8stars_GaiaeDR3_TIC_hires.csv'
hires_obs_outfile = 'koa_out/all.csv'
resume = 0 # index of sample to start querying -- 0 by default

def filter(rec):
    return rec[(rec['iodout']=='T') & (rec['specres'] >= 60000) & (rec['imagetyp'] == 'object')]

def coadd_snr(rec):
    snrs = rec['sig2nois']
    return np.sqrt(np.sum(snrs**2))
    

if __name__ == "__main__":
    if resume > 0:
        # load up in-progress sample:
        sample = Table.read(sample_outfile)
        hires_obs = Table.read(hires_obs_outfile)
    else:
        # read input sample:  
        sample = Table(np.genfromtxt(sample_infile, 
                                     delimiter='\t', names=True, 
                                     dtype=None, encoding=None))

        sample['n_hires_obs_all'] = 0
        sample['n_hires_obs_iodout'] = 0
        sample['hires_snr'] = 0

        # set up table from query on first target:
        Koa.query_position('HIRES', 'circle {0} {1} 0.5'.format(sample[0]['_RAJ2000'], sample[0]['_DEJ2000']),
                        outpath='koa_out/{0}.tbl'.format(sample[0]['EDR3Name'].replace(" ", "_")),
                        overwrite=True)
        rec = Table.read('koa_out/{0}.tbl'.format(sample[0]['EDR3Name'].replace(" ", "_")), format='ascii.ipac')
        rec['EDR3Name'] = sample[0]['EDR3Name']

        hires_obs = rec

    # populate table with others:
    for i,s in enumerate(sample):
        if i<resume:
            continue
        if i%10 == 0:
            print('TARGET {0}/{1}'.format(i+1, len(sample)))
        try: 
            rec = Table.read('koa_out/{0}.tbl'.format(s['EDR3Name'].replace(" ", "_")), format='ascii.ipac')
        except:
            Koa.query_position('HIRES', 'circle {0} {1} 0.5'.format(s['_RAJ2000'], s['_DEJ2000']),
                    outpath='koa_out/{0}.tbl'.format(s['EDR3Name'].replace(" ", "_")),
                    overwrite=True)
            rec = Table.read('koa_out/{0}.tbl'.format(s['EDR3Name'].replace(" ", "_")), format='ascii.ipac')
        sample[i]['n_hires_obs_all'] = len(rec)
        if len(rec['koaid']) >= 1:
            rec['EDR3Name'] = s['EDR3Name']
            good = filter(rec)
            if len(good) >= 1:
                sample[i]['n_hires_obs_iodout'] = len(good['koaid'])
                sample[i]['hires_snr'] = coadd_snr(good)
            hires_obs = vstack([hires_obs, rec])

    # save:
    sample.write(sample_outfile, overwrite=True) 
    hires_obs.write(hires_obs_outfile, overwrite=True)
