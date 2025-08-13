from tkinter import Tk, Frame, Label, Button, Text, Checkbutton, IntVar, StringVar, ttk
import threading
import os
import shutil

class FiveMCleanerApp:
    def __init__(self, master):
        self.master = master
        master.title("FiveM Cleaner")
        
        self.frame = Frame(master)
        self.frame.pack(padx=10, pady=10)

        self.header = Label(self.frame, text="FiveM Cleaner", font=("Helvetica", 16))
        self.header.pack()

        self.textbox = Text(self.frame, height=10, width=50)
        self.textbox.pack(pady=5)

        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)

        self.restore_keybind_var = IntVar()
        self.restore_keybind = Checkbutton(self.frame, text="Restore Keybind", variable=self.restore_keybind_var)
        self.restore_keybind.pack(pady=5)

        self.start_button = Button(self.frame, text="Start Cleaning", command=self.start_cleaning)
        self.start_button.pack(pady=5)

        self.footer = Label(self.frame, text="Links: [GitHub](https://github.com) | [Documentation](https://docs.example.com)")
        self.footer.pack(pady=5)

    def start_cleaning(self):
        threading.Thread(target=self.clean_fivem).start()

    def clean_fivem(self):
        self.progress['value'] = 0
        self.textbox.delete(1.0, "end")
        self.textbox.insert("end", "Cleaning started...\n")
        
        paths_to_clean = ["path/to/fivem/folder1", "path/to/fivem/folder2"]
        total_paths = len(paths_to_clean)

        for index, path in enumerate(paths_to_clean):
            if os.path.exists(path):
                shutil.rmtree(path)
                self.textbox.insert("end", f"Deleted: {path}\n")
            else:
                self.textbox.insert("end", f"Path not found: {path}\n")
            self.progress['value'] = (index + 1) / total_paths * 100
            self.master.update_idletasks()

        self.textbox.insert("end", "Cleaning completed.\n")

if __name__ == "__main__":
    root = Tk()
    app = FiveMCleanerApp(root)
    root.mainloop()