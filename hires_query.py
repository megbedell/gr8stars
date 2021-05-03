import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack
from astropy import units as u
from astropy.coordinates import SkyCoord
from pykoa.koa import Koa
from tqdm.auto import tqdm

def filter(rec):
    return rec[(rec['iodout']=='T') & (rec['specres'] >= 45000)]


if __name__ == "__main__": 
    # read in sample:  
    sample = Table.read('ollie_stars.tsv', format='ascii',  
            delimiter='\t', header_start=1, data_start=3)

    sample['n_hires_obs_all'] = 0
    sample['n_hires_obs_iodout'] = 0
    sample['hires_snr'] = 0

    # set up table from query on first target:
    Koa.query_position('HIRES', 'circle {0} {1} 0.5'.format(sample[0]['RA_ICRS'], sample[0]['DE_ICRS']),
                    outpath='koa_out/{0}.tbl'.format(sample[0]['Gaia Name'].replace(" ", "_")),
                    overwrite=True)
    rec = Table.read('koa_out/{0}.tbl'.format(sample[0]['Gaia Name'].replace(" ", "_")), format='ascii.ipac')
    rec['Gaia Name'] = sample[0]['Gaia Name']
    sample[0]['n_hires_obs_all'] = len(rec)
    good = filter(rec)
    if len(good) >= 1:
        sample[0]['n_hires_obs_iodout'] = len(good)
        sample[0]['hires_snr'] = np.max(good['sig2nois'])

    hires_obs = rec

    # populate table with others:
    for i,s in enumerate(sample):
        if i%10 == 0:
            print('TARGET {0}/{1}'.format(i+1, len(sample)))
        try: 
            rec = Table.read('koa_out/{0}.tbl'.format(s['Gaia Name'].replace(" ", "_")), format='ascii.ipac')
        except:
            Koa.query_position('HIRES', 'circle {0} {1} 0.5'.format(s['RA_ICRS'], s['DE_ICRS']),
                    outpath='koa_out/{0}.tbl'.format(s['Gaia Name'].replace(" ", "_")),
                    overwrite=True)
            rec = Table.read('koa_out/{0}.tbl'.format(s['Gaia Name'].replace(" ", "_")), format='ascii.ipac')
        sample[i+1]['n_hires_obs_all'] = len(rec)
        if len(rec['koaid']) >= 1:
            rec['Gaia Name'] = s['Gaia Name']
            good = filter(rec)
            if len(good) >= 1:
                sample[i+1]['n_hires_obs_iodout'] = len(good['koaid'])
                sample[i+1]['hires_snr'] = np.max(good['sig2nois']) # CO-ADD?
            hires_obs = vstack([hires_obs, rec])

    # save:
    hires_obs.write('koa_out/all.csv', overwrite=True)
    sample.write('ollie_stars_w_hires.csv', overwrite=True) 