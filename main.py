import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import bisect
from collections import deque
from array import array
import threading
import queue


# ------------------- SORT ALGORITHM -------------------
def bureaucratic_sort_optimized(
    arr,
    pity_range=(5, 10),
    batch_size=1000,
    seed=42,
    progress_queue=None
):
    if seed is not None:
        random.seed(seed)

    start_time = time.time()
    last_report = start_time
    REPORT_INTERVAL = 1.0

    working = array('i')
    purged_values = deque()

    for x in arr:
        if not working or x >= working[-1]:
            working.append(x)
        else:
            purged_values.append(x)

        now = time.time()
        if progress_queue and now - last_report >= REPORT_INTERVAL:
            progress_queue.put(("progress", len(working), len(purged_values)))
            last_report = now

    while purged_values:
        for _ in range(min(batch_size, len(purged_values))):
            v = purged_values.popleft()
            bisect.insort_right(working, v)

        now = time.time()
        if progress_queue and now - last_report >= REPORT_INTERVAL:
            progress_queue.put(("progress", len(working), len(purged_values)))
            last_report = now

    elapsed = time.time() - start_time
    return list(working), elapsed


# ------------------- TKINTER UI -------------------
class BureaucraticSortUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bureaucratic Sort")
        self.geometry("800x600")

        self.progress_queue = queue.Queue()
        self.create_widgets()
        self.last_status = ""
        
        self.poll_queue()

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

        ttk.Button(frame, text="Run Sort", command=self.start_sort_thread).grid(row=5, column=0, pady=10, sticky="w")
        ttk.Button(frame, text="Clear Output", command=self.clear_output).grid(row=5, column=1, pady=10, sticky="w")

        self.output = tk.Text(self, wrap="word", height=20)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------------- THREADING ----------------
    def start_sort_thread(self):
        try:
            size = self.size_var.get()
            min_val = self.min_var.get()
            max_val = self.max_var.get()

            if size <= 0:
                raise ValueError("Array size must be positive.")

            self.output.insert(tk.END, "Starting Bureaucratic Sort...\n\n")
            self.output.see(tk.END)

            data = [random.randint(min_val, max_val) for _ in range(size)]

            thread = threading.Thread(
                target=self.run_sort,
                args=(data,),
                daemon=True
            )
            thread.start()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_sort(self, data):
        sorted_data, elapsed = bureaucratic_sort_optimized(
            data,
            pity_range=(self.pity_min_var.get(), self.pity_max_var.get()),
            progress_queue=self.progress_queue
        )
        self.progress_queue.put(("done", sorted_data, elapsed))

    # ---------------- QUEUE POLLING ----------------
    def poll_queue(self):
        try:
            while True:
                msg = self.progress_queue.get_nowait()

                if msg[0] == "progress":
                    _, working_count, purged_count = msg
                    self.last_status = f"Working count: {working_count} | Purged count: {purged_count}"

                elif msg[0] == "done":
                    _, sorted_data, elapsed = msg
                    self.output.insert(tk.END, "\nSort complete.\n")
                    self.output.insert(tk.END, f"Sorted sample (first 50):\n{sorted_data[:50]}\n")
                    self.output.insert(tk.END, f"Time taken: {elapsed:.4f}s\n\n")
                    self.output.see(tk.END)
                    self.last_status = ""

        except queue.Empty:
            pass

        if self.last_status:
            self.output.insert(tk.END, self.last_status + "\n")
            self.output.see(tk.END)
            self.last_status = ""

        self.after(200, self.poll_queue)  # check the queue every 0.2s

    def clear_output(self):
        self.output.delete("1.0", tk.END)


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app = BureaucraticSortUI()
    app.mainloop()
