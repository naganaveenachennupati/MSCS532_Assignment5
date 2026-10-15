"""Empirical comparison of deterministic and randomized Quicksort.

The experiment measures both implementations across several input sizes
and data distributions. Each configuration is executed for multiple
trials, and both the individual measurements and aggregated statistics
are saved as CSV files.
"""

from __future__ import annotations

import csv
import random
import statistics
import time
from pathlib import Path
from typing import Callable

from quicksort import quicksort
from randomized_quicksort import randomized_quicksort


RESULTS_DIR = Path("results")

TRIALS_FILE = RESULTS_DIR / "quicksort_trials.csv"
SUMMARY_FILE = RESULTS_DIR / "quicksort_summary.csv"

SIZES = [
    100,
    500,
    1_000,
    2_000,
    5_000,
]

TRIALS = 5

DATASET_SEED = 532
RANDOMIZED_SEED = 1532


SortFunction = Callable[[list[int], int], None]


def deterministic_runner(
    values: list[int],
    seed: int,
) -> None:
    """Run deterministic Quicksort.

    The seed parameter is accepted so both algorithm runners have the
    same interface. It is not needed by deterministic Quicksort.
    """
    del seed
    quicksort(values)


def randomized_runner(
    values: list[int],
    seed: int,
) -> None:
    """Run randomized Quicksort with a reproducible random seed."""
    randomized_quicksort(
        values,
        random.Random(seed),
    )


ALGORITHMS: dict[str, SortFunction] = {
    "Deterministic Quicksort": deterministic_runner,
    "Randomized Quicksort": randomized_runner,
}


def make_dataset(
    distribution: str,
    size: int,
    trial: int,
) -> list[int]:
    """Create a reproducible dataset for one experimental trial."""
    rng = random.Random(
        DATASET_SEED
        + size * 101
        + trial
    )

    if distribution == "Random":
        return [
            rng.randint(
                -10_000_000,
                10_000_000,
            )
            for _ in range(size)
        ]

    if distribution == "Repeated":
        return [
            rng.randint(-10, 10)
            for _ in range(size)
        ]

    base = rng.sample(
        range(
            -20_000_000,
            20_000_000,
        ),
        size,
    )

    base.sort()

    if distribution == "Sorted":
        return base

    if distribution == "Reverse Sorted":
        return list(reversed(base))

    raise ValueError(
        f"Unknown distribution: {distribution}"
    )


def time_one(
    algorithm: str,
    source: list[int],
    seed: int,
) -> float:
    """Time one sort and return elapsed milliseconds."""
    values = source.copy()
    expected = sorted(source)

    runner = ALGORITHMS[algorithm]

    start = time.perf_counter_ns()

    runner(
        values,
        seed,
    )

    elapsed_ns = (
        time.perf_counter_ns()
        - start
    )

    if values != expected:
        raise AssertionError(
            f"{algorithm} produced an incorrect result"
        )

    return elapsed_ns / 1_000_000


def main() -> None:
    """Run the complete empirical comparison."""
    RESULTS_DIR.mkdir(exist_ok=True)

    distributions = [
        "Random",
        "Sorted",
        "Reverse Sorted",
        "Repeated",
    ]

    trial_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for distribution in distributions:
        print(f"\n{distribution}")

        for size in SIZES:
            for algorithm in ALGORITHMS:
                timings: list[float] = []

                for trial in range(
                    1,
                    TRIALS + 1,
                ):
                    source = make_dataset(
                        distribution,
                        size,
                        trial,
                    )

                    seed = (
                        RANDOMIZED_SEED
                        + size * 1009
                        + trial * 37
                    )

                    elapsed_ms = time_one(
                        algorithm,
                        source,
                        seed,
                    )

                    timings.append(
                        elapsed_ms
                    )

                    trial_rows.append(
                        {
                            "distribution":
                                distribution,
                            "size":
                                size,
                            "algorithm":
                                algorithm,
                            "trial":
                                trial,
                            "elapsed_ms":
                                f"{elapsed_ms:.6f}",
                        }
                    )

                mean_ms = statistics.mean(
                    timings
                )

                stdev_ms = (
                    statistics.stdev(timings)
                    if len(timings) > 1
                    else 0.0
                )

                summary_rows.append(
                    {
                        "distribution":
                            distribution,
                        "size":
                            size,
                        "algorithm":
                            algorithm,
                        "trials":
                            TRIALS,
                        "mean_ms":
                            f"{mean_ms:.6f}",
                        "stdev_ms":
                            f"{stdev_ms:.6f}",
                    }
                )

                print(
                    f"  n={size:>5}  "
                    f"{algorithm:<24} "
                    f"mean={mean_ms:>10.4f} ms  "
                    f"sd={stdev_ms:.4f}"
                )

    with TRIALS_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "distribution",
                "size",
                "algorithm",
                "trial",
                "elapsed_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(trial_rows)

    with SUMMARY_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "distribution",
                "size",
                "algorithm",
                "trials",
                "mean_ms",
                "stdev_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(summary_rows)

    print(
        f"\nSaved {TRIALS_FILE}"
    )

    print(
        f"Saved {SUMMARY_FILE}"
    )


if __name__ == "__main__":
    main()