# -*- coding: utf-8 -*-
"""Generate experimental figures for the GainSOP manuscript (vector PDF + PNG).

Fig 2: MiniBooNE accuracy vs budget, 5 policies, mean +/- 1 std band.
Fig 3: Cross-dataset low-budget grouped bar chart with error bars.
Data source: plot_data.json (aggregated from gen_results.json, same source as tables).
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DATA = r"E:\课题\论文集\jevtree\plot_data.json"
OUTDIR = r"E:\课题\论文集\jevtree\jevtree-paper\figures"

with open(DATA, encoding="utf-8") as f:
    D = json.load(f)

POLICIES = ["ig_static", "ig_conditional", "ig_discriminative", "random", "sequential"]
P_LABEL = {
    "ig_static": "IG-static (ours)",
    "ig_conditional": "IG-conditional (ours)",
    "ig_discriminative": "IG-discriminative",
    "random": "Random",
    "sequential": "Sequential",
}
# Okabe-Ito colorblind-safe palette
COLOR = {
    "ig_static": "#0072B2",
    "ig_conditional": "#E69F00",
    "ig_discriminative": "#D55E00",
    "random": "#777777",
    "sequential": "#009E73",
}
LINESTYLE = {
    "ig_static": "-",
    "ig_conditional": "-",
    "ig_discriminative": "-",
    "random": "--",
    "sequential": ":",
}
MARKER = {
    "ig_static": "o",
    "ig_conditional": "s",
    "ig_discriminative": "^",
    "random": "v",
    "sequential": "D",
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9.5,
    "legend.fontsize": 8,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "axes.linewidth": 0.9,
    "figure.dpi": 100,
})

# ---------------------------------------------------------------- Fig 2 ----
def fig2_miniboone():
    mb = D["miniboone"]
    budgets = [int(b) for b in mb["ig_static"]]
    fig, ax = plt.subplots(figsize=(5.4, 3.5))
    for pol in POLICIES:
        row = mb[pol]
        xs = [int(b) for b in row]
        ys = [row[str(b)]["acc_mean"] for b in xs]
        sd = [row[str(b)]["acc_std"] for b in xs]
        ax.plot(xs, ys, color=COLOR[pol], ls=LINESTYLE[pol], lw=1.9,
                marker=MARKER[pol], ms=5, mec="white", mew=0.6,
                label=P_LABEL[pol], zorder=3)
        ax.fill_between(xs, np.array(ys) - np.array(sd), np.array(ys) + np.array(sd),
                        color=COLOR[pol], alpha=0.15, lw=0, zorder=2)
    # highlight the low-budget gap between IG-static and random
    s5 = mb["ig_static"]["5"]["acc_mean"]; r5 = mb["random"]["5"]["acc_mean"]
    ax.annotate("", xy=(5.4, s5), xytext=(5.4, r5),
                arrowprops=dict(arrowstyle="<->", color="#333333", lw=1.0))
    ax.text(6.2, (s5 + r5) / 2, "+%.1f pts at B=5" % ((s5 - r5) * 100),
            fontsize=8, color="#333333", va="center")
    ax.set_xlabel("Budget $B$ (features acquired)")
    ax.set_ylabel("Accuracy")
    ax.set_xticks(budgets)
    ax.set_ylim(0.65, 0.95)
    ax.set_xlim(2, 43)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", ls=":", lw=0.6, alpha=0.45)
    ax.legend(loc="lower right", frameon=False, ncol=1, handlelength=1.8)
    fig.tight_layout()
    fig.savefig(f"{OUTDIR}/fig2_miniboone_curves.pdf", bbox_inches="tight")
    fig.savefig(f"{OUTDIR}/fig2_miniboone_curves.png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    print("fig2 saved")

# ---------------------------------------------------------------- Fig 3 ----
def fig3_lowbudget():
    mb, db, cb = D["miniboone"], D["diabetes"], D["cube_without_noise"]
    groups = [
        ("MiniBooNE", "miniboone", "5"),
        ("Diabetes", "diabetes", "5"),
        ("Cube-5", "cube_without_noise", "3"),
    ]
    fig, ax = plt.subplots(figsize=(5.4, 3.5))
    n_pol = len(POLICIES)
    width = 0.15
    for gi, (gname, ds, budget) in enumerate(groups):
        row = D[ds]
        base = gi * (n_pol + 0.7) + 0.5
        for pi, pol in enumerate(POLICIES):
            if pol not in row or budget not in row[pol]:
                continue
            v = row[pol][budget]
            mean, sd = v["acc_mean"], v["acc_std"]
            x = base + pi * width
            ax.bar(x, mean, width, color=COLOR[pol], edgecolor="white", lw=0.4,
                   alpha=0.92, label=P_LABEL[pol] if gi == 0 else None)
            ax.errorbar(x, mean, yerr=sd, fmt="none", ecolor="#333333",
                        elinewidth=0.8, capsize=2.2)
    # dataset separators + labels
    xticks = []
    for gi, (gname, ds, budget) in enumerate(groups):
        base = gi * (n_pol + 0.7) + 0.5
        xticks.append(base + (n_pol - 1) * width / 2)
    ax.set_xticks(xticks)
    ax.set_xticklabels(["MiniBooNE\n(B=5)", "Diabetes\n(B=5)", "Cube-5\n(B=3)"])
    ax.set_xlim(0.15, groups[-1][0] and len(groups) * (n_pol + 0.7))
    ax.set_ylabel("Accuracy at smallest budget")
    ax.set_ylim(0.55, 1.05)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", ls=":", lw=0.6, alpha=0.45)
    ax.legend(loc="upper left", frameon=False, ncol=1, handlelength=1.2, fontsize=7.6)
    fig.tight_layout()
    fig.savefig(f"{OUTDIR}/fig3_lowbudget_bars.pdf", bbox_inches="tight")
    fig.savefig(f"{OUTDIR}/fig3_lowbudget_bars.png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    print("fig3 saved")

fig2_miniboone()
fig3_lowbudget()
