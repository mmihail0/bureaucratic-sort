import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import bisect
from collections import deque
from array import array


# ------------------- SORT ALGORITHM -------------------
def bureaucratic_sort_optimized(arr, pity_range=(5, 10), batch_size=1000, seed=42):
    if seed is not None:
        random.seed(seed)

    start_time = time.time()

    working = array('i')
    purged_values = deque()
    purged_attempts = deque()
    purged_pity = deque()

    for x in arr:
        if not working or x >= working[-1]:
            working.append(x)
        else:
            purged_values.append(x)
            purged_attempts.append(0)
            purged_pity.append(random.randint(*pity_range))

    while purged_values:
        for _ in range(min(batch_size, len(purged_values))):
            v = purged_values.popleft()
            bisect.insort_right(working, v)

    return list(working), time.time() - start_time


# ------------------- TKINTER UI -------------------
class BureaucraticSortUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bureaucratic Sort")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="x")

        self.size_var = tk.IntVar(value=1000)
        self.min_var = tk.IntVar(value=1)
        self.max_var = tk.IntVar(value=100)
        self.pity_min_var = tk.IntVar(value=5)
        self.pity_max_var = tk.IntVar(value=10)

        def add_row(label, var, row):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w")
            ttk.Entry(frame, textvariable=var, width=10).grid(row=row, column=1, sticky="w")

        add_row("Array size:", self.size_var, 0)
        add_row("Minimum value:", self.min_var, 1)
        add_row("Maximum value:", self.max_var, 2)
        add_row("Pity min:", self.pity_min_var, 3)
        add_row("Pity max:", self.pity_max_var, 4)

        ttk.Button(frame, text="Run Sort", command=self.run_sort).grid(row=5, column=0, pady=10, sticky="w")
        ttk.Button(frame, text="Clear Output", command=self.clear_output).grid(row=5, column=1, pady=10, sticky="w")

        self.output = tk.Text(self, wrap="word", height=20)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def run_sort(self):
        try:
            size = self.size_var.get()
            min_val = self.min_var.get()
            max_val = self.max_var.get()
            pity_min = self.pity_min_var.get()
            pity_max = self.pity_max_var.get()

            if size <= 0:
                raise ValueError("Array size must be positive.")
            if min_val > max_val:
                raise ValueError("Minimum value must be ≤ maximum value.")
            if pity_min > pity_max:
                raise ValueError("Pity min must be ≤ pity max.")

            data = [random.randint(min_val, max_val) for _ in range(size)]

            self.output.insert(tk.END, "Running Bureaucratic Sort...\n\n")
            self.output.see(tk.END)

            sorted_data, elapsed = bureaucratic_sort_optimized(
                data,
                pity_range=(pity_min, pity_max)
            )

            self.output.insert(tk.END, f"Original sample (first 50):\n{data[:50]}\n\n")
            self.output.insert(tk.END, f"Sorted sample (first 50):\n{sorted_data[:50]}\n\n")
            self.output.insert(tk.END, f"Time taken: {elapsed:.4f} seconds\n\n")
            self.output.see(tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_output(self):
        self.output.delete("1.0", tk.END)


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app = BureaucraticSortUI()
    app.mainloop()
