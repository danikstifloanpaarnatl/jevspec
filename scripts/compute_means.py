# -*- coding: utf-8 -*-
"""Print ablation results (ab_*) from gen_results"""
import json, os, re

with open(r"E:\课题\论文集\jevtree\exp_results\gen_results.json", encoding="utf-8") as f:
    data = json.load(f)

def fmt_curve(d):
    return "; ".join("b%d:%.3f/%.3f" % (p["budget"], p["accuracy"], p["f1"]) for p in d.get("curve", []))

for n in sorted(data):
    if n.startswith("ab_") or "cube_ig_discriminative_logistic" in n:
        d = data[n]
        print("%-45s %s" % (n, fmt_curve(d)))

# compute means for main tables
import statistics
print("\n=== MINIBOONE means (acc/f1) ===")
pols = ["ig_static", "ig_conditional", "ig_discriminative", "random", "sequential"]
for pol in pols:
    rows = [data[f"miniboone_{pol}_s{s}"] for s in range(4)]
    accs = {b: [] for b in [5,10,20,40]}; f1s = {b: [] for b in [5,10,20,40]}
    for r in rows:
        for p in r["curve"]:
            accs[p["budget"]].append(p["accuracy"]); f1s[p["budget"]].append(p["f1"])
    line = " ".join("b%d:%.3f(±%.3f)/%.3f" % (b, statistics.mean(accs[b]), statistics.stdev(accs[b]), statistics.mean(f1s[b])) for b in [5,10,20,40])
    print("%-16s %s" % (pol, line))

print("\n=== DIABETES means ===")
for pol in pols:
    rows = [data[f"diabetes_{pol}_s{s}"] for s in range(3)]
    accs = {b: [] for b in [5,10,20]}; f1s = {b: [] for b in [5,10,20]}
    for r in rows:
        for p in r["curve"]:
            accs[p["budget"]].append(p["accuracy"]); f1s[p["budget"]].append(p["f1"])
    line = " ".join("b%d:%.3f/%.3f" % (b, statistics.mean(accs[b]), statistics.mean(f1s[b])) for b in [5,10,20])
    print("%-16s %s" % (pol, line))

print("\n=== CUBE means ===")
for pol in pols:
    rows = [data[f"cube_{pol}_s{s}"] for s in range(3)]
    accs = {b: [] for b in [1,2,3]}
    for r in rows:
        for p in r["curve"]:
            accs[p["budget"]].append(p["accuracy"])
    line = " ".join("b%d:%.3f" % (b, statistics.mean(accs[b])) for b in [1,2,3])
    print("%-16s %s" % (pol, line))
