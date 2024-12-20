import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import butter, filtfilt


# DC Component Removal
def remove_dc_batch(signals):
    """
    Remove DC component from multiple signals.
    
    Parameters:
    signals (numpy.ndarray): 2D array where each row is a signal
    """
    return signals - np.mean(signals, axis=1)[:, np.newaxis]



# Bandpass Filter
def create_bandpass_filter(lowcut, highcut, fs, order=4):
    """
    Create Butterworth bandpass filter.
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_bandpass_filter_batch(signals, fs, lowcut=0.5, highcut=40, order=4):
    """
    Apply Butterworth bandpass filter to multiple signals.
    
    Parameters:
    signals (numpy.ndarray): 2D array where each row is a signal
    """
    b, a = create_bandpass_filter(lowcut, highcut, fs, order)
    return np.apply_along_axis(lambda x: filtfilt(b, a, x), 1, signals)



# Signal Normalizing
def normalize_signals_batch(signals):
    """
    Normalize multiple signals to range [0, 1].
    
    Parameters:
    signals (numpy.ndarray): 2D array where each row is a signal
    """
    min_vals = np.min(signals, axis=1)[:, np.newaxis]
    max_vals = np.max(signals, axis=1)[:, np.newaxis]
    return (signals - min_vals) / (max_vals - min_vals)


# Compining all Utilites in one function
def preprocess_ecg_batch(data, fs):
    """
    Complete preprocessing pipeline for multiple ECG signals.
    
    Parameters:
    data (pandas.DataFrame): DataFrame where each row is an ECG signal
    fs (float): Sampling frequency in Hz
    
    Returns:
    DataFrame: preprocessed signals DataFrame
    """
    # Convert DataFrame to numpy array for processing
    signals = data.values
    
    # Apply preprocessing steps
    signals = remove_dc_batch(signals)
    signals = apply_bandpass_filter_batch(signals, fs)
    signals = normalize_signals_batch(signals)
    
    # Convert back to DataFrames with original column names
    processed_df = pd.DataFrame(signals, columns=data.columns, index=data.index)
    
    return processed_df


# Custom plotting function for visualization
def plot_signal_comparison(original_signals, processed_signals, fs, num_examples=3):
    """
    Plot comparison of original and processed signals for a subset of examples.
    
    Parameters:
    original_signals (DataFrame): Original signals
    processed_signals (DataFrame): Processed signals
    fs (float): Sampling frequency
    num_examples (int): Number of example signals to plot
    """
    time = np.arange(original_signals.shape[1]) / fs
    
    # Select random examples if we have more signals than num_examples
    if original_signals.shape[0] > num_examples:
        indices = np.random.choice(original_signals.shape[0], num_examples, replace=False)
    else:
        indices = range(original_signals.shape[0])
    
    fig, axes = plt.subplots(len(indices), 2, figsize=(15, 5*len(indices)))
    
    for idx, signal_idx in enumerate(indices):
        # Plot original signal
        axes[idx, 0].plot(time, original_signals.iloc[signal_idx], 'r-')
        axes[idx, 0].set_title(f'Original Signal {signal_idx}')
        axes[idx, 0].set_xlabel('Time (s)')
        axes[idx, 0].set_ylabel('Amplitude')
        axes[idx, 0].grid(True)
        
        # Plot processed signal
        axes[idx, 1].plot(time, processed_signals.iloc[signal_idx], 'b-')
        axes[idx, 1].set_title(f'Processed Signal {signal_idx}')
        axes[idx, 1].set_xlabel('Time (s)')
        axes[idx, 1].set_ylabel('Normalized Amplitude')
        axes[idx, 1].grid(True)
    
    plt.tight_layout()
    plt.show()
