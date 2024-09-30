import tkinter as tk
from tkinter import filedialog
from script import select_and_read_file

def on_button_click():
    #run the file read script in script.py
    file_path = filedialog.askopenfilename(title="Select a file")
    select_and_read_file(file_path)

#makes the ui
def create_ui():
    root = tk.Tk()
    root.title("File Reader")

    label = tk.Label(root, text="Click to select file to read")
    label.pack(pady=10)
    label.pack(padx=50)

    button = tk.Button(root, text="Select File", command=on_button_click)
    button.pack(pady=10)
    button.pack(padx=50)

    root.mainloop()


if __name__ == "__main__":
    create_ui()