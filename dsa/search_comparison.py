import json
import time
import random
import os

# ---------------------------
# Step 1: Load or Create Transactions
# ---------------------------
dataset_path = "../api/transactions.json"

if not os.path.exists(dataset_path):
    print("Warning: transactions.json not found. Creating a dummy dataset...")

    dummy_data = [
        {"id": f"T{i:03}", "amount": random.randint(50, 1000), "status": random.choice(["SUCCESS", "FAILED", "PENDING"])}
        for i in range(1, 101)  # generate 100 transactions
    ]

    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
    with open(dataset_path, "w") as f:
        json.dump(dummy_data, f, indent=4)

with open(dataset_path) as f:
    transactions_list = json.load(f)

# ---------------------------
# Step 2: Linear Search
# ---------------------------
def linear_search(transactions, target_id):
    for txn in transactions:
        if txn['id'] == target_id:
            return txn
    return None

# ---------------------------
# Step 3: Dictionary Lookup
# ---------------------------
transactions_dict = {txn['id']: txn for txn in transactions_list}

def dict_lookup(transactions_dict, target_id):
    return transactions_dict.get(target_id, None)

# ---------------------------
# Step 4: Test Individual Searches
# ---------------------------
if transactions_list:
    sample_id = transactions_list[0]['id']  # first transaction for testing

    start = time.time()
    result_linear = linear_search(transactions_list, sample_id)
    end = time.time()
    print("Linear Search Result:", result_linear)
    print("Time taken (linear):", round(end - start, 6), "seconds")

    start = time.time()
    result_dict = dict_lookup(transactions_dict, sample_id)
    end = time.time()
    print("Dict Lookup Result:", result_dict)
    print("Time taken (dict):", round(end - start, 6), "seconds")

# ---------------------------
# Step 5: Compare Performance on 20 Random IDs
# ---------------------------
if transactions_list and len(transactions_list) >= 20:
    sample_ids = random.sample([txn['id'] for txn in transactions_list], 20)

    linear_times = []
    dict_times = []

    for tid in sample_ids:
        start = time.time()
        linear_search(transactions_list, tid)
        linear_times.append(time.time() - start)

        start = time.time()
        dict_lookup(transactions_dict, tid)
        dict_times.append(time.time() - start)

    print("\n=== Performance Comparison ===")
    print("Average Linear Search Time:", round(sum(linear_times)/len(linear_times), 6), "seconds")
    print("Average Dict Lookup Time:", round(sum(dict_times)/len(dict_times), 6), "seconds")

# ---------------------------
# Step 6: Reflection
# ---------------------------
"""
Reflection:
- Linear search has time complexity O(n).
- Dictionary lookup has average time complexity O(1).
- Dict lookup is much faster as dataset grows.
"""

