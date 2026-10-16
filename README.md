# MSCS 532 Assignment 5 — Quicksort Algorithm: Implementation, Analysis, and Randomization

**Student:** Naga Naveena Chennupati  
**Student ID:** 005063666  
**Course:** MSCS 532 — Algorithms and Data Structures  
**University:** University of the Cumberlands

## Overview

This project implements and analyzes deterministic and randomized versions of the Quicksort algorithm in Python. The deterministic version uses the final element of each active subarray as the pivot and applies Lomuto partitioning. The randomized version selects a pivot uniformly at random from the active subarray before applying the same partitioning procedure.

The project examines the theoretical best, average, and worst cases of Quicksort and evaluates how randomized pivot selection affects performance. An empirical comparison was performed across multiple input sizes and data distributions, including random, sorted, reverse-sorted, and repeated-value inputs.

## Project Structure

```text
MSCS532_Assignment5/
│
├── results/
│   ├── quicksort_trials.csv
│   ├── quicksort_summary.csv
│   ├── random_comparison.png
│   ├── sorted_comparison.png
│   ├── reverse_sorted_comparison.png
│   └── repeated_comparison.png
│
├── .gitignore
├── benchmark_quicksort.py
├── generate_graphs.py
├── NagaNaveenaChennupati_Assignment5.docx
├── quicksort.py
├── randomized_quicksort.py
├── requirements.txt
├── test_quicksort.py
└── README.md
```

## Deterministic Quicksort

The deterministic implementation uses Lomuto partitioning and selects the final element of each active subarray as the pivot. During partitioning, values less than or equal to the pivot are moved to its left, while values greater than the pivot remain on its right.

Using the final element as the pivot makes the effect of input ordering easy to observe. Random input generally produces reasonably distributed partitions, while already sorted or reverse-sorted input can repeatedly produce highly unbalanced partitions.

The implementation sorts the list in place. To control Python call-stack growth, it recursively processes the smaller partition and handles the larger partition iteratively.

## Randomized Quicksort

The randomized implementation selects a pivot uniformly from the current subarray. The selected value is exchanged with the final element and then processed using the same Lomuto partition function as the deterministic version.

Using the same partitioning method in both implementations keeps the empirical comparison focused primarily on the effect of pivot selection.

Randomization does not eliminate the theoretical O(n²) worst case. Instead, it reduces the likelihood that a fixed input arrangement will repeatedly produce poor pivot choices. Its expected running time is therefore O(n log n).

## Complexity Analysis

| Version | Best Case | Average / Expected Case | Worst Case | Auxiliary Stack Space |
|---|---:|---:|---:|---:|
| Deterministic Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Randomized Quicksort | O(n log n) | Expected O(n log n) | O(n²) | O(log n) |

For balanced partitions, the recurrence is approximately:

```text
T(n) = 2T(n/2) + Θ(n)
```

which gives Θ(n log n).

For highly unbalanced partitions, the recurrence becomes approximately:

```text
T(n) = T(n - 1) + Θ(n)
```

which gives Θ(n²).

The implementation recursively processes only the smaller partition and handles the larger partition iteratively. This limits call-stack growth while preserving Quicksort's underlying time-complexity behavior.

## Testing

The project includes 22 automated tests covering both deterministic and randomized Quicksort.

The tests include:

- empty input
- single-element input
- two-element input
- already sorted input
- reverse-sorted input
- duplicate values
- all-equal values
- negative and positive values
- large random datasets
- large sorted datasets
- in-place sorting behavior
- Lomuto partition correctness
- multiple randomized pivot seeds

Run the complete test suite with:

```bash
python -m unittest -v
```

The final validation completed successfully with all 22 tests passing.

## Empirical Methodology

The empirical comparison evaluates both Quicksort implementations using the following input sizes:

- 100
- 500
- 1,000
- 2,000
- 5,000

Four data distributions are tested:

- Random
- Sorted
- Reverse Sorted
- Repeated Values

Each combination of algorithm, input size, and distribution is executed for five trials.

The complete experiment therefore contains:

```text
5 input sizes × 4 distributions × 2 algorithms × 5 trials
= 200 timed sorting runs
```

Execution time is measured using Python's `time.perf_counter_ns()` function. Dataset generation and creation of the expected sorted result occur outside the timed section so that the measurements focus on the sorting operation itself.

Each timed result is validated against Python's expected sorted output before it is recorded. Fixed random seeds are used to make dataset generation and randomized pivot selection reproducible.

