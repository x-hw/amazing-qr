import os
import tkinter as tk
from tkinter import filedialog, ttk

from sv_ttk import use_dark_theme

from amzqr.amzqr import run


class QRCodeApp(tk.Tk):
    """A simpler UI interface for creating QR codes"""

    def __init__(self):
        super().__init__()
        self.title("Amazing QR")
        self.vars = {
            "input_text": tk.StringVar(),
            "version": tk.IntVar(value=7),
            "level": tk.StringVar(value="H"),
            "picture": tk.StringVar(),
            "colorized_picture": tk.BooleanVar(value=True),
            "contrast": tk.DoubleVar(value=1.0),
            "brightness": tk.DoubleVar(value=1.0),
            "filename_out": tk.StringVar(),
            "output_directory": tk.StringVar(value=os.getcwd()),
        }
        self.create_widgets()

    def add_picture_quality_frame(self):
        """Image quality settings"""
        ttk.Label(self, text="📷 Image Quality")\
            .grid(row=2, column=0, sticky="NSEW", padx=5, pady=3)
        frame0 = ttk.Frame(self)
        frame0.grid(row=3, column=0, columnspan=5, sticky="NSEW", pady=10)
        frame1 = ttk.Frame(self)
        frame1.grid(row=4, column=0, columnspan=5, sticky="NSEW", pady=10)
        frame2 = ttk.Frame(self)
        frame2.grid(row=5, column=0, columnspan=5, sticky="NSEW", pady=10)

        # Row 0 : file picker
        ttk.Label(frame0, text="Picture: ")\
            .grid(row=0, column=0, sticky="NSEW", padx=(30, 10))
        ttk.Entry(frame0, textvariable=self.vars["picture"], width=45)\
            .grid(row=0, column=1, padx=5)
        ttk.Button(frame0, text="Browse", command=self.select_picture)\
            .grid(row=0, column=2, padx=5)

        # Row 1: image dimensions, ecc
        ttk.Label(frame1, text="Height/Width:")\
            .grid(row=0, column=0, sticky="NSEW", padx=(30, 2))
        ttk.Combobox(
            frame1, textvariable=self.vars["version"], values=list(range(1, 41)), width=8)\
            .grid(row=0, column=1)

        ttk.Label(frame1, text="Error Correction Level:")\
            .grid(row=0, column=2, sticky="NSEW", padx=(30, 2))
        ttk.Combobox(
            frame1, textvariable=self.vars["level"], values=("L", "M", "Q", "H"), width=8)\
            .grid(row=0, column=3)

        #  Row 2: Colorized, Contrast, Brightness
        ttk.Checkbutton(frame2, text="Colorized", variable=self.vars["colorized_picture"])\
            .grid(row=0, column=0, sticky="NSEW", padx=30)
        ttk.Label(frame2, text="Contrast:")\
            .grid(row=0, column=1, sticky="NSEW", padx=(63, 5))
        ttk.Entry(frame2, textvariable=self.vars["contrast"], width=4)\
            .grid(row=0, column=2, sticky="NSEW")

        ttk.Label(frame2, text="Brightness:")\
            .grid(row=0, column=3, sticky="NSEW", padx=(63, 5))
        ttk.Entry(frame2, textvariable=self.vars["brightness"], width=4)\
            .grid(row=0, column=4, sticky="NSEW")

    def add_output_frame(self):
        """Output settings frame"""
        ttk.Label(self, text="🗃 Output settings")\
            .grid(row=6, column=0, sticky="NSEW", padx=5, pady=3)

        outframe = ttk.Frame(self)
        outframe.grid(row=7, column=0, columnspan=5, sticky="NSEW", pady=10)
        outframe2 = ttk.Frame(self)
        outframe2.grid(row=8, column=0, columnspan=5, sticky="NSEW", pady=10)

        ttk.Label(outframe, text="Filename:")\
            .grid(row=0, column=0, sticky="NSEW", padx=(30, 10))
        ttk.Entry(outframe, textvariable=self.vars["filename_out"], width=45)\
            .grid(row=0, column=1, padx=5)

        ttk.Label(outframe2, text="Directory:")\
            .grid(row=0, column=0, sticky="NSEW", padx=(30, 8))
        ttk.Entry(outframe2, textvariable=self.vars["output_directory"], width=45)\
            .grid(row=0, column=1, padx=5)
        ttk.Button(outframe2, text="Browse", command=self.select_directory)\
            .grid(row=0, column=2, padx=(0, 0))

    def create_widgets(self):
        """Input fields similar to those in terminal.py"""
        ttk.Label(self, text="⌨ Text to encode")\
            .grid(row=0, column=0, sticky="NSEW", padx=5, pady=3)
        ttk.Entry(self, textvariable=self.vars["input_text"], width=65)\
            .grid(row=1, column=0, padx=(30, 10), pady=2, sticky="NSEW")

        self.add_picture_quality_frame()
        self.add_output_frame()

        ttk.Button(self, text="Generate QR Code", command=self.generate_qr)\
            .grid(row=9, column=0, pady=5, sticky="NSEW")

    def select_picture(self):
        """Image handler"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.png *.bmp *.gif")])
        if file_path:
            self.vars["picture"].set(file_path)
            if not self.vars["filename_out"].get():
                name, ext = os.path.splitext(file_path.split("/")[-1])
                self.vars["filename_out"].set(f'{name}_qrcode{ext}')

    def select_directory(self):
        """Output directory picker"""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.vars["output_directory"].set(dir_path)

    def display_qrcode(self, qr_name):
        """Display the QR code in a new window"""
        img = tk.PhotoImage(file=qr_name)
        label = tk.Label(tk.Toplevel(self), image=img)
        label.garbage_collection_prevention = img
        label.pack()

    def generate_qr(self):
        """Run main method"""
        params = {
            "Words": self.vars["input_text"].get(),
            "Version": self.vars["version"].get(),
            "Level": self.vars["level"].get(),
            "Picture": self.vars["picture"].get(),
            "Colorized": self.vars["colorized_picture"].get(),
            "Contrast": self.vars["contrast"].get(),
            "Brightness": self.vars["brightness"].get(),
            "Name": self.vars["filename_out"].get(),
            "Directory": self.vars["output_directory"].get(),
        }
        _, _, filename = run(*params.values())
        self.display_qrcode(filename)


def main():
    """Runs the tkinter UI"""
    app = QRCodeApp()
    use_dark_theme(app)
    app.mainloop()


if __name__ == "__main__":
    main()
