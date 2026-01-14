import time
import random
import bisect
from collections import deque
from array import array

def chaotic_bureaucratic_sort_optimized(arr, pity_range=(5,10), batch_size=1000, verbose=True, seed=42):
    """
    Optimized Chaotic Bureaucratic Sort for very large arrays.
    - Stalin purge removes numbers violating order
    - Purged numbers stored in deque for O(1) pop/append
    - Reintegration uses bisect.insort for log(n) insertion
    - Batch processing reduces overhead for massive arrays
    """
    if seed is not None:
        random.seed(seed)
    start_time = time.time()

    # Phase 1: Stalin purge
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

    passes = 0

    while purged_values:
        passes += 1

        # Batch processing: pop multiple purged values at once
        for _ in range(min(batch_size, len(purged_values))):
            v = purged_values.popleft()
            attempts = purged_attempts.popleft() + 1
            pity = purged_pity.popleft()

            # Binary search insertion
            bisect.insort_right(working, v)

        # Progress printing
        if verbose and passes % 100 == 0:
            print(f"passes={passes} | working={len(working)} | queued={len(purged_values)} | time={time.time()-start_time:.2f}s")

    total_time = time.time() - start_time
    if verbose:
        print(f"\nFinal sorted array sample (first 100 elements): {working[:100]} ...")
        print(f"Total passes: {passes}")
        print(f"Total time: {total_time:.4f}s")

    return working

# ------------------- Main Program -------------------
if __name__ == "__main__":
    print("=== Chaotic Bureaucratic Sort (Optimized for Large Arrays) ===\n")

    # User input
    size = int(input("Enter the size of the array (e.g., 1000000): "))
    min_val = int(input("Enter minimum number (e.g., 1): "))
    max_val = int(input("Enter maximum number (e.g., 100): "))
    print("Pity threshold determines how many failed reintegration attempts a number can have before it is forcibly inserted.")
    pity_min = int(input("Enter minimum pity threshold (e.g., 5): "))
    pity_max = int(input("Enter maximum pity threshold (e.g., 10): "))

    # Generate random array
    data = [random.randint(min_val, max_val) for _ in range(size)]
    print("\nOriginal array sample (first 100):", data[:100])

    # Run sort
    sorted_data = chaotic_bureaucratic_sort_optimized(
        data,
        pity_range=(pity_min, pity_max),
        batch_size=1000,
        verbose=True,
        seed=42
    )
