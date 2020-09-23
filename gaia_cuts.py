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

    print("loading isochrone file {0}".format(isofile))
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
    
    for ind,a in enumerate(ages):
        if a == int(age):
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

    # Parallax uncertainty <= 2.5%:
    plx_cut = data['parallax_over_error'] >= 40
    data = data[plx_cut]
    print('sources after parallax error cut: {0}'.format(len(data)))

    '''
    # G < 8:
    mag_cut = data['phot_g_mean_mag'] <= 8.0
    data = data[mag_cut]
    print('sources with G < 8.0: {0}'.format(len(data)))
    '''

    # Color cut:
    color_cut = data['bp_rp'] >= 0.5
    data = data[color_cut]
    print('sources with Bp-Rp >= 0.5: {0}'.format(len(data)))

    color_cut2 = data['bp_rp'] <= 2.7
    data = data[color_cut2]
    print('sources with Bp-Rp <= 2.7: {0}'.format(len(data)))

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
    plt.savefig('gaia_cuts_uniterror.pdf', dpi=100)
    plt.clf()

    uniterror_cut = uniterror <= 1.2 * np.exp(-0.2 * (data['phot_g_mean_mag'] - 19.5))
    data = data[uniterror_cut]
    print('sources after unit error cut: {0}'.format(len(data)))



    # Isochrone cut:
    iso_colors, iso_mags = load_isochrone(age=1, feh=0., alpha=0.)
    iso_colors2, iso_mags2 = load_isochrone(age=1, feh=0.5, alpha=0.)
    iso_colors3, iso_mags3 = load_isochrone(age=1, feh=0.5, alpha=0.2)

    abs_gs = data['phot_g_mean_mag'] - 5.*np.log10(1000.0/data['parallax']) + 5.
    plt.scatter(data['bp_rp'], abs_gs, marker='.', s=4, alpha=0.5, c='k')
    plt.plot(iso_colors, iso_mags, label=r'1 Gyr, [Fe/H]=0.0, [$\alpha$/H]=0.0')
    plt.plot(iso_colors2, iso_mags2, label=r'1 Gyr, [Fe/H]=0.5, [$\alpha$/H]=0.0')
    plt.plot(iso_colors3, iso_mags3, label=r'1 Gyr, [Fe/H]=0.5, [$\alpha$/H]=0.2')
    plt.xlim([0,3])
    plt.ylim([12,-2])
    plt.xlabel('Bp - Rp', fontsize=14)
    plt.ylabel('abs G', fontsize=14)
    plt.legend(fontsize=10)
    plt.savefig('gaia_cuts_isochrone.pdf', dpi=100)
    plt.clf()

    mask_giants = iso_mags >= 2.
    iso_function = interpolate.interp1d(iso_colors[mask_giants], 
                                        iso_mags[mask_giants], kind='cubic')
    iso_cut = abs_gs >= iso_function(data['bp_rp'].data.compressed())
    data = data[iso_cut]
    print('sources after isochrone cut: {0}'.format(len(data)))


    abs_gs = data['phot_g_mean_mag'] - 5.*np.log10(1000.0/data['parallax']) + 5.
    plt.scatter(data['bp_rp'], abs_gs, marker='.', s=4, alpha=0.5, c=data['phot_g_mean_mag'])
    plt.xlim([0.3,2.7])
    plt.ylim([10,2.5])
    plt.xlabel('Bp - Rp', fontsize=14)
    plt.ylabel('abs G', fontsize=14)
    plt.colorbar(label='apparent G')
    plt.savefig('gaia_cuts_cmd.pdf', dpi=100)
    plt.clf()









