.. FILE AUTO GENERATED !! 

Spyctral: Astronomical spectral data analyser
=============================================


.. image:: https://github.com/candelac/Spyctral/actions/workflows/Testing.yml/badge.svg
   :target: https://github.com/candelac/Spyctral/actions/workflows/Testing.yml/badge.svg
   :alt: Tests


.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT


.. image:: https://img.shields.io/badge/python-3.9+-blue.svg
   :target: https://img.shields.io/badge/python-3.9+-blue.svg
   :alt: Python 3.9+


Spyctral is a python package that allows to determine fundamental parameters of compact stellar systems from the analysis of their spectral synthesis and/or templates fitting. 

Description
-----------

Spyctral is a set of tools to represent, load, manipulate and analyze astronomical spectroscopic data from spectral synthesis code results and templates fitting ones. The package provides a python toolbox to organize the outputs files and calculate astronomical parameters in a fast and accurate way giving to the astronomical community the spectra analysis more user-friendly.

Motivation
----------

Star clusters stand as a pivotal yardstick in modern astrophysics. They are excellent targets to determine stellar ages and metallicities providing rich information on the star formation and chemical histories of their host galaxies (e.g., Greggio & Renzini 2011; Adamo et al. 2020; Berek et al. 2023). Ages, metallicities, radial velocities and reddening of star clusters can be obtained using the integrated spectrum fitting technique both in the Local Group and in more distant galaxies (e.g., Asa’d et al. 2013; Ahumada et al. 2016; Clariá et al. 2017; Colucci et al. 2017; Chilingarian & Asa’d 2018; Ahumada et al. 2019; Bastian et al. 2019; Moura et al. 2019; Sakari et al. 2021; Simondi-Romero et al. 2022). Several automated tools have been developed to apply this powerful technique and they are widely used in the literature. STARLIGHT (Cid Fernandes et al. 2005), NBursts (Chilingarian et al. 2007), EZ_age (Graves & Schiavon 2008), FISA (Benítez-Llambay et al. 2012), and Analyzer of Spectra for Age Determination (A.S.A.D) (Asa’d 2014) are some examples.

STARLIGHT apply the integrated spectrum of the star clusters to estimate the age, reddening and radial velocity, however the two tools use different approaches. STARLIGHT provides the results of the best simple stellar populations (SSP) mixture that match the observed integrated spectrum along with the final synthetic spectrum which represents the combined contributions of the different SSP population mixtures. However, the outputfile does not give the final object parameters so Spyctral was developed to could explore the results and finally 
obtain ages, reddenings, radial velocities and abundances. 

FISA: “Fast Integrated Spectra Analyzer” permits fast and reasonably accurate age and reddening determinations for star clusters by using their integrated spectra and currently available template spectrum libraries. This algorithm and its implementation gives a results file with the astrophysical information in differents blocks. To look at the parameters in shorter times rather than looking case by case or file by file, Spyctral take the FISA outfile and give you the object parameters in a easy way. 

The Spyctral code receives files (text files with all the spectroscopic info) related to the observed object, extracts the necessary information and offers the necessary methods to determine the astrophysical parameters of the object. This approach will save processing time and help to achieve astrophysical results in shorter times than from other methods. In this way the focus of analysis can be quickly redirected to the astrophysical results in a timely manner. 

Features
--------

Spyctral needs a minimum of one text file and you need to know the source code of the file to be analysed to use the library correctly. 

Requeriments
------------

You will need Python 3.8 or higher to run Sypctral.

Basic install
-------------

You could find Spyctral at PyPI. The standar instalation via pip:

.. code-block:: bash

   $ pip install spyctral

Development install
-------------------

Clone this repo and then inside the local directory execute

.. code-block:: bash

   $ git clone https://github.com/candelac/Spyctral.git
   $ cd Spyctral
   $ pip install -e .

Tutorial
--------

Future upgrades
---------------

This is the first version of Spyctral code and we hope to add functionality so that the package will support output files from other synthesis codes, the next one to be included is A.S.A.D. 

Authors
-------


* Tapia-Reina Martina (martina.tapia@mi.unc.edu.ar)
* Cerdosino Candela (candelacerdosino@mi.unc.edu.ar)
* Fiore J.Manuel (juanmfiore@mi.unc.edu.ar)
* Martinez J.Luis (martinez.joseco@gmail.com)
* Cabral Juan (jbcabral@unc.edu.ar)
