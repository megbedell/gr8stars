# gr8stars

The repository for the code to generate [the gr8stars database](https://flathub.flatironinstitute.org/gr8) may be found [on Github](https://github.com/megbedell/gr8stars).

### About the gr8stars project:

The gr8stars catalog is an assembly of stellar properties and downloadable high-resolution spectra of bright Sun-like stars in the Northern hemisphere.
gr8stars targets are uniformly selected from Gaia EDR3 to fulfill the following criteria:
- Bright: Gaia G magnitude <= 8
- Observable from northern hemisphere facilities: Declination >= -15 degrees
- Cool: Gaia B-R color >= 0.6
- Main-sequence: based on isochronal cuts in Gaia color-magnitude space

The resulting catalog of nearly 3,000 targets encompasses a prime sample for Northern-hemisphere radial velocity exoplanet surveys, precision stellar abundances, future direct imaging surveys, and more.

More information about the project and its sample selection can be found in the first gr8stars paper, [Freckelton et al (2024)](https://ui.adsabs.harvard.edu/abs/2025MNRAS.540.1786F/abstract). 

### gr8stars database contents:

Interactive access to the database is hosted on [FlatHUB](https://flathub.flatironinstitute.org/gr8).

For complete documentation of the Gaia parameters captured in the database, please see [the Gaia DR3 data model](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/). Please note that only a selection of Gaia parameters are included in the gr8stars database; if more are needed, they can be found by querying the Gaia archive using the DR3 (or DR2) IDs provided in the database. For information about the stellar parameters derived with PAWS and with SED fitting, see [Freckelton et al (2024)](https://ui.adsabs.harvard.edu/abs/2025MNRAS.540.1786F/abstract).

Further spectroscopic information will be added with the publication of future gr8stars papers.

### Citation info:

If you make use of the gr8stars database, please cite [Freckelton et al (2024)](https://ui.adsabs.harvard.edu/abs/2025MNRAS.540.1786F/abstract). This is also the citation for use of the PAWS and SED stellar parameters included in the database table.

Please additionally follow [the Gaia team's citation instructions](https://www.cosmos.esa.int/web/gaia-users/credits). The current version of gr8stars includes data from Gaia DR3 and includes information from both the `gaia_source` and `astrophysical_parameters` tables.

**IMPORTANT**: The spectra hosted in the gr8stars database are made available for convenience only and are not owned by the gr8stars team. If you make use of these spectra, please be sure to credit the instrument, observatory, and original PIs appropriately.

### Collaboration membership:

The gr8stars team is led by Annelies Mortier (University of Birmingham) and Megan Bedell (Flatiron Institute) and includes the following scientists from institutions worldwide: Vardan Adibekyan (Universidade do Porto), John Brewer (San Francisco State University), Lars Buchhave (DTU Space), Michael Cretignier (University of Oxford), Ernst De Mooij (Queen’s University Belfast), Elisa Delgado Mena (Universidade do Porto), Alix Freckelton (University of Birmingham), Jonay González Hernández (Instituto de Astrofísica de Canarias), Raphaelle Haywood (University of Exeter), David Jackson (Queen's University Belfast), Baptiste Klein (University of Oxford), Jared Kolecki (University of Notre Dame), Andreas Korn (Uppsala University), Suvrath Mahadevan (Penn State University), Sam Morrell (University of Exeter), Tim Naylor (University of Exeter), Belinda Nicholson (University of Oxford), Nikolai Piskunov (Uppsala University), Andreas Quirrenbach (University of Heidelberg), Ansgar Reiners (University of Göttingen), Arpita Roy (Space Telescope Science Institute), Nuno Santos (Universidade do Porto), Sérgio Sousa (Universidade do Porto), Alejandro Suárez Mascareño (Instituto de Astrofísica de Canarias), Sam Thompson (University of Cambridge), Maria Tsantaki (Arcetri Observatory), Chris Watson (Queen's University Belfast), Lily Zhao (University of Chicago). 

Please contact Annelies and Megan if you are interested in joining the team. We welcome new participants.