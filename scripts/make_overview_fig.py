# -*- coding: utf-8 -*-
"""Generate JevSpec overview figure (vector PDF + high-res PNG)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12.5, 4.6), dpi=200)
ax.set_xlim(0, 125); ax.set_ylim(0, 46)
ax.axis("off")

C_IN = "#E8F0FE"; C_LLM = "#FFF3E0"; C_IG = "#E8F5E9"; C_LOOP = "#F3E5F5"; C_OUT = "#FCE4EC"; C_EVAL = "#ECEFF1"

def box(x, y, w, h, text, color, fs=10.5):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.45", fc=color, ec="#37474F", lw=1.4)
    ax.add_patch(p)
    if text:
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color="#212121",
                fontfamily="sans-serif", weight="bold")
    return (x + w, y + h/2)

def arrow(p1, p2, label=None, color="#546E7A"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=18, lw=1.6, color=color))
    if label:
        mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2 + 1.5
        ax.text(mx, my, label, ha="center", va="bottom", fontsize=8.8, color="#37474F", style="italic")

# Row 1: data + goal -> featuretable -> IG ranking
bx1 = box(3, 36, 16, 7, "Tabular\nData $\\mathcal{D}$", C_IN)
bx2 = box(24, 36, 15, 7, "NL Goal $g$", C_IN)
ax.text(20.5, 39.5, "+", ha="center", va="center", fontsize=15, color="#37474F")
arrow(bx1, (24, 39.5)); arrow((39, 39.5), (45, 39.5))
bx3 = box(45, 36, 17, 7, "LLM Schema Pass\n(auditable semantics)", C_LLM)
arrow(bx3, (62, 39.5), "normalize")
bx4 = box(62, 36, 15, 7, "FeatureTable\n$\\widehat{\\mathcal{D}}$", C_IG)
arrow(bx4, (77, 39.5), "quantize")
box(77, 36, 17, 7, "IG Ranking $\\mathcal{R}$\n(n_bins quantiles)", C_IG)

# Row 2: acquisition episode
ax.text(2, 31.4, "Hard-budget episode (per test instance)", fontsize=9.6, color="#37474F", style="italic")
pol = box(2, 17, 22, 12, "", C_OUT)
ax.text(13, 26.3, "policies", ha="center", fontsize=9.6, weight="bold", color="#B71C1C")
for i, t in enumerate(["ig_static", "ig_conditional", "ig_discriminative", "random / sequential"]):
    ax.text(13, 23.4 - i*1.9, t, ha="center", fontsize=9.0, color="#212121", family="monospace")
box(30, 17, 46, 12, "", C_LOOP)
ax.text(53, 26.5, "acquisition loop  ($t=1..B$)", ha="center", fontsize=9.8, weight="bold", color="#4A148C")
ax.text(36, 22.6, "$a_t = \\pi(\\mathbf{x}_{\\mathrm{mask}}, \\mathrm{mask})$", ha="center", fontsize=10.2)
ax.text(53, 22.6, "$\\rightarrow$ observe $x_{a_t}$", ha="center", fontsize=10.2)
ax.text(70, 22.6, "$\\rightarrow$ stop at $B$", ha="center", fontsize=10.2)
ax.text(53, 19.0, "$\\hat{y} = f(\\mathbf{x}_{\\mathrm{obs}})$  (shared predictor)", ha="center", fontsize=10.0, color="#B71C1C")
arrow((24, 23), (30, 23))

# Artifacts column (x 83..125)
ax.text(83, 34.2, "Auditable artifacts (export once)", fontsize=9.6, color="#37474F", style="italic")
box(83, 25.5, 20, 7, "tree.json", C_OUT)
box(106, 25.5, 19, 7, "story.md", C_OUT)
box(83, 16.5, 20, 7, "spec\n(typed decision spec)", C_OUT, fs=9.6)
box(106, 16.5, 19, 7, "receipts\n(per-instance)", C_OUT, fs=9.6)
box(83, 8.0, 42, 6.5, "spec questions typed as Jev  Choice / Noul / Score", "#E0F2F1", fs=9.2)
arrow((77, 23), (83, 22), "ID3 grow", color="#37474F")

# bottom: evaluation protocol
box(30, 1.5, 46, 9.5, "", C_EVAL)
ax.text(53, 8.0, "Hard-budget protocol  (shared predictor, multi-split)", ha="center",
        fontsize=10.0, color="#212121", weight="bold")
ax.text(53, 4.2, "metrics:  Acc / macro-F1  vs  budget  $B$", ha="center",
        fontsize=9.8, color="#1A237E", weight="bold")
arrow((53, 17), (53, 11))

plt.tight_layout()
plt.savefig("E:/课题/论文集/jevtree/jevtree-paper/figures/overview.pdf", bbox_inches="tight")
plt.savefig("E:/课题/论文集/jevtree/jevtree-paper/figures/overview.png", bbox_inches="tight", dpi=200)
print("figure saved")
