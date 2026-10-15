"""Deterministic Quicksort implementation for MSCS 532 Assignment 5.

This implementation uses Lomuto partitioning and selects the final element
of each active subarray as the pivot. The algorithm sorts the input list
in place.
"""

from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def lomuto_partition(values: MutableSequence[T], low: int, high: int) -> int:
    """Partition values[low:high + 1] using the final element as the pivot.

    Elements less than or equal to the pivot are moved to its left, while
    elements greater than the pivot are moved to its right.

    Args:
        values: Mutable sequence containing the values to partition.
        low: Starting index of the active subarray.
        high: Ending index of the active subarray.

    Returns:
        The final index of the pivot.
    """
    pivot = values[high]
    boundary = low - 1

    for index in range(low, high):
        if values[index] <= pivot:
            boundary += 1
            values[boundary], values[index] = values[index], values[boundary]

    pivot_index = boundary + 1
    values[pivot_index], values[high] = values[high], values[pivot_index]

    return pivot_index


def quicksort(values: MutableSequence[T]) -> MutableSequence[T]:
    """Sort values in ascending order using deterministic Quicksort.

    The final element of each active subarray is used as the pivot.
    The input sequence is modified in place and returned.

    Average-case time complexity: O(n log n)
    Worst-case time complexity: O(n^2)
    """
    if len(values) < 2:
        return values

    _quicksort_range(values, 0, len(values) - 1)

    return values


def _quicksort_range(
    values: MutableSequence[T],
    low: int,
    high: int,
) -> None:
    """Sort the specified range using smaller-partition recursion.

    Recursing on the smaller partition and processing the larger partition
    iteratively limits Python call-stack growth while preserving Quicksort's
    partitioning behavior.
    """
    while low < high:
        pivot_index = lomuto_partition(values, low, high)

        left_size = pivot_index - low
        right_size = high - pivot_index

        if left_size < right_size:
            _quicksort_range(values, low, pivot_index - 1)
            low = pivot_index + 1
        else:
            _quicksort_range(values, pivot_index + 1, high)
            high = pivot_index - 1


if __name__ == "__main__":
    sample = [19, 3, 15, 8, 12, 7]

    print("Original:", sample)

    quicksort(sample)

    print("Sorted:  ", sample)