"""Generate performance graphs from Quicksort benchmark results.

The program reads the aggregated benchmark results and creates one graph
for each input distribution, comparing deterministic and randomized
Quicksort across increasing input sizes.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


RESULTS_DIR = Path("results")
SUMMARY_FILE = RESULTS_DIR / "quicksort_summary.csv"


def slugify(name: str) -> str:
    """Convert a distribution name into a filename-friendly form."""
    return name.lower().replace(" ", "_")


def main() -> None:
    """Generate one comparison graph for each input distribution."""
    grouped: dict[
        str,
        dict[
            str,
            list[tuple[int, float, float]],
        ],
    ] = defaultdict(
        lambda: defaultdict(list)
    )

    with SUMMARY_FILE.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            grouped[
                row["distribution"]
            ][
                row["algorithm"]
            ].append(
                (
                    int(row["size"]),
                    float(row["mean_ms"]),
                    float(row["stdev_ms"]),
                )
            )

    for distribution, algorithm_data in grouped.items():
        plt.figure(figsize=(8, 5))

        for algorithm, points in algorithm_data.items():
            points.sort(
                key=lambda point: point[0]
            )

            sizes = [
                point[0]
                for point in points
            ]

            means = [
                point[1]
                for point in points
            ]

            errors = [
                point[2]
                for point in points
            ]

            plt.errorbar(
                sizes,
                means,
                yerr=errors,
                marker="o",
                capsize=3,
                label=algorithm,
            )

        plt.title(
            f"Quicksort Performance - {distribution} Input"
        )

        plt.xlabel(
            "Input Size (n)"
        )

        plt.ylabel(
            "Mean Running Time (ms)"
        )

        plt.grid(
            True,
            alpha=0.25,
        )

        plt.legend()

        plt.tight_layout()

        output_file = (
            RESULTS_DIR
            / f"{slugify(distribution)}_comparison.png"
        )

        plt.savefig(
            output_file,
            dpi=200,
        )

        plt.close()

        print(
            f"Saved {output_file}"
        )


if __name__ == "__main__":
    main()