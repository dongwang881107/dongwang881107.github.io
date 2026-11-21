"""Describe current-pattern ranks and a voltage-only baseline on KIT4 v1.

Run with NumPy and SciPy:
  python kit4-voltage-audit.py data_mat_files.zip kit4-voltage-errors.csv

Input archive: https://zenodo.org/records/1203914
"""
import argparse
import csv
from hashlib import md5
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from scipy.io import loadmat


KIT4_MD5 = "ad9f03325cafc9aae8c0149927de8e06"
ADJACENT = slice(0, 16)
SKIP_ONE = slice(16, 32)
SKIP_TWO = slice(32, 48)
SKIP_THREE = slice(48, 64)
FIELDS = ("case", "skip_one_relative_error", "skip_two_relative_error")


def ranks(currents, fit):
    scores = (fit, SKIP_ONE, SKIP_TWO)
    return tuple(
        int(np.linalg.matrix_rank(np.hstack([currents[:, part] for part in scores[:i]])))
        for i in range(1, len(scores) + 1)
    )


def prediction_error(currents, voltages, test):
    fit_currents = currents[:, ADJACENT]
    test_currents = currents[:, test]
    weights = np.linalg.lstsq(fit_currents, test_currents, rcond=None)[0]
    if not np.allclose(fit_currents @ weights, test_currents, atol=1e-12, rtol=1e-12):
        raise ValueError("Test drives fall outside the fitted current span")
    observed = voltages[:, test]
    predicted = voltages[:, ADJACENT] @ weights
    scale = np.linalg.norm(observed)
    if scale == 0:
        raise ValueError("All observed voltages in the test block are zero")
    return np.linalg.norm(predicted - observed) / scale


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    data = args.archive.read_bytes()
    if md5(data).hexdigest() != KIT4_MD5:
        raise ValueError("Expected the data_mat_files.zip from KIT4 v1 on Zenodo")

    rank_sets = set()
    rank_measurements = set()
    rows = []
    with ZipFile(BytesIO(data)) as archive:
        cases = sorted(name for name in archive.namelist() if Path(name).name.startswith("datamat_") and name.endswith(".mat"))
        if len(cases) != 38:
            raise ValueError("Expected 38 MAT cases")
        for name in cases:
            arrays = loadmat(BytesIO(archive.read(name)))
            currents = arrays["CurrentPattern"]
            voltages = arrays["Uel"]
            measurements = arrays["MeasPattern"]
            if currents.shape != (16, 79) or voltages.shape != currents.shape or measurements.shape != (16, 16):
                raise ValueError(f"Unexpected array dimensions in {name}")
            if not all(np.isfinite(a).all() for a in (currents, voltages, measurements)):
                raise ValueError(f"Non-finite value in {name}")
            rank_sets.add((ranks(currents, ADJACENT), ranks(currents, SKIP_THREE)))
            rank_measurements.add(int(np.linalg.matrix_rank(measurements)))
            rows.append((
                Path(name).stem.removeprefix("datamat_"),
                prediction_error(currents, voltages, SKIP_ONE),
                prediction_error(currents, voltages, SKIP_TWO),
            ))

    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(FIELDS)
        writer.writerows(rows)

    print("Cumulative current ranks (adjacent start, skip-three start):", sorted(rank_sets))
    print("Readout ranks:", sorted(rank_measurements))
    for column, name in enumerate(FIELDS[1:], start=1):
        print(name, "min, Q1, median, Q3, max, percent:", np.quantile(
            [row[column] * 100 for row in rows], [0, 0.25, 0.5, 0.75, 1]
        ))


if __name__ == "__main__":
    main()
