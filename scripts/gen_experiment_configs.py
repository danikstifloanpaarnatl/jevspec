# -*- coding: utf-8 -*-
"""Generate experiment configs for jevtree eval-afa and write to local dir."""
import json, os

OUT = r"E:\课题\论文集\jevtree\gen_configs"
os.makedirs(OUT, exist_ok=True)

def w(name, cfg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("WROTE", name)

POLICIES = {
    "ig_static":       {"name": "ig_static"},
    "ig_conditional":  {"name": "ig_conditional", "min_samples": 20, "max_candidates": 15},
    "ig_discriminative":{"name": "ig_discriminative", "min_samples": 20, "max_candidates": 15},
    "random":          {"name": "random"},
    "sequential":      {"name": "sequential"},
}

BASE_OUT = {"results_dir": "results/", "jsonl": True, "summary": True}
PROV = {"log_git_commit": True, "log_config_path": True}

# ---- A. MiniBooNE main: 5 policies x seeds 0..3, logistic_impute, budgets [5,10,20,40]
for pol, pcfg in POLICIES.items():
    for seed in range(4):
        cfg = {
            "dataset_id": "miniboone",
            "dataset_path": "data/cache/miniboone_uci_pid.txt",
            "split_seed": seed,
            "n_train": 2000,
            "n_test": 500,
            "hard_budgets": [5, 10, 20, 40],
            "budget_unit_cost": 1.0,
            "predictor": {"name": "logistic_impute", "path": None,
                          "note": "Shared MaskedLogisticPredictor across policies"},
            "output": BASE_OUT, "provenance": PROV,
            "policy": {**pcfg, "criterion": "gain", "n_bins": 4, "bin_seed": 0,
                       "seed": seed, "force_acquisition": True, "has_builtin_classifier": True},
        }
        w(f"miniboone_{pol}_s{seed}.json", cfg)

# ---- B. Diabetes main: 5 policies x seeds 0..2, logistic_impute, budgets [5,10,20]
for pol, pcfg in POLICIES.items():
    for seed in range(3):
        cfg = {
            "dataset_id": "diabetes",
            "dataset_path": "data/cache/diabetes_openml_37.csv",
            "split_seed": seed,
            "n_train": 500,
            "n_test": 200,
            "hard_budgets": [5, 10, 20],
            "budget_unit_cost": 1.0,
            "predictor": {"name": "logistic_impute", "path": None,
                          "note": "Shared MaskedLogisticPredictor across policies"},
            "output": BASE_OUT, "provenance": PROV,
            "policy": {**pcfg, "criterion": "gain", "n_bins": 4, "bin_seed": 0,
                       "seed": seed, "force_acquisition": True, "has_builtin_classifier": True},
        }
        w(f"diabetes_{pol}_s{seed}.json", cfg)

# ---- C. Cube main: 5 policies x seeds 0..2, match_majority (policy.predict), budgets [1,2,3]
for pol, pcfg in POLICIES.items():
    for seed in range(3):
        cfg = {
            "dataset_id": "cube_without_noise",
            "n_samples": 256, "n_features": 5,
            "split_seed": seed,
            "hard_budgets": [1, 2, 3],
            "budget_unit_cost": 1.0,
            "predictor": {"name": "policy.predict", "path": None},
            "output": BASE_OUT, "provenance": PROV,
            "policy": {**pcfg, "criterion": "gain", "n_bins": 4, "bin_seed": 0,
                       "seed": seed, "force_acquisition": True, "has_builtin_classifier": True},
        }
        w(f"cube_{pol}_s{seed}.json", cfg)

# ---- D. Ablations on MiniBooNE seed=0 (logistic_impute, budgets [5,10,20,40])
AB = [
    ("ab_miniboone_ig_static_gainratio.json", {"name": "ig_static", "criterion": "gain_ratio"}),
    ("ab_miniboone_ig_cond_gainratio.json", {"name": "ig_conditional", "criterion": "gain_ratio", "min_samples": 20, "max_candidates": 15}),
    ("ab_miniboone_ig_static_nbins2.json", {"name": "ig_static", "n_bins": 2}),
    ("ab_miniboone_ig_static_nbins8.json", {"name": "ig_static", "n_bins": 8}),
    ("ab_miniboone_ig_cond_c5.json", {"name": "ig_conditional", "max_candidates": 5, "min_samples": 20}),
    ("ab_miniboone_ig_cond_ms10.json", {"name": "ig_conditional", "min_samples": 10, "max_candidates": 15}),
    ("ab_miniboone_ig_cond_ms40.json", {"name": "ig_conditional", "min_samples": 40, "max_candidates": 15}),
    ("ab_miniboone_ig_disc_c5.json", {"name": "ig_discriminative", "max_candidates": 5, "min_samples": 20}),
    ("ab_miniboone_ig_disc_ms10.json", {"name": "ig_discriminative", "min_samples": 10, "max_candidates": 15}),
    ("ab_miniboone_ig_disc_nbins2.json", {"name": "ig_discriminative", "n_bins": 2, "min_samples": 20, "max_candidates": 15}),
]
for fname, pcfg in AB:
    cfg = {
        "dataset_id": "miniboone",
        "dataset_path": "data/cache/miniboone_uci_pid.txt",
        "split_seed": 0,
        "n_train": 2000, "n_test": 500,
        "hard_budgets": [5, 10, 20, 40],
        "budget_unit_cost": 1.0,
        "predictor": {"name": "logistic_impute", "path": None},
        "output": BASE_OUT, "provenance": PROV,
        "policy": {**pcfg, "criterion": pcfg.get("criterion", "gain"), "n_bins": pcfg.get("n_bins", 4),
                   "bin_seed": 0, "seed": 0, "force_acquisition": True, "has_builtin_classifier": True},
    }
    w(fname, cfg)

# ---- E. Cube discriminative + logistic (contrast row)
cfg = {
    "dataset_id": "cube_without_noise",
    "n_samples": 256, "n_features": 5,
    "split_seed": 0,
    "hard_budgets": [1, 2, 3],
    "budget_unit_cost": 1.0,
    "predictor": {"name": "logistic_impute", "path": None},
    "output": BASE_OUT, "provenance": PROV,
    "policy": {"name": "ig_discriminative", "criterion": "gain", "n_bins": 4, "bin_seed": 0,
               "seed": 0, "force_acquisition": True, "has_builtin_classifier": True,
               "min_samples": 20, "max_candidates": 15},
}
w("cube_ig_discriminative_logistic_s0.json", cfg)

print("TOTAL", len(os.listdir(OUT)))
