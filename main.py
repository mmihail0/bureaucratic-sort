import time
from collections import deque
import random

def chaotic_bureaucratic_sort(arr, pity_range=(5, 10), reshuffle_interval=50_000, verbose=True, seed=None):
    """
    Chaotic Bureaucratic Sort:
    - Stalin purge removes numbers out of order
    - Purged elements enter a queue with random pity thresholds
    - Each pass reintegrates one element in sorted order
    - Every reshuffle_interval passes, the queue is partially shuffled
    - Time-based progress printing
    """
    if seed is not None:
        random.seed(seed)
    start = time.time()

    # Phase 1: Stalin purge
    working = []
    purged_queue = deque()
    for x in arr:
        if not working or x >= working[-1]:
            working.append(x)
        else:
            purged_queue.append({
                "value": x,
                "attempts": 0,
                "pity": random.randint(*pity_range)
            })

    passes = 0

    # Phase 2: Bureaucratic reintegration
    while purged_queue:
        passes += 1
        item = purged_queue.popleft()
        v = item["value"]
        item["attempts"] += 1

        inserted = False
        # Insert in correct sorted position
        for i in range(len(working)+1):
            left_ok = (i == 0 or working[i-1] <= v)
            right_ok = (i == len(working) or v <= working[i])
            if left_ok and right_ok:
                working.insert(i, v)
                inserted = True
                break

        # Pity system: force insert in sorted order if attempts exceed pity threshold
        if not inserted and item["attempts"] >= item["pity"]:
            for i in range(len(working)+1):
                if i == len(working) or v <= working[i]:
                    working.insert(i, v)
                    inserted = True
                    break
        elif not inserted:
            purged_queue.append(item)  # retry later

        # Periodic reshuffle for chaos
        if passes % reshuffle_interval == 0 and len(purged_queue) > 1:
            temp_list = list(purged_queue)
            random.shuffle(temp_list)
            purged_queue = deque(temp_list)

        # Time-based progress printing
        if verbose and passes % 100_000 == 0:
            print(
                f"passes={passes} | working={len(working)} | "
                f"queued={len(purged_queue)} | time={time.time()-start:.2f}s"
            )

    total_time = time.time() - start
    if verbose:
        print(f"\nFinal sorted array: {working}")
        print(f"Total passes: {passes}")
        print(f"Total time: {total_time:.4f}s")

    return working


# ------------------- Main Program -------------------

if __name__ == "__main__":
    print("=== Chaotic Bureaucratic Sort ===\n")

    # User input
    while True:
        try:
            size = int(input("Enter the size of the array (e.g., 20): "))
            if size <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")

    while True:
        try:
            min_val = int(input("Enter minimum number (e.g., 0): "))
            max_val = int(input("Enter maximum number (e.g., 10): "))
            if min_val > max_val:
                raise ValueError
            break
        except ValueError:
            print("Please enter valid integers with min <= max.")

    while True:
        try:
            print("Pity threshold determines how many failed reintegration attempts an element can have before it is forcibly inserted into the array.")
            pity_min = int(input("Enter minimum pity threshold (e.g., 5): "))
            pity_max = int(input("Enter maximum pity threshold (e.g., 10): "))
            if pity_min > pity_max or pity_min <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter valid positive integers with min <= max.")

    # Generate random array
    data = [random.randint(min_val, max_val) for _ in range(size)]
    print("\nOriginal array:", data)

    # Run sort
    sorted_data = chaotic_bureaucratic_sort(
        data,
        pity_range=(pity_min, pity_max),
        reshuffle_interval=50_000,
        verbose=True,
        seed=42
    )
