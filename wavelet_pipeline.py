import pywt
import numpy as np
import pandas as pd
from scipy.stats import skew
import matplotlib.pyplot as plt
from tqdm import tqdm

def apply_dwt(signal, wavelet, level):
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    reconstructed_signals = []
    
    for i in range(level + 1):
        coeff_list = [np.zeros_like(c) for c in coeffs]
        coeff_list[i] = coeffs[i]
        reconstructed = pywt.waverec(coeff_list, wavelet)
        
        if len(reconstructed) != len(signal):
            reconstructed = reconstructed[:len(signal)]
            
        reconstructed_signals.append(reconstructed)
    
    return coeffs, reconstructed_signals

def evaluate_statistics(original, reconstructed):
    """
    Compare statistical measures between original and reconstructed signals.
    """
    # Calculate statistics for both signals
    orig_mean = np.mean(original)
    orig_std = np.std(original)
    orig_skew = skew(original)
    
    recon_mean = np.mean(reconstructed)
    recon_std = np.std(reconstructed)
    recon_skew = skew(reconstructed)
    
    # Calculate preservation ratios (closer to 1 is better)
    mean_preservation = 1 - abs(orig_mean - recon_mean) / abs(orig_mean) if orig_mean != 0 else 0
    std_preservation = 1 - abs(orig_std - recon_std) / orig_std if orig_std != 0 else 0
    skew_preservation = 1 - abs(orig_skew - recon_skew) / abs(orig_skew) if orig_skew != 0 else 0
    
    return {
        'mean_preservation': mean_preservation,
        'std_preservation': std_preservation,
        'skew_preservation': skew_preservation
    }

def analyze_dwt_parameters(data, wavelets=['db3', 'db4', 'db6'], levels=[3, 4]):
    results = []
    
    for wavelet in wavelets:
        for level in levels:
            print(f"\nAnalyzing {wavelet} with level {level}")
            
            for idx in tqdm(range(len(data))):
                signal = data.iloc[idx].values
                _, reconstructed_signals = apply_dwt(signal, wavelet, level)
                
                for i, rec_signal in enumerate(reconstructed_signals):
                    metrics = evaluate_statistics(signal, rec_signal)
                    metrics.update({
                        'wavelet': wavelet,
                        'decomp_level': level,
                        'coeff_level': i,
                        'signal_idx': idx
                    })
                    results.append(metrics)
    
    return pd.DataFrame(results)

def plot_statistical_comparison(results_df):
    summary = results_df.groupby(['wavelet', 'decomp_level', 'coeff_level'])[
        ['mean_preservation', 'std_preservation', 'skew_preservation']
    ].mean().reset_index()
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 6), constrained_layout=True)
    metrics = ['mean_preservation', 'std_preservation', 'skew_preservation']
    titles = ['Mean Preservation', 'STD Preservation', 'Skewness Preservation']
    
    for i, (metric, title) in enumerate(zip(metrics, titles)):
        for wavelet in summary['wavelet'].unique():
            data = summary[summary['wavelet'] == wavelet]
            axes[i].plot(data['coeff_level'], data[metric], 
                        marker='o', label=f'{wavelet}')
            
        axes[i].set_title(title)
        axes[i].set_xlabel('Coefficient Level')
        axes[i].set_ylabel('Preservation Ratio')
        axes[i].grid(True)
        axes[i].legend()
    
    #plt.tight_layout()
    return fig

