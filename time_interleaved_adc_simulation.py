import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider

print("==================================================")
print(" TASK 1: STATIC TIME-INTERLEAVED SYSTEM SIMULATION")
print("==================================================")

# --- 1. User Configuration ---
# Registration ID: 2023589 -> Target Time: 5.89 seconds
last_three_digits = "589"

sec = int(last_three_digits[0])
fract = int(last_three_digits[1:])
target_time_static = sec + fract/100.0

print(f"Target Signal Location: {target_time_static} seconds")

# --- 2. System Parameters ---
t_end = 10.0
fs_cont = 10000       # High-res simulation of "continuous" time
t = np.linspace(0, t_end, int(fs_cont * t_end) + 1)

# Samplers that can only sample at a rate of 10 Hz
Fs_low = 10
Ts_low = 1/Fs_low

# Target resolution is 0.01s, requiring 100 Hz effective rate
Fs_req = 100
Ts_req = 1/Fs_req

# Calculate number of branches required (K)
K_static = int(Fs_req / Fs_low)

# --- 3. Generate Continuous Input Signal (Impulse) ---
sigma_static = 0.001
x_cont_static = np.exp(-0.5 * ((t - target_time_static)/sigma_static)**2)

# --- 4. System Simulation (Delays + Sampling) ---
N_high = int(np.floor(t_end * Fs_req)) + 1
y_final_static = np.zeros(N_high)
t_final_static = np.arange(N_high) / Fs_req

# Base timeline for a single 10Hz sampler
t_samples_base_static = np.arange(0, int(np.floor(t_end * Fs_low))+1) * Ts_low

# Loop through each branch (simulating parallel samplers)
for k in range(K_static):
    delay = k * Ts_req
    branch_sample_times = t_samples_base_static + delay
    branch_values = np.interp(branch_sample_times, t, x_cont_static, left=0.0, right=0.0)
    
    # "Adder" / Interleaver logic
    for i, val in enumerate(branch_values):
        idx_high = i * K_static + k
        if idx_high < N_high:
            y_final_static[idx_high] = val

# --- 5. Generate Static Plots ---
zoom_window = 0.5
plt.figure(figsize=(10, 8))

# Plot A: Continuous-Time Signal
plt.subplot(3, 1, 1)
plt.plot(t, x_cont_static, 'g')
plt.title(f'1. Continuous-Time Signal (Impulse at {target_time_static}s)')
plt.xlim(max(0, target_time_static - zoom_window), min(t_end, target_time_static + zoom_window))
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)

# Plot B: Original Discrete-Time Signal (Single 10 Hz Sampler)
x_single_sampler = np.interp(t_samples_base_static, t, x_cont_static, left=0.0, right=0.0)
plt.subplot(3, 1, 2)
plt.stem(t_samples_base_static, x_single_sampler)
plt.title('2. Original Discrete-Time Signal (Single 10 Hz Sampler)')
plt.xlim(max(0, target_time_static - zoom_window), min(t_end, target_time_static + zoom_window))
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)

# Plot C: Final Resampled Signal (100 Hz)
plt.subplot(3, 1, 3)
plt.stem(t_final_static, y_final_static, linefmt='r-', markerfmt='ro', basefmt='k-')
plt.title('3. Final Discrete-Time Signal (Resampled at 100 Hz)')
plt.xlim(max(0, target_time_static - zoom_window), min(t_end, target_time_static + zoom_window))
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n==================================================")
print(" TASK 2: INTERACTIVE SYSTEM EXPLORATION")
print("==================================================")

def simulate_interleaved_system(target_time, K, sigma):
    t_end = 10.0
    fs_cont = 10000        
    t = np.linspace(0, t_end, int(fs_cont * t_end) + 1)
    
    Fs_low = 10
    Ts_low = 1/Fs_low
    Fs_req = Fs_low * K
    Ts_req = 1/Fs_req

    x_cont = np.exp(-0.5 * ((t - target_time)/sigma)**2)
    if np.max(x_cont) > 0:
        x_cont = x_cont / np.max(x_cont)

    N_high = int(np.floor(t_end * Fs_req)) + 1
    y_final = np.zeros(N_high)
    t_final = np.arange(N_high) / Fs_req

    t_samples_base = np.arange(0, int(np.floor(t_end * Fs_low))+1) * Ts_low

    for k in range(K):
        delay = k * Ts_req
        branch_sample_times = t_samples_base + delay
        branch_values = np.interp(branch_sample_times, t, x_cont, left=0.0, right=0.0)

        for i, val in enumerate(branch_values):
            idx_high = i * K + k
            if idx_high < N_high:
                y_final[idx_high] = val

    zoom_window = 0.5
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

    ax1.plot(t, x_cont, 'g')
    ax1.set_title(f'Continuous Input (Target: {target_time:.2f}s)')
    ax1.set_xlim(max(0, target_time - zoom_window), min(t_end, target_time + zoom_window))
    ax1.grid(True, alpha=0.3)

    x_single = np.interp(t_samples_base, t, x_cont, left=0.0, right=0.0)
    ax2.stem(t_samples_base, x_single)
    ax2.set_title('Original Discrete-Time Signal (Single 10 Hz Sampler)')
    ax2.set_xlim(max(0, target_time - zoom_window), min(t_end, target_time + zoom_window))
    ax2.grid(True, alpha=0.3)

    ax3.stem(t_final, y_final, linefmt='r-', markerfmt='ro', basefmt='k-')
    ax3.set_title(f'Final Output (Effective Rate: {Fs_req} Hz with K={K} branches)')
    ax3.set_xlim(max(0, target_time - zoom_window), min(t_end, target_time + zoom_window))
    ax3.set_xlabel('Time (s)')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

# --- Interactive Sliders ---
interact(simulate_interleaved_system,
         target_time=FloatSlider(min=0.1, max=9.9, step=0.01, value=5.89, description='Target Time'),
         K=IntSlider(min=1, max=20, step=1, value=10, description='Branches (K)'),
         sigma=FloatSlider(min=0.001, max=0.02, step=0.001, value=0.002, description='Pulse Width')
        );
