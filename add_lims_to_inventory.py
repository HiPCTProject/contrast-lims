"""
Using pre-calculated histograms, add constrast limits to inventory.
"""
from pathlib import Path
from typing import Tuple

import numpy as np

from hipct_data_tools import load_datasets
from hipct_data_tools.inventory.esrf_report import save_datasets

from calc_distributions import HIST_PATH


PERCENTILES = [1, 99]

def limits_from_counts(hist_path: Path) -> Tuple[int, int]:
    counts = np.load(hist_path)["counts"]
    counts_sum = np.cumsum(counts)
    counts_sum = counts_sum.astype(float) / counts_sum[-1]

    lower_lim = np.argmax(counts_sum > PERCENTILES[0] / 100)
    upper_lim = np.argmax(counts_sum > PERCENTILES[1] / 100)
    return int(lower_lim), int(upper_lim)


if __name__ == "__main__":
    datasets = load_datasets()

    for dataset in datasets:
        hist_path = HIST_PATH / f"counts_{dataset.name}.npz"
        if hist_path.exists():
            lims = limits_from_counts(hist_path=hist_path)

            print(dataset.name, lims)
            dataset.contrast_low = lims[0]
            dataset.contrast_high = lims[1]

    save_datasets(datasets=datasets)
