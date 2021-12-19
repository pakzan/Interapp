import os
import win32gui
import tkinter as tk
import tkinter.ttk as ttk
import face2emo

class ActionWindow():
    def __init__(self, root, action_num, click_fn):
        frame = tk.Frame(root)

        self.texts = []
        self.labels = []
        for i in range(action_num):
            text = tk.StringVar()
            label = ttk.Label(frame, textvariable=text)
            label.grid(row=i, column=2)

            self.texts.append(text)
            self.labels.append(label)
            # set action button UI
            ttk.Button(
                frame, text='Helpful', command=lambda i=i: click_fn(self.texts[i].get())
            ).grid(row=i, column=1)
        frame.pack(padx=10, pady=10)

    def update_label(self, ind, text, size):
        self.texts[ind].set(text)
        self.labels[ind].config(font=("Helvetica", size))

class MenuWindow():
    def __init__(self, root):
        self.win_dics = {}
        self.choices = []
        self.win_dimen = 0
        win32gui.EnumWindows(self.win_handler, None)

        frame = tk.Frame(root)
        self.win_op_var = tk.StringVar()
        ttk.Label(frame, text="Window to analyse: ").grid(row=1, column=1)
        ttk.OptionMenu(frame, self.win_op_var, *self.choices).grid(row=1, column=2)
        self.win_op_var.trace('w', self.onchange_dropdown)

        frame.pack(padx=10, pady=10)

    def win_handler(self, hwnd, ctx):
        win_text = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowVisible(hwnd) and win_text != '':
            self.win_dics[win_text] = hwnd
            self.choices.append(win_text)

    def onchange_dropdown(self, *args):
        self.win_dimen = face2emo.find_windows_dimension_from_hwnd(
            self.win_dics[self.win_op_var.get()]
        )

class ProgressWindow():
    def __init__(self, root, progress_l):
        frame = tk.Frame(root)

        self.bars = []
        for i, name in enumerate(progress_l):
            var = tk.DoubleVar()            
            ttk.Label(frame, text=name).grid(row=i, column=1)
            ttk.Progressbar(frame, length=300, maximum=1, variable=var).grid(row=i, column=2)
            self.bars.append(var)

        frame.pack(padx=20, pady=20)
        
    def update_label(self, ind, val):        
        bar = self.bars[ind]
        diff = val - bar.get()
        bar.set(bar.get() + diff / 30)

class FileHandler():
    def __init__(self, update_path, data_path):
        self.update_path = update_path
        self.data_path = data_path

    def add_update(self, text):
        with open(self.update_path, "a") as f:
            f.write(text)

    def has_update(self):
        return os.path.exists(self.update_path)

    def update_data(self):
        with open(self.data_path, "a") as date_f:
            with open(self.update_path, "r") as update_f:
                date_f.write(update_f.read())
        os.remove(self.update_path)
