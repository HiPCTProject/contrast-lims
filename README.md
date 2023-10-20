# contrast-lims

Code for calculating contrast limits for HiP-CT datasets.
The code is split into two parts:

## Calculating histograms of data values
`calc_distributions.py` calculates distributions of all the pixels within a dataset.

## Calculating percentiles & adding to inventory
`add_lims_to_inventory.py` calculates percentiles from the pre-computed data distributions, and saves them to the HiP-CT inventory.