Individual trial measurements are stored in:

```text
results/quicksort_trials.csv
```

Aggregated mean and sample standard deviation values are stored in:

```text
results/quicksort_summary.csv
```

## Empirical Results

The following table summarizes the mean running time at the largest tested input size, n = 5000.

| Input Distribution | Deterministic Quicksort | Randomized Quicksort |
|---|---:|---:|
| Random | 4.3880 ms | 5.2693 ms |
| Sorted | 717.9259 ms | 4.4940 ms |
| Reverse Sorted | 464.8349 ms | 4.4472 ms |
| Repeated Values | 33.3521 ms | 34.8809 ms |

## Analysis of Results

### Random Input

For random input, both implementations showed relatively similar growth. At n = 5000, deterministic Quicksort completed in 4.3880 ms compared with 5.2693 ms for randomized Quicksort.

The deterministic implementation was slightly faster in this experiment because the input was already randomly ordered, while randomized pivot selection introduced additional random-number-generation and pivot-exchange overhead. The result is consistent with both versions exhibiting efficient expected behavior on ordinary random input.

### Sorted Input

Sorted input produced the clearest worst-case behavior for deterministic Quicksort. At n = 5000, deterministic Quicksort required 717.9259 ms, while randomized Quicksort required only 4.4940 ms.

Because the deterministic implementation always selects the final element as the pivot, an already sorted array repeatedly places the pivot at an extreme end of the partition. This creates highly unbalanced subproblems and behavior consistent with the Θ(n²) worst case.

Randomized pivot selection prevents the original sorted order from systematically controlling the pivot position and therefore produced much more stable performance.

### Reverse-Sorted Input

Reverse-sorted input produced a similar pattern. At n = 5000, deterministic Quicksort required 464.8349 ms compared with 4.4472 ms for randomized Quicksort.

The deterministic endpoint pivot again creates highly unbalanced partitions, while random pivot selection greatly reduces sensitivity to the original ordering of the input.

### Repeated Values

On repeated-value input, the two implementations performed similarly. At n = 5000, deterministic Quicksort required 33.3521 ms and randomized Quicksort required 34.8809 ms.

The repeated-value dataset contains values from a small range. With two-way Lomuto partitioning, many values equal to the pivot can be placed on the same side of a partition. Randomizing the pivot does not fully address this behavior because many candidate pivots may have equal values.

This result shows that randomization is particularly useful for reducing sensitivity to input ordering, but it does not automatically eliminate every source of unbalanced partitioning.

## Performance Graphs

The `results` directory contains one graph for each tested input distribution:

- `random_comparison.png`
- `sorted_comparison.png`
- `reverse_sorted_comparison.png`
- `repeated_comparison.png`

Each graph displays mean execution time across increasing input sizes. Error bars represent the sample standard deviation across the five trials.

## Setup

Python 3 is required.

Install the plotting dependency with:

```bash
python -m pip install -r requirements.txt
```

## Running the Implementations

Run deterministic Quicksort:

```bash
python quicksort.py
```

Run randomized Quicksort:

```bash
python randomized_quicksort.py
```

## Running the Tests

```bash
python -m unittest -v
```

## Running the Benchmark

```bash
python benchmark_quicksort.py
```

This command generates the benchmark CSV files in the `results` directory.

## Generating the Graphs

After benchmark results have been generated, run:

```bash
python generate_graphs.py
```

This creates the four performance graphs in the `results` directory.
## Final Report

The detailed written analysis, including implementation design, theoretical complexity analysis, empirical methodology, performance results, testing, and discussion, is available in:

`NagaNaveenaChennupati_Assignment5.docx`
## Conclusion

The experiment demonstrates that Quicksort performance depends strongly on pivot selection and input characteristics. Deterministic Quicksort using a fixed endpoint pivot performs efficiently on random input but can degrade substantially on already sorted or reverse-sorted input.

Randomized Quicksort reduces the influence of the original input ordering and produces much more stable performance on those unfavorable arrangements. However, randomization adds some overhead and does not eliminate the O(n²) theoretical worst case.

The repeated-value experiment also shows that randomized pivot selection is not a complete solution for every unfavorable dataset. Partitioning strategy and the number of duplicate values can also influence practical performance.

Overall, the experimental results support the theoretical expectation that randomized pivot selection improves the robustness of Quicksort while maintaining expected O(n log n) performance.