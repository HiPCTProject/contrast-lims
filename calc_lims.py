from hipct_data_tools import load_datasets
import numpy as np
import glymur
from pathlib import Path
from multiprocessing import Pool

from zarr.convenience import save_array

from tqdm import tqdm


def data_in_circle(arr):
    """
    Given a 2D array, return only an array inside a circle touching the edges.
    """
    nx, ny = arr.shape
    X, Y = np.meshgrid(np.linspace(-0.5, 0.5, nx), np.linspace(-0.5, 0.5, ny))
    mask = (X**2 + Y**2) < 0.25
    return arr[mask]

def value_count(jp2_path):
    jp2k = glymur.Jp2k(jp2_path)
    all_data = jp2k[:]
    data = data_in_circle(all_data)
    counts = np.bincount(data, minlength=2**16)
    return counts.astype(np.uint64)

if __name__ == "__main__":
    datasets = load_datasets()

    hist_data = np.zeros(2**16, dtype=np.uint64)

    for dataset in datasets:
        step = 10
        paths = sorted(dataset.esrf_jp2_path.glob("*.jp2"))[::step]
        print(f"Processing {dataset.name}...")

        with Pool() as p:
            result = list(tqdm(p.imap(value_count, paths), total=len(paths)))

        counts = np.sum(result, axis=0)
        save_array(dataset.esrf_jp2_path.parent / f"counts_{dataset.name}.zarr", counts)
