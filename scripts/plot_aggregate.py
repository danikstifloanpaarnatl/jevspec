# -*- coding: utf-8 -*-
"""Aggregate per-config curves from experiment_results.json into plot-ready stats."""
import json, collections

SRC = r"E:\课题\论文集\jevtree\jevtree-paper\experiment_results.json"
OUT = r"E:\课题\论文集\jevtree\plot_data.json"

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

# group key: (dataset_id, policy_name) -> budget -> list of (acc, f1)
groups = collections.defaultdict(lambda: collections.defaultdict(list))

for cfg, entry in data.items():
    ds = entry["dataset_id"]
    pol = entry["policy_name"]
    # main-experiment rows only: skip ablation rows (ab_*) and the Cube logistic contrast
    if not (cfg.startswith("miniboone_") or cfg.startswith("diabetes_") or cfg.startswith("cube_")):
        continue
    if "logistic" in cfg:
        continue
    for pt in entry["curve"]:
        groups[(ds, pol)][pt["budget"]].append((pt["accuracy"], pt.get("f1", float("nan"))))

def stats(vals):
    n = len(vals)
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / max(n - 1, 1)
    return mean, (var ** 0.5 if n > 1 else 0.0), n

result = {}
for (ds, pol), by_budget in sorted(groups.items()):
    result.setdefault(ds, {})[pol] = {
        str(b): {"acc_mean": round(stats([v[0] for v in lst])[0], 4),
                 "acc_std": round(stats([v[0] for v in lst])[1], 4),
                 "f1_mean": round(stats([v[1] for v in lst])[0], 4),
                 "f1_std": round(stats([v[1] for v in lst])[1], 4),
                 "n_splits": len(lst)}
        for b, lst in sorted(by_budget.items())
    }

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("datasets:", list(result.keys()))
for ds in result:
    print(ds, "policies:", list(result[ds].keys()))
    for pol in result[ds]:
        print("  ", pol, {b: result[ds][pol][b]["acc_mean"] for b in result[ds][pol]})
