"""Randomized Quicksort implementation for MSCS 532 Assignment 5.

This implementation randomly selects a pivot from the active subarray
before applying the same Lomuto partitioning strategy used by the
deterministic Quicksort implementation.
"""

from __future__ import annotations

import random
from typing import MutableSequence, TypeVar

from quicksort import lomuto_partition

T = TypeVar("T")


def randomized_quicksort(
    values: MutableSequence[T],
    rng: random.Random | None = None,
) -> MutableSequence[T]:
    """Sort values in ascending order using randomized Quicksort.

    A pivot is selected uniformly at random from the active subarray.
    The selected pivot is moved to the final position before applying
    Lomuto partitioning.

    Args:
        values: Mutable sequence to sort.
        rng: Optional random-number generator for reproducible experiments.

    Returns:
        The same sequence after sorting it in place.

    Expected time complexity: O(n log n)
    Worst-case time complexity: O(n^2)
    """
    if len(values) < 2:
        return values

    generator = rng if rng is not None else random.Random()

    _randomized_quicksort_range(
        values,
        0,
        len(values) - 1,
        generator,
    )

    return values


def _randomized_quicksort_range(
    values: MutableSequence[T],
    low: int,
    high: int,
    rng: random.Random,
) -> None:
    """Sort the specified range using randomly selected pivots."""
    while low < high:
        random_index = rng.randint(low, high)

        values[random_index], values[high] = (
            values[high],
            values[random_index],
        )

        pivot_index = lomuto_partition(values, low, high)

        left_size = pivot_index - low
        right_size = high - pivot_index

        if left_size < right_size:
            _randomized_quicksort_range(
                values,
                low,
                pivot_index - 1,
                rng,
            )
            low = pivot_index + 1
        else:
            _randomized_quicksort_range(
                values,
                pivot_index + 1,
                high,
                rng,
            )
            high = pivot_index - 1


if __name__ == "__main__":
    sample = [19, 3, 15, 8, 12, 7]

    print("Original:", sample)

    randomized_quicksort(sample, random.Random(532))

    print("Sorted:  ", sample)