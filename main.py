# -----------------------------------------------------------------------------
# Penn State MicroDesignLab
# Roofline-Style Bandwidth vs. Frequency Simulator
#
# Copyright (c) 2025 Penn State MicroDesignLab.
# Author: Pingyi Huo
# -----------------------------------------------------------------------------

"""
Roofline-Style Bandwidth vs. Frequency Simulator

This script implements a simplified Roofline model to estimate
multi-threaded CPU performance under varying memory access ratios (α)
and CPU frequencies (Q in GHz). It identifies whether the workload
is compute-bound or memory-bound and locates the crossover point.

Assumptions:
  - N_threads: number of parallel threads
  - M_links: number of shared memory channels
  - S: bandwidth per channel (GB/s)
  - alpha_list: list of per-thread memory access ratios
  - Q: CPU frequency (GHz)
  - bytes_per_flop: data transfer in bytes per floating-point operation
  - flops_per_cycle: FLOPS per thread per clock cycle

Dependencies:
  - numpy
  - pandas
  - matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def theoretical_tflops(
    N_threads: int,
    M_links: int,
    S: float,
    alpha_list: list[float],
    Q: float,
    bytes_per_flop: float,
    flops_per_cycle: int = 1
) -> float:
    """
    Compute the theoretical FLOP/s limited by either memory bandwidth or compute.

    Returns:
        float: the achievable FLOP/s
    """
    # Total memory bandwidth in bytes per second
    total_bandwidth = M_links * S * 1e9
    # Sum of memory access ratios across threads
    alpha_sum = sum(alpha_list)
    # Memory-bound performance (FLOP/s)
    mem_bound = total_bandwidth * N_threads / (bytes_per_flop * alpha_sum)
    # Compute-bound performance (FLOP/s)
    comp_bound = Q * 1e9 * flops_per_cycle * N_threads
    # Actual performance is the minimum of the two
    return min(mem_bound, comp_bound)


def run_exploration(
    N_threads: int = 16,
    M_links: int = 4,
    S: float = 25.0,
    bytes_per_flop: float = 16,
    flops_per_cycle: int = 1,
    Q_list: np.ndarray = None,
    alpha_list: np.ndarray = None
) -> pd.DataFrame:
    """
    Explore a grid of CPU frequencies and memory access ratios,
    computing the corresponding TFLOPS and classification.

    Returns:
        pd.DataFrame: results with columns [Q_GHz, alpha, alpha_thresh, TFLOPS, Bound]
    """
    if Q_list is None:
        Q_list = np.arange(1, 5)  # GHz
    if alpha_list is None:
        alpha_list = np.linspace(0.1, 1.0, 10)

    records = []
    for Q in Q_list:
        # Calculate crossover ratio alpha_thresh
        alpha_thresh = (M_links * S) / (bytes_per_flop * Q * N_threads)
        for alpha in alpha_list:
            flops = theoretical_tflops(
                N_threads, M_links, S,
                [alpha] * N_threads,
                Q, bytes_per_flop, flops_per_cycle
            )
            tf = flops / 1e12  # convert to TFLOPS
            bound = 'Compute-bound' if alpha < alpha_thresh else 'Memory-bound'
            records.append({
                'Q_GHz': Q,
                'alpha': round(alpha, 3),
                'alpha_thresh': round(alpha_thresh, 3),
                'TFLOPS': round(tf, 6),
                'Bound': bound
            })

    df = pd.DataFrame(records)
    # Print pivot table to console
    print("\n=== Simulation Results ===")
    pivot = df.pivot(index='alpha', columns='Q_GHz', values='TFLOPS')
    print(pivot)
    return df


def plot_results(df: pd.DataFrame) -> None:
    """
    Plot TFLOPS vs. memory access ratio for each CPU frequency.
    """
    plt.figure(figsize=(8, 6))
    for Q in sorted(df['Q_GHz'].unique()):
        subset = df[df['Q_GHz'] == Q]
        plt.plot(
            subset['alpha'], subset['TFLOPS'], marker='o',
            label=f'{Q} GHz'
        )
    plt.xlabel('Memory Access Ratio (α)')
    plt.ylabel('Theoretical TFLOPS')
    plt.title('TFLOPS vs α for Different CPU Frequencies')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # User-adjustable parameters
    N_threads = 4
    M_links = 4
    S = 25.0             # GB/s per link
    bytes_per_flop = 16  # bytes per operation
    flops_per_cycle = 1  # FLOPS per thread per cycle

    Q_list = np.arange(1, 5)            # CPU frequencies: 1,2,3,4 GHz
    alpha_list = np.linspace(0.1, 1.0, 10)  # Memory ratios from 0.1 to 1.0

    df = run_exploration(
        N_threads, M_links, S,
        bytes_per_flop, flops_per_cycle,
        Q_list, alpha_list
    )
    plot_results(df)
