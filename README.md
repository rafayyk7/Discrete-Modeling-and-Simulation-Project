# Time-Interleaved ADC System Simulation

**Author:** Abdul Rafay Khan   
**Institution:** Ghulam Ishaq Khan Institute of Engineering Sciences and Technology (GIKI)  

## 🚀 Project Overview
This project simulates an interactive Time-Interleaved Analog-to-Digital Converter (ADC) system. The core objective is to demonstrate how multiple slow-speed samplers (10 Hz) can be operated in parallel with precise time delays to achieve a much higher effective sampling rate (100+ Hz). This technique is crucial in modern digital signal processing for capturing high-frequency, narrow transient signals (like Gaussian impulses) without requiring hardware with native high-speed clocks.

## 🛠️ Tech Stack & Methodology
* **Language:** Python
* **Environment:** Google Colab / Jupyter Notebook
* **Key Libraries:** `numpy`, `matplotlib`, `ipywidgets`
* **Core DSP Concepts:** Continuous-to-Discrete sampling, Time-Interleaving, Interpolation, and Signal Aliasing resolution.

## 📊 Key Features & Results
* **Mathematical Modeling:** Accurately models a continuous-time Gaussian impulse and simulates the discrete sampling process across $K$ parallel branches.
* **Algorithm Design:** Implements an interleaver logic formula (`index_high = index_low * K + branch_k`) to seamlessly reconstruct the high-speed output array from delayed low-speed arrays.
* **Interactive Exploration:** Features a dynamic UI utilizing `ipywidgets`, allowing users to adjust the target signal time, the number of parallel branches ($K$), and the pulse width ($\sigma$) in real-time to observe the immediate effects on signal reconstruction and system resolution.

## 💻 How to Run
1. Clone this repository to your local machine.
2. Install the required dependencies: 
   ```bash
   pip install numpy matplotlib ipywidgets
