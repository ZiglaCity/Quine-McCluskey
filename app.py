import tkinter as tk
from tkinter import ttk

class Quine_McCluskey:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Zigla's Quine-McCluskey Minimizer")
        self.root.geometry("600x400") 
        self.root.resizable(False, False)
        self.apply_global_style() 
        self.setup_ui()

    def apply_global_style(self):
        style = ttk.Style()
        style.theme_use('vista')  # Using 'clam' theme for a modern look
        style.theme_use('clam')

        style.configure('TFrame', background='#ffffff')
        style.configure('TLabel', background='#ffffff', font=('Arial', 18, 'bold'))
        style.configure('TEntry', font=('Arial', 14), padding=10, width=30)
        style.configure('TButton', font=('Arial', 14), padding=10)

    def setup_ui(self):
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(expand=True, fill="both")

        ttk.Label(form_frame, text="ZIGLA's").pack()
        header_label = ttk.Label(form_frame, text="Quine-McCluskey Minimizer", style='TLabel')
        header_label.pack(pady=10)

        self.minterms_entry = ttk.Entry(form_frame, style='TEntry')
        self.minterms_entry.pack(pady=10, fill="x")
        self.add_placeholder(self.minterms_entry, "Enter minterms (e.g., 0, 1, 2)")

        self.dont_cares_entry = ttk.Entry(form_frame, style='TEntry')
        self.dont_cares_entry.pack(pady=10, fill="x")
        self.add_placeholder(self.dont_cares_entry, "Enter don't cares (e.g., 3, 4)")

        self.variables_entry = ttk.Entry(form_frame, style='TEntry')
        self.variables_entry.pack(pady=10, fill="x")
        self.add_placeholder(self.variables_entry, "Enter variables (e.g., A, B, C)")

        solve_button = ttk.Button(form_frame, text="Solve", command=self.solve)
        solve_button.pack(pady=20)

    def add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.on_focus_in(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.on_focus_out(entry, placeholder))

    def on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def check_inputs(self, inputs):
        for item in inputs:
            if not item.isdigit():
                raise ValueError(f"Invalid input: {item}. All inputs should be integers.")
        return True

    def solve(self):
        minterms = self.minterms_entry.get().replace(" ", "").strip(',')
        dont_cares = self.dont_cares_entry.get().replace(" ", "").strip(',')
        variables = self.variables_entry.get().replace(" ", "").strip(',')

        minterms_list = minterms.split(',')
        dont_cares_list = dont_cares.split(',')
        variables_list = variables.split(',')

        if self.dont_cares_entry.get() == "Enter don't cares (e.g., 3, 4)":
            dont_cares_list = []
        if self.variables_entry.get() == "Enter variables (e.g., A, B, C)":
            variables_list = ['A', 'B', 'C', 'D']

        try:
            self.check_inputs(minterms_list)
            self.check_inputs(dont_cares_list)
        except ValueError as e:
            print(e)
            return

        if int(max(minterms_list)) > 15:
            print("Minterm greater than expected!")

        print(f"Minterms: {minterms_list}")
        print(f"Don't Cares: {dont_cares_list}")
        print(f"Variables: {variables_list}")

        print("Solving...")

if __name__ == "__main__":
    root = tk.Tk()
    app = Quine_McCluskey(root)
    root.mainloop()
