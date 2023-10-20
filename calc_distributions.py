from multiprocessing import Pool
from pathlib import Path
from typing import Any

import glymur
import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from hipct_data_tools import load_datasets

HIST_PATH = Path("/data/projects/hop/data_repository/Various/histograms")


def data_in_circle(arr: npt.NDArray[Any]) -> npt.NDArray[Any]:
    """
    Given a 2D array, return only an array inside a circle touching the edges.
    """
    nx, ny = arr.shape
    X, Y = np.meshgrid(
        np.linspace(-0.5, 0.5, nx), np.linspace(-0.5, 0.5, ny), indexing="ij"
    )
    mask = (X**2 + Y**2) < 0.25
    return arr[mask]


def value_count(jp2_path: Path) -> npt.NDArray[np.uint64]:
    jp2k = glymur.Jp2k(jp2_path)
    all_data = jp2k[:]
    data = data_in_circle(all_data)
    counts = np.bincount(data, minlength=2**16)
    return counts.astype(np.uint64)


if __name__ == "__main__":
    datasets = load_datasets()

    hist_data = np.zeros(2**16, dtype=np.uint64)

    for dataset in datasets:
        hist_path = HIST_PATH / f"counts_{dataset.name}.npz"
        if hist_path.exists():
            print(f"Already processed {dataset.name}")
            continue

        step = 10
        paths = sorted(dataset.esrf_jp2_path.glob("*.jp2"))[::step]
        print(f"Processing {dataset.name}...")

        with Pool() as p:
            result = list(tqdm(p.imap(value_count, paths), total=len(paths)))

        counts = np.sum(result, axis=0)
        np.savez_compressed(HIST_PATH / f"counts_{dataset.name}.npz", counts=counts)
