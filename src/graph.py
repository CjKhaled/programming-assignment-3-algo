"""
Runs HVLCS on each input file and makes the graph + updates outputs
"""
import time
import os
import sys
import matplotlib.pyplot as plt
from hvlcs import read_input, hvlcs

DATA_DIR = "data/input"
RESULTS_DIR = "data/output"
os.makedirs(RESULTS_DIR, exist_ok=True)

def get_file_number(filename):
    return int(filename.replace("input", "").replace(".txt", ""))

files = []
for f in os.listdir(DATA_DIR):
    if f.endswith(".txt"):
        files.append(f)
files.sort(key=get_file_number)

labels = []
runtimes = []

# run hvlcs on each input file and record the runtime
for fname in files:
    path = os.path.join(DATA_DIR, fname)
    with open(path) as f:
        text = f.read()

    values, a, b = read_input(text)

    reps = 3
    start = time.perf_counter()
    for i in range(reps):
        val, seq = hvlcs(values, a, b)
    elapsed = (time.perf_counter() - start) / reps * 1000

    labels.append(f"{len(a)}x{len(b)}")
    runtimes.append(elapsed)

    print(f"{fname}  {len(a)}x{len(b)}  {elapsed:.3f}ms  val={val}")

    out_path = os.path.join(RESULTS_DIR, fname.replace("input", "output"))
    with open(out_path, "w") as f:
        f.write(f"{val}\n{seq}\n")

# make graph
plt.figure(figsize=(10, 5))
plt.plot(range(len(labels)), runtimes, marker="o", linewidth=2, color="#2563eb", markersize=7)
plt.xticks(range(len(labels)), labels, rotation=30, ha="right")
plt.xlabel("Input size (len(A) x len(B))")
plt.ylabel("Runtime (ms)")
plt.title("HVLCS Runtime vs Input Size")
plt.grid(True, alpha=0.3)
plt.ylim(bottom=0, top=max(runtimes) * 1.15)

for x, y in enumerate(runtimes):
    if x == len(runtimes) - 1:
        xa = -20
    elif x == len(runtimes) - 2:
        xa = -15
    else:
        xa = 0
    plt.annotate(f"{y:.1f}ms", (x, y), textcoords="offset points", xytext=(xa, 8), ha="center", fontsize=8)

plt.tight_layout()
os.makedirs("results", exist_ok=True)
plt.savefig("results/runtime_graph.png", dpi=150)
print("saved to results/runtime_graph.png")