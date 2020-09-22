import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from scipy import interpolate

def load_isochrone(age=1, feh=0., alpha=0.):
    iso_dir = '/Users/mbedell/python/gr8stars/annelies/'

    if feh==0. and alpha==0.:
        isofile = 'fehp00afep0.Gaia'
    elif feh==0.5 and alpha==0.:
        isofile = 'fehp05afep0.Gaia'
    elif feh==0.5 and alpha==0.2:
        isofile = 'fehp05afep2.Gaia'
    else:
        print('isochrone not found for configuration')
        return

    f = open(iso_dir+isofile,'r')
    lines = f.readlines()
    f.close()
    lines = np.array(lines)

    # Select all lines that start with #AGE
    ages = []
    start = []
    nr = []
    for n,line in enumerate(lines):
        if line[:4] == '#AGE':
            ages.append(float(line[5:10]))
            nr.append(int(line[17:]))
            start.append(n+2)

    for ind,age in enumerate(ages):
        if age == int(age):
            iso = lines[start[ind]:start[ind]+nr[ind]]

            Gmag = [float(i[39:47]) for i in iso]
            BPmag = np.array([float(i[47:55]) for i in iso])
            RPmag = np.array([float(i[55:63]) for i in iso])

            bp_rps = np.array(BPmag-RPmag)
            gmags = np.array(Gmag)

    return bp_rps,gmags

if __name__ == "__main__":
    # Read in from query (with cuts on periods used, G mag uncertainty):
    data = Table.read('/Users/mbedell/python/gr8stars/gaiadr2/g_lt_8.5-result.fits')
    print('sources with G < 8.5: {0}'.format(len(data)))

    # Unit error cut following Lindegren+2018 appendix C:
    uniterror = np.sqrt(data['astrometric_chi2_al']/(data['astrometric_n_good_obs_al']-5))

    plt.scatter(data['phot_g_mean_mag'], uniterror, marker='.', s=4, alpha=0.5, 
             c=data['visibility_periods_used'])
    gg = np.linspace(2, 8.5, 100)
    #uu = 1.2 * np.max(np.vstack([np.exp(-0.2 * (gg - 19.5)), 
    #                             np.ones_like(gg)]), axis=0)
    uu = 1.2 * np.exp(-0.2 * (gg - 19.5))
    plt.plot(gg, uu, c='red', alpha=0.8)
    plt.xlabel('G mag')
    plt.ylabel('Unit error')
    plt.yscale('log')
    plt.colorbar(label='# periods used')
    plt.savefig('gaia_cuts_uniterror.pdf')
    plt.clf()

    uniterror_cut = uniterror <= 1.2 * np.exp(-0.2 * (data['phot_g_mean_mag'] - 19.5))
    data = data[uniterror_cut]
    print('sources after unit error cut: {0}'.format(len(data)))

    # Parallax uncertainty <= 2.5%:
    plx_cut = data['parallax_over_error'] > 40
    data = data[plx_cut]
    print('sources after parallax error cut: {0}'.format(len(data)))


    # Isochrone cut:
    iso_colors, iso_mags = load_isochrone(age=1, feh=0., alpha=0.)

    abs_gs = data['phot_g_mean_mag'] - 5.*np.log10(1000.0/data['parallax']) + 5.
    plt.scatter(data['bp_rp'], abs_gs, marker='.', s=4, alpha=0.5)
    plt.plot(iso_colors, iso_mags, color='k')
    plt.xlim([0,4])
    plt.ylim([14,-2])
    plt.xlabel('Bp - Rp')
    plt.ylabel('abs G')
    plt.show()

    breakpoint()




