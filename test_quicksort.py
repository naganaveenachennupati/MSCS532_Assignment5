"""Automated tests for deterministic and randomized Quicksort."""

from __future__ import annotations

import random
import unittest

from quicksort import lomuto_partition, quicksort
from randomized_quicksort import randomized_quicksort


class DeterministicQuicksortTests(unittest.TestCase):
    """Tests for the deterministic Quicksort implementation."""

    def test_empty_list(self) -> None:
        values: list[int] = []

        result = quicksort(values)

        self.assertIs(result, values)
        self.assertEqual(values, [])

    def test_single_element(self) -> None:
        values = [7]

        quicksort(values)

        self.assertEqual(values, [7])

    def test_two_elements(self) -> None:
        values = [2, 1]

        quicksort(values)

        self.assertEqual(values, [1, 2])

    def test_already_sorted(self) -> None:
        values = list(range(100))

        quicksort(values)

        self.assertEqual(values, list(range(100)))

    def test_reverse_sorted(self) -> None:
        values = list(range(100, 0, -1))
        expected = sorted(values)

        quicksort(values)

        self.assertEqual(values, expected)

    def test_duplicate_values(self) -> None:
        values = [5, 1, 5, 3, 1, 5, 2, 2]
        expected = sorted(values)

        quicksort(values)

        self.assertEqual(values, expected)

    def test_all_equal_values(self) -> None:
        values = [4] * 200

        quicksort(values)

        self.assertEqual(values, [4] * 200)

    def test_negative_and_positive_values(self) -> None:
        values = [0, -10, 4, -3, 8, -1, 4]
        expected = sorted(values)

        quicksort(values)

        self.assertEqual(values, expected)

    def test_large_random_input(self) -> None:
        rng = random.Random(532)
        values = [
            rng.randint(-100_000, 100_000)
            for _ in range(2_000)
        ]
        expected = sorted(values)

        quicksort(values)

        self.assertEqual(values, expected)

    def test_large_sorted_input_does_not_overflow_stack(self) -> None:
        values = list(range(2_000))

        quicksort(values)

        self.assertEqual(values, list(range(2_000)))

    def test_sorts_in_place(self) -> None:
        values = [3, 2, 1]
        original_id = id(values)

        result = quicksort(values)

        self.assertEqual(id(result), original_id)
        self.assertEqual(values, [1, 2, 3])

    def test_lomuto_partition_property(self) -> None:
        values = [9, 3, 7, 1, 5]

        pivot_index = lomuto_partition(
            values,
            0,
            len(values) - 1,
        )

        pivot = values[pivot_index]

        self.assertTrue(
            all(
                value <= pivot
                for value in values[:pivot_index]
            )
        )

        self.assertTrue(
            all(
                value > pivot
                for value in values[pivot_index + 1:]
            )
        )


class RandomizedQuicksortTests(unittest.TestCase):
    """Tests for the randomized Quicksort implementation."""

    def test_empty_list(self) -> None:
        values: list[int] = []

        result = randomized_quicksort(
            values,
            random.Random(1),
        )

        self.assertIs(result, values)
        self.assertEqual(values, [])

    def test_single_element(self) -> None:
        values = [7]

        randomized_quicksort(
            values,
            random.Random(1),
        )

        self.assertEqual(values, [7])

    def test_sorted_input(self) -> None:
        values = list(range(100))

        randomized_quicksort(
            values,
            random.Random(2),
        )

        self.assertEqual(values, list(range(100)))

    def test_reverse_sorted_input(self) -> None:
        values = list(range(100, 0, -1))
        expected = sorted(values)

        randomized_quicksort(
            values,
            random.Random(3),
        )

        self.assertEqual(values, expected)

    def test_duplicate_values(self) -> None:
        values = [5, 1, 5, 3, 1, 5, 2, 2]
        expected = sorted(values)

        randomized_quicksort(
            values,
            random.Random(4),
        )

        self.assertEqual(values, expected)

    def test_all_equal_values(self) -> None:
        values = [6] * 200

        randomized_quicksort(
            values,
            random.Random(5),
        )

        self.assertEqual(values, [6] * 200)

    def test_negative_values(self) -> None:
        values = [-5, -10, -1, -7, 0]
        expected = sorted(values)

        randomized_quicksort(
            values,
            random.Random(6),
        )

        self.assertEqual(values, expected)

    def test_multiple_random_seeds(self) -> None:
        source_rng = random.Random(532)

        source = [
            source_rng.randint(-10_000, 10_000)
            for _ in range(1_000)
        ]

        expected = sorted(source)

        for seed in range(10):
            with self.subTest(seed=seed):
                values = source.copy()

                randomized_quicksort(
                    values,
                    random.Random(seed),
                )

                self.assertEqual(values, expected)

    def test_large_random_input(self) -> None:
        source_rng = random.Random(1532)

        values = [
            source_rng.randint(
                -1_000_000,
                1_000_000,
            )
            for _ in range(3_000)
        ]

        expected = sorted(values)

        randomized_quicksort(
            values,
            random.Random(2532),
        )

        self.assertEqual(values, expected)

    def test_sorts_in_place(self) -> None:
        values = [3, 2, 1]
        original_id = id(values)

        result = randomized_quicksort(
            values,
            random.Random(7),
        )

        self.assertEqual(id(result), original_id)
        self.assertEqual(values, [1, 2, 3])


if __name__ == "__main__":
    unittest.main(verbosity=2)