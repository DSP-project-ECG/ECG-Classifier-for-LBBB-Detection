import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import PhotoImage

class SignalVisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Signal Processing Application")
        self.geometry("830x560")

        # Load the background image
        self.background_image = tk.PhotoImage(file="Pics/blueSignal.png")

        # Add the image as a label and make it fill the entire window
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Configure style and layout
        self.style = ttk.Style(self)
        self._set_theme()
        self._create_layout()
    def _set_theme(self):
        """Set the ttk theme and style."""
        self.style.theme_use("clam")

        # Frame Styling
        self.style.configure("TFrame", background="#F8FAFC")

        # Button Styling
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

        # Accent Button Styling for primary actions
        self.style.configure(
            "Accent.TButton",
            background="#28A745",
            foreground="white",
            font=("Helvetica", 12, "bold"),
            borderwidth=0,
            padding=8,
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", "#218838"), ("pressed", "#1E7E34")],
        )

        # Label Styling
        self.style.configure(
            "TLabel",
            background="#343A40",
            foreground="#F8FAFC",
            font=("Helvetica", 12),
        )
        self.style.configure(
            "Title.TLabel",
            font=("Helvetica", 16, "bold"),
            background="#F8FAFC",
            foreground="#343A40",
        )

    def _create_layout(self):
        """Create the main layout."""
        # Title Section
        title_label = ttk.Label(
        self,
        text="Signal Processing Application",
        style="TLabel",
        anchor="center",
        font=("Helvetica", 24, "bold"),  
        )
        title_label.pack(pady=10)
        

        # Set the background color of the main window (if needed)
        # Main Plotting Area
    #    self._create_plot_area()

        # Buttons Section
        self._create_buttons()

    def _create_plot_area(self):
        """Create a placeholder plot area."""
        plot_frame = ttk.Frame(self, style="TFrame")
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.plot.set_title("Signal Plot")
        self.plot.set_xlabel("Time")
        self.plot.set_ylabel("Amplitude")

        canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

    def _create_buttons(self):
       """Create the buttons below the plot."""

       ttk.Button(
        self, text="Run Model", style="TButton", command=self.upload_signal_file
       ).pack(pady=10)

       

    def upload_signal_file(self):
        """Handle uploading a signal file."""
        print("Upload Signal File clicked!")

    def run_model(self):
        """Handle running the model."""
        print("Run Model clicked!")


if __name__ == "__main__":
    app = SignalVisualizerApp()
    app.mainloop()