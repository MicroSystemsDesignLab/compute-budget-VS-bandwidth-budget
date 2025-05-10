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

## Theoretical Model

1. **Total Memory Bandwidth** (Bytes/s):  
   ![B_total = M_links × S × 10^9](https://latex.codecogs.com/svg.image?B_{total}=M_{links}\times%20S\times10^9)

2. **Memory-Bound Limit** (FLOP/s):  
   ![F_mem = (B_total × N_threads) / (bytes_per_flop × Σα)](https://latex.codecogs.com/svg.image?F_{mem}=\frac{B_{total}\times%20N_{threads}}{bytes\_per\_flop\times\sum%20\alpha})

3. **Compute-Bound Limit** (FLOP/s):
   ![F_comp = Q × 10^9 × flops_per_cycle × N_threads](https://latex.codecogs.com/svg.image?F_{comp}=Q\times10^9\times flops_{per\_cycle}\times N_{threads})

4. **Actual Performance** (FLOP/s):  
   ![F_actual = min(F_mem, F_comp)](https://latex.codecogs.com/svg.image?F_{actual}=\min(F_{mem},%20F_{comp}))

5. **Crossover Ratio** (α_thresh):  
   ![alpha_thresh = (M_links × S) / (bytes_per_flop × Q × N_threads)](https://latex.codecogs.com/svg.image?\alpha_{thresh}=\frac{M_{links}\times%20S}{bytes\_per\_flop\times%20Q\times%20N_{threads}})


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
   chmod +x main.py
   ```
3. Run the script:

   ```bash
   ./main.py
   ```

   or

   ```bash
   python main.py
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
