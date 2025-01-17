import tkinter as tk
from tkinter import ttk, messagebox

class Quine_McCluskey:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Zigla's Quine-McCluskey Minimizer")
        self.root.geometry("600x500") 
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
        self.add_placeholder(self.variables_entry, "Enter variables if you want to change default (e.g., A, B, C, D)")

        solve_button = ttk.Button(form_frame, text="Solve", command=self.solve)
        solve_button.pack(pady=30)

        self.answer = tk.StringVar()
        self.answer_label = ttk.Label(form_frame, textvariable=self.answer)
        self.answer_label.pack(pady=20)

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

    def solve(self):
        if self.minterms_entry.get() == "Enter minterms (e.g., 0, 1, 2)":
            return messagebox.showerror("Error!", "Please input minterms to solve!")
        minterms = self.minterms_entry.get().replace(" ", "").strip(',')
        minterms = [int(x) for x in minterms.split(',') if x.isdigit()] #remove all characters which are not numbers
        if not minterms:
            return messagebox.showinfo("Wrong Input!", "Please input numbers for minterms!")
        if int(max(minterms)) > 15:
            return messagebox.showinfo("Exceeded Limit!", "Maximum minterm should be 15, since its 4 variables.")

    
        if self.dont_cares_entry.get() == "Enter don't cares (e.g., 3, 4)":
            dont_cares = []
        else:
            dont_cares = self.dont_cares_entry.get().replace(" ", "").strip(',')
            dont_cares = [int(x) for x in dont_cares.split(',') if x.isdigit()]
            if int(max(dont_cares)) > 15:
                return messagebox.showinfo("Exceeded Limit!", "Maximum dont care should be 15, since its 4 variables.")


        if self.variables_entry.get() == "Enter variables if you want to change default (e.g., A, B, C, D)":
            variables = ['A', 'B', 'C', 'D']
        else:
            variables = self.variables_entry.get().replace(" ", "").strip(',').split(',')
            if len(variables) > 4:
                return messagebox.showinfo("Exceeded Limit!", "Too many variables, input just 4!")


        print(f"Minterms: {minterms}")
        print(f"Don't Cares: {dont_cares}")
        print(f"Variables: {variables}")

        print("Solving...")

        def to_binary(num, num_vars):
            return f"{num:0{num_vars}b}"

        def count_ones(binary):
            return binary.count('1')

        def combine_terms(term1, term2):
            diff_count = 0
            combined = []
            for bit1, bit2 in zip(term1, term2):
                if bit1 != bit2:
                    diff_count += 1
                    combined.append('-')
                else:
                    combined.append(bit1)
            return ''.join(combined) if diff_count == 1 else None

        def find_prime_implicants(minterms, num_vars):
            groups = {i: [] for i in range(num_vars + 1)}
            for minterm in minterms:
                binary = to_binary(minterm, num_vars)
                groups[count_ones(binary)].append(binary)

            prime_implicants = []
            checked = []
            while any(groups.values()):
                next_groups = {i: [] for i in range(num_vars + 1)}
                for i in range(num_vars):
                    for term1 in groups[i]:
                        for term2 in groups[i + 1]:
                            combined = combine_terms(term1, term2)
                            if combined:
                                checked.append(term1)
                                checked.append(term2)
                                next_groups[count_ones(combined)].append(combined)
                prime_implicants.extend([term for group in groups.values() for term in group if term not in checked])
                groups = next_groups

            return prime_implicants

        def build_chart(minterms, prime_implicants):
            chart = {pi: [] for pi in prime_implicants}
            for minterm in minterms:
                binary = to_binary(minterm, len(next(iter(prime_implicants))))
                for pi in prime_implicants:
                    if all(pi_bit == '-' or pi_bit == minterm_bit for pi_bit, minterm_bit in zip(pi, binary)):
                        chart[pi].append(minterm)
            return chart

        def extract_essential_prime_implicants(chart):
            essential_pis = []
            covered_minterms = []

            for pi, minterms in sorted(chart.items()):
                uncovered = [m for m in minterms if m not in covered_minterms]
                if len(uncovered) == 1:
                    essential_pis.append(pi)
                    covered_minterms.extend(minterms)
            return essential_pis, covered_minterms

        def iterative_reduction(chart, essential_pis):
            covered_minterms = []
            for pi in essential_pis:
                covered_minterms.extend(chart[pi])
            covered_minterms = list(set(covered_minterms))

            remaining_chart = {}
            for pi, minterms in chart.items():
                remaining_minterms = [m for m in minterms if m not in covered_minterms]
                if remaining_minterms:
                    remaining_chart[pi] = remaining_minterms

            while remaining_chart:
                max_pi = max(remaining_chart, key=lambda pi: len(remaining_chart[pi]))
                essential_pis.append(max_pi)
                covered_minterms.extend(remaining_chart[max_pi])
                covered_minterms = list(set(covered_minterms))

                new_remaining_chart = {}
                for pi, minterms in remaining_chart.items():
                    remaining_minterms = [m for m in minterms if m not in covered_minterms]
                    if remaining_minterms:
                        new_remaining_chart[pi] = remaining_minterms
                remaining_chart = new_remaining_chart

            return essential_pis

        def minimize_function(minterms, dont_cares, num_vars):
            all_terms = minterms + dont_cares
            prime_implicants = find_prime_implicants(all_terms, num_vars)
            chart = build_chart(minterms, prime_implicants)

            essential_pis, _ = extract_essential_prime_implicants(chart)
            final_pis = iterative_reduction(chart, essential_pis)

            return final_pis
        

        def sop_expression(prime_implicants):
            # variables = ['A', 'B', 'C', 'D']  
            terms = []

            for pi in sorted(prime_implicants):
                term = ''
                for idx, bit in enumerate(pi):
                    if bit == '0':
                        term += f"{variables[idx]}'"
                    elif bit == '1':
                        term += f"{variables[idx]}"
                terms.append(term)

            return ' + '.join(sorted(terms))
        

        final_prime_implicants = minimize_function(minterms, dont_cares, len(variables))
        final_expression = sop_expression(final_prime_implicants)

        print("Minimized Boolean Function: F = ", final_expression)
        self.answer.set(f"F = {final_expression}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Quine_McCluskey(root)
    root.mainloop()
