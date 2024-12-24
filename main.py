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

def plot_ecg_signal1(data):
    """
    Plot ECG signal from a DataFrame where columns are sample indices
    and the single row contains the signal amplitudes, and render it in a new tkinter window.
    
    Parameters:
    data (pandas.DataFrame): DataFrame containing ECG samples.
    """
    

    # Create a new tkinter window
    new_window = tk.Toplevel()
    new_window.title("ECG Signal Plot")
    new_window.geometry("800x400")

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
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()
knn = joblib.load('knn_model.joblib')
class SignalVisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ECG Classifier for LBBB Detection")
        self.geometry("830x560")
        self.background_image = tk.PhotoImage(file="Pics/blueSignal.png")

        # Add the image as a label
        # Add the image as a label and make it fill the entire window
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
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
        
        # Frame background color
        self.style.configure("TFrame", background="#0B132B")
        
        # Button styling
        self.style.configure(
            "TButton",
            background="#1E90FF",
            foreground="white",
            font=("Helvetica", 12, "bold"),
            borderwidth=0,
            padding=8,
        )
        self.style.map(
            "TButton",
            background=[("active", "#104E8B"), ("pressed", "#0A74DA")],
        )
        
        # Title styling
        self.style.configure(
            "Title.TLabel",
            font=("Helvetica", 18, "bold"),
            background="#1B263B",  # Dark blue background
            foreground="white",
            anchor="center",
        )

    def _create_layout(self):
        """Create the main layout."""
        title_label = ttk.Label(
            self, text="Wavelet-Based ECG Classifier for LBBB Detection", style="Title.TLabel"
        )
        title_label.pack(pady=10)

        self._create_buttons()
    def _create_buttons(self):
        """Create buttons."""
        ttk.Button(
            self, text="Upload Signal File", style="TButton", command=self.upload_signal_file
        ).pack(pady=10)

        ttk.Button(
            self, text="Run model", style="TButton", command=self.preprocess_signals
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
                lbbb = knn.predict(ret)
                print(lbbb)
                if lbbb == 1 :
                    messagebox.showwarning("Bad News", "The person is diagnosed with Left Bundle Branch Block (LBBB)")
                else :
                    messagebox.showinfo("good News", "The person is not diagnosed with Left Bundle Branch Block (LBBB)")

           # except Exception as e:
            #    messagebox.showerror("Error", f"Failed to preprocess signals: {e}")
        else:
            messagebox.showerror("Error", "No signal file uploaded!")

        """Visualize the original and processed signals."""
        if self.original_signals is not None : 
            # Visualize original signal
            try:
                plot_ecg_signal1(self.original_signals)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot signals: {e}")
        else:
            messagebox.showerror("Error", "upload the signals before visualizing!")


if __name__ == "__main__":
    app = SignalVisualizerApp()
    app.mainloop()
    