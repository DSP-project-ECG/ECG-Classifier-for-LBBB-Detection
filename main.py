import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from utils import preprocess_ecg_batch, extract_wavelet_features
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import pywt
from scipy.stats import skew, kurtosis

def plot_ecg_signal1(root, data):
    """
    Plot ECG signal from a DataFrame where columns are sample indices
    and the single row contains the signal amplitudes, and render it in a tkinter window.
    
    Parameters:
    root (tk.Tk or tk.Frame): The tkinter root or frame where the plot will be embedded.
    data (pandas.DataFrame): DataFrame containing ECG samples.
    """
    # Convert the single row to a DataFrame suitable for plotting
    signal_df = pd.DataFrame({
        'Sample': range(len(data.columns)),
        'Amplitude': data.iloc[0].values
    })
    
    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.set_style("whitegrid")
    
    # Plot the signal
    sns.lineplot(data=signal_df, x='Sample', y='Amplitude', ax=ax, linewidth=1, color='red')
    
    # Customize the plot
    ax.set_title('ECG Signal', pad=15)
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Amplitude')
    fig.tight_layout()
    
    # Embed the matplotlib figure in tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()
knn = joblib.load('knn_model.joblib')
class SignalVisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Signal Processing Application")
        self.geometry("830x560")

        # Add GUI components
        self.style = ttk.Style(self)
        self._set_theme()
        self._create_layout()
        
        # Variables
        self.original_signals = None
        self.processed_signals = None
        self.feature_vector = None
        self.fs = 360  # Default sampling frequency (can be adjusted)
    
    def _set_theme(self):
        """Set the ttk theme and style."""
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#F8FAFC")
        self.style.configure(
            "TButton",
            background="#007BFF",
            foreground="white",
            font=("Helvetica", 12),
            borderwidth=0,
            padding=6,
        )
        self.style.map(
            "TButton",
            background=[("active", "#0056B3"), ("pressed", "#004085")],
        )
        self.style.configure(
            "Title.TLabel",
            font=("Helvetica", 16, "bold"),
            background="#F8FAFC",
            foreground="#343A40",
        )

    def _create_layout(self):
        """Create the main layout."""
        title_label = ttk.Label(
            self, text="Signal Processing Application", style="Title.TLabel"
        )
        title_label.pack(pady=10)

        self._create_buttons()
        self.plot_frame = ttk.Frame(self, padding=10)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def _create_buttons(self):
        """Create buttons."""
        ttk.Button(
            self, text="Upload Signal File", style="TButton", command=self.upload_signal_file
        ).pack(pady=10)

        ttk.Button(
            self, text="Preprocess Signals", style="TButton", command=self.preprocess_signals
        ).pack(pady=10)

        ttk.Button(
            self, text="Visualize Signals", style="TButton", command=self.visualize_signals
        ).pack(pady=10)

    def upload_signal_file(self):
        """Handle uploading a signal file."""
        file_path = filedialog.askopenfilename()                 
        if file_path:
            try:
                self.original_signals = pd.read_csv(file_path,delimiter = '|', header=None)
                self.original_signals = self.original_signals.iloc[:, :-1]
                messagebox.showinfo("Success", "File uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
        else:
            messagebox.showinfo("Cancelled", "File upload cancelled.")

    def preprocess_signals(self):
        """Preprocess the uploaded signals."""
        if self.original_signals is not None:
           # try:
                self.processed_signals = preprocess_ecg_batch(self.original_signals, self.fs)
                self.processed_signals = self.processed_signals.iloc[:, :-1].values
                ret = extract_wavelet_features(self.processed_signals)
                print(ret)
                print(knn.predict(ret))
                messagebox.showinfo("Success", "Signals preprocessed successfully!")
           # except Exception as e:
            #    messagebox.showerror("Error", f"Failed to preprocess signals: {e}")
        else:
            messagebox.showerror("Error", "No signal file uploaded!")

    def visualize_signals(self):
        """Visualize the original and processed signals."""
        if self.original_signals is not None :
            # Clear previous plot
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            # Create the plot
            figure = Figure(figsize=(8, 4), dpi=100)
            axis = figure.add_subplot(111)

            # Visualize original signal
            try:
                plot_ecg_signal1(self,self.original_signals)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot signals: {e}")
        else:
            messagebox.showerror("Error", "upload the signals before visualizing!")


if __name__ == "__main__":
    app = SignalVisualizerApp()
    app.mainloop()
    