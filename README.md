# Roofline-Style Bandwidth vs. Frequency Simulator

## Overview

This Python script implements a simplified Roofline model to estimate multi-threaded CPU performance under varying memory access intensities (α) and CPU frequencies (Q in GHz). It helps identify whether an application is compute-bound or memory-bound and pinpoints the crossover (“knee”) where the performance bottleneck shifts.

### Key Features

* Configurable hardware parameters: number of threads (`N_threads`), memory channels (`M_links`), per-channel bandwidth (GB/s), etc.
* Scans combinations of CPU frequency (`Q`) and memory access ratio (`α`), computes both memory-bound and compute-bound FLOPS, and takes the minimum as the actual performance.
* Prints a pivot table of results and plots TFLOPS vs. α curves, clearly showing compute-bound regions (flat) and memory-bound regions (decreasing) along with their crossover points.

## Theoretical Model

Given:

* **N\_threads**: Number of threads
* **M\_links**: Number of shared memory channels
* **S**: Bandwidth per channel (GB/s)
* **α**: Memory access ratio per thread (0 ≤ α ≤ 1)
* **bytes\_per\_flop**: Bytes transferred per floating-point operation
* **Q**: CPU frequency (GHz)
* **flops\_per\_cycle**: FLOPS per thread per clock cycle

1. **Total Memory Bandwidth** (Bytes/s):

   $$
   B_{total} = M_{links} \times S \times 10^9
   $$

2. **Memory-Bound Limit** (FLOP/s):

   $$
   F_{mem} = \frac{B_{total} \times N_{threads}}{bytes\_per\_flop \times (\sum \alpha)}
   $$

   Here, $\sum \alpha$ is the sum of memory access ratios across all threads, approximating total bandwidth demand.

3. **Compute-Bound Limit** (FLOP/s):

   $$
   F_{comp} = Q \times 10^9 \times flops\_per\_cycle \times N_{threads}
   $$

4. **Actual Performance** (FLOP/s):

   $$
   F_{actual} = \min(F_{mem}, F_{comp})
   $$

5. **Crossover Point** (α\_thresh):
   Solving $F_{mem} = F_{comp}$ gives:

   $$
   \alpha_{thresh} = \frac{B_{total}}{bytes\_per\_flop \times Q \times 10^9 \times N_{threads}} = \frac{M_{links} \times S}{bytes\_per\_flop \times Q \times N_{threads}}
   $$

* If **α < α\_thresh**, the workload is **compute-bound**.
* If **α > α\_thresh**, the workload is **memory-bound**.

## Script Structure

* `theoretical_tflops()`: Core function returning FLOP/s based on input parameters.
* `run_exploration()`: Scans a grid of Q and α, prints a pivot table of TFLOPS, and returns a DataFrame of results.
* `plot_results()`: Plots TFLOPS vs. α for each frequency.
* `__main__`: Entry point with example parameters that can be modified.

## Installation and Usage

1. Install dependencies:

   ```bash
   pip install numpy pandas matplotlib
   ```
2. Save the script as `roofline_simulator.py` and make it executable:

   ```bash
   chmod +x roofline_simulator.py
   ```
3. Run the script:

   ```bash
   ./roofline_simulator.py
   ```

   or

   ```bash
   python roofline_simulator.py
   ```

## Parameters

* `N_threads`: Number of parallel threads
* `M_links`: Number of memory channels
* `S`: Bandwidth per channel (GB/s)
* `bytes_per_flop`: Bytes per float operation (e.g., 16 for double-precision)
* `flops_per_cycle`: FLOPS per thread per cycle (adjust for SIMD width)
* `Q_list`, `alpha_list`: Lists of frequencies and memory ratios to explore

## Interpretation of Results

* **Flat Regions** (Compute-Bound): TFLOPS remains constant until α reaches α\_thresh.
* **Declining Regions** (Memory-Bound): TFLOPS decreases approximately as 1/α.
* **Knee Points**: α\_thresh values where the curves transition from flat to declining—key for optimization decisions.

---

This simulator provides quantitative insight into when CPU frequency versus memory bandwidth limits application performance, guiding both algorithm and hardware choices.
