import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk  
class FileCompressionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("21121034 张庭昀 基于人脸识别的安全压缩 GUI")

        # Variables for user input
        self.username_var = tk.StringVar()
        self.image_path_var = tk.StringVar()
        self.file_path_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.option_var = tk.IntVar()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Username Entry
        tk.Label(self.root, text="Username:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.username_var).grid(row=0, column=1)

        # Image Path Entry
        tk.Label(self.root, text="Image Path:").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.image_path_var).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_image_path).grid(row=1, column=2)

        # File Path Entry
        tk.Label(self.root, text="File Path:").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.file_path_var).grid(row=2, column=1)
        tk.Button(self.root, text="Browse Folder", command=self.browse_file_path).grid(row=2, column=2)
        tk.Button(self.root, text="Browse Zip", command=self.browse_zip_file).grid(row=2, column=3)

        # Password Entry
        tk.Label(self.root, text="Password:").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.password_var, show="*").grid(row=3, column=1)

        # Compression/Extraction Option
        tk.Label(self.root, text="Option:").grid(row=4, column=0)
        tk.Radiobutton(self.root, text="Compress", variable=self.option_var, value=1).grid(row=4, column=1)
        tk.Radiobutton(self.root, text="Extract", variable=self.option_var, value=2).grid(row=4, column=2)

        tk.Label(self.root, text="Image Preview:").grid(row=0, column=2)
        self.image_preview_label = tk.Label(self.root)
        self.image_preview_label.grid(row=0, column=4)

        # Run Button
        tk.Button(self.root, text="Run", command=self.run_core_code).grid(row=5, column=1)

    def browse_image_path(self):
        path = filedialog.askopenfilename()
        self.image_path_var.set(path)
        self.display_image_preview(path)

    def browse_file_path(self):
        path = filedialog.askdirectory()
        self.file_path_var.set(path)

    def browse_zip_file(self):
        path = filedialog.askopenfilename(filetypes=[("Rar Files", "*.rar"), ("All Files", "*.*")])
        self.file_path_var.set(path)

    def run_core_code(self):
        # Get user inputs
        username = self.username_var.get()
        image_path = self.image_path_var.get()
        file_path = self.file_path_var.get()
        password = self.password_var.get()
        option = self.option_var.get()
    
        # Validate inputs
        if not username or not image_path or not file_path or not password or not option:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Execute core code
        try:
            output = subprocess.check_output(['python', 'detect.py', username, image_path, file_path, password, str(option)])
            print(output)
            messagebox.showinfo("Result", output.decode('utf-8', 'ignore'))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_image_preview(self, path):
        try:
            image = Image.open(path)
            image = image.resize((100, 100), Image.ANTIALIAS)  # Resize the image for preview
            photo = ImageTk.PhotoImage(image)

            # Update the image label
            self.image_preview_label.configure(image=photo)
            self.image_preview_label.image = photo  # Keep a reference to avoid garbage collection issues

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image preview: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCompressionGUI(root)
    root.mainloop()
