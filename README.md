# contrast-lims

Code for calculating contrast limits for HiP-CT datasets.
Designed to be run on the ESRF servers.

The code is split into two parts:

## Calculating histograms of data values
`calc_distributions.py` calculates distributions of all the pixels within a dataset.
This is parallelised across slices of images, so makes sense to run it on a cluster at ESRF.
The distributions are saved to files in `/data/projects/hop/data_repository/Various/data/histograms`.

## Calculating percentiles & adding to inventory
`add_lims_to_inventory.py` calculates percentiles from the pre-computed data distributions, and saves them to the HiP-CT inventory.
