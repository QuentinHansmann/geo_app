import tkinter as tk
from tkinter import filedialog
import shutil

root = tk.Tk()

def select_file():
    # Open a dialog box to select a file
    file_path = filedialog.askopenfilename()
    destination = '/path/to/destination/folder'
    # Copy the file to the destination folder
    shutil.copy(file_path, destination)

# Create a button to select a file
select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack()

root.mainloop()
