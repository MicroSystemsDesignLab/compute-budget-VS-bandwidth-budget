# Roofline-Style Bandwidth vs. Frequency Simulator

**Company Confidential**  
**Penn State MicroDesignLab © 2025 Penn State MicroDesignLab**  
**Author: Pingyi Huo**

---

## Overview

This script implements a simplified Roofline model to estimate multi-threaded CPU performance under varying memory access ratios (α) and CPU frequencies (Q in GHz). It identifies whether the workload is compute-bound or memory-bound and locates the crossover (“knee”) point.

---

## Features

- **Configurable hardware parameters:**
  - `N_threads`  
  - `M_links`  
  - `S` (Channel bandwidth in GB/s)  
  - `bytes_per_flop`  
  - `flops_per_cycle`  
- Scans a grid of CPU frequencies (`Q_list`) and memory access ratios (`alpha_list`)  
- Computes both memory-bound and compute-bound throughput and selects the minimum  
- Prints a pivot table of TFLOPS vs. α  
- Plots TFLOPS vs. α curves with clear labels  

---

## Theoretical Model

**Total Memory Bandwidth (Bytes/s):**  
\[
B_{\text{total}} = M_{\text{links}} \times S \times 10^9
\]

**Memory-Bound Limit (FLOP/s):**  
\[
F_{\text{mem}} = \frac{B_{\text{total}} \times N_{\text{threads}}}{\text{bytes\_per\_flop} \times \sum \alpha}
\]

**Compute-Bound Limit (FLOP/s):**  
\[
F_{\text{comp}} = Q \times 10^9 \times \text{flops\_per\_cycle} \times N_{\text{threads}}
\]

**Actual Performance:**  
\[
F_{\text{actual}} = \min\bigl(F_{\text{mem}},\,F_{\text{comp}}\bigr)
\]

**Crossover Ratio (αₜₕᵣₑₛₕ):**  
\[
\alpha_{\text{thresh}} = \frac{M_{\text{links}} \times S}
                          {\text{bytes\_per\_flop} \times Q \times N_{\text{threads}}}
\]

- If \(\alpha < \alpha_{\text{thresh}}\): **compute-bound**  
- If \(\alpha > \alpha_{\text{thresh}}\): **memory-bound**

---

## Installation

```bash
pip install numpy pandas matplotlib
Usage
Save the script as roofline_simulator.py.

Make it executable:

bash
Copy
Edit
chmod +x roofline_simulator.py
Run:

bash
Copy
Edit
./roofline_simulator.py
# or
python roofline_simulator.py
Configuration
python
Copy
Edit
# Number of parallel threads
N_threads = 4

# Number of memory channels
M_links = 4

# Bandwidth per channel in GB/s
S = 25.0

# Bytes per floating-point operation
bytes_per_flop = 16

# FLOPS per thread per cycle
flops_per_cycle = 1

# List of CPU frequencies to explore (GHz)
Q_list = [1.0, 1.5, 2.0, 2.5, 3.0]

# List of memory access ratios to explore
alpha_list = [0.1, 0.5, 1.0, 2.0, 5.0]
Output
Console: Pivot table of α vs. TFLOPS for each frequency

Plot: Graph of TFLOPS vs. α curves

Interpretation
Flat Regions: Compute-bound, TFLOPS limited by CPU frequency

Declining Regions: Memory-bound, TFLOPS inversely proportional to α

Knee Points: α_thresh where the bottleneck switches

Use these insights to guide algorithmic optimizations and hardware tuning.

Contact
For questions or contributions, contact Pingyi Huo at Penn State MicroDesignLab.
