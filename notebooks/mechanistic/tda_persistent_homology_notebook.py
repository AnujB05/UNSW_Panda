# %% [markdown]
# # TDA Persistent Homology — Panda Generalisation Study
#
# **Run this locally with your actual Weather / ETTh1 / ETTh2 CSVs.**
# Replace the file paths in Cell 2 with your local paths.
#
# Methodology: per-channel delay embedding (Takens) -> Vietoris-Rips (ripser) -> H1 persistence
# tau: first minimum of mutual information (per channel)
# d: 3 (fixed, documented limitation — false nearest neighbours would be more rigorous)
# Primary statistic: max H1 persistence (longest-lived loop)
# Secondary statistic: total H1 persistence (sum of all loop lifetimes)
#
# CRITICAL: max_pers and total_pers can tell opposite stories (few-long vs many-short loops).
# Report both, do not collapse to one number without checking the other.

# %%
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
np.random.seed(42)

# pip install ripser   (if not already installed)
from ripser import ripser

# %% [markdown]
# ## Cell 2 — Load your real data
#
# Replace these paths with your local files.

# %%
WEATHER_PATH = "weather.csv"      # <-- your local Weather CSV
ETTH1_PATH   = "ETTh1.csv"
ETTH2_PATH   = "ETTh2.csv"

weather_df = pd.read_csv(WEATHER_PATH)
etth1_df   = pd.read_csv(ETTH1_PATH)
etth2_df   = pd.read_csv(ETTH2_PATH)

# Drop date/time columns — adjust column name if different in your files
date_cols = ['date']
weather_cols = [c for c in weather_df.columns if c not in date_cols]
etth1_cols   = [c for c in etth1_df.columns if c not in date_cols]
etth2_cols   = [c for c in etth2_df.columns if c not in date_cols]

N_POINTS_TIMESERIES = 3000  # length of series to use per channel before embedding

weather_data = weather_df[weather_cols].values[:N_POINTS_TIMESERIES].astype(float)
etth1_data   = etth1_df[etth1_cols].values[:N_POINTS_TIMESERIES].astype(float)
etth2_data   = etth2_df[etth2_cols].values[:N_POINTS_TIMESERIES].astype(float)

print(f"Weather: {weather_data.shape}")
print(f"ETTh1:   {etth1_data.shape}")
print(f"ETTh2:   {etth2_data.shape}")

# %% [markdown]
# ## Cell 3 — Lorenz simulation (training-distribution reference, exact)

# %%
def simulate_lorenz(n=5000, dt=0.01, sigma=10, rho=28, beta=8/3):
    """RK4 integration of the Lorenz system."""
    x, y, z = 0.1, 0.0, 0.0
    xs, ys, zs = [x], [y], [z]
    for _ in range(n - 1):
        k1x = sigma * (y - x)
        k1y = x * (rho - z) - y
        k1z = x * y - beta * z
        k2x = sigma * ((y + dt/2*k1y) - (x + dt/2*k1x))
        k2y = (x + dt/2*k1x) * (rho - (z + dt/2*k1z)) - (y + dt/2*k1y)
        k2z = (x + dt/2*k1x) * (y + dt/2*k1y) - beta * (z + dt/2*k1z)
        k3x = sigma * ((y + dt/2*k2y) - (x + dt/2*k2x))
        k3y = (x + dt/2*k2x) * (rho - (z + dt/2*k2z)) - (y + dt/2*k2y)
        k3z = (x + dt/2*k2x) * (y + dt/2*k2y) - beta * (z + dt/2*k2z)
        k4x = sigma * ((y + dt*k3y) - (x + dt*k3x))
        k4y = (x + dt*k3x) * (rho - (z + dt*k3z)) - (y + dt*k3y)
        k4z = (x + dt*k3x) * (y + dt*k3y) - beta * (z + dt*k3z)
        x += dt/6*(k1x+2*k2x+2*k3x+k4x)
        y += dt/6*(k1y+2*k2y+2*k3y+k4y)
        z += dt/6*(k1z+2*k2z+2*k3z+k4z)
        xs.append(x); ys.append(y); zs.append(z)
    return np.array([xs, ys, zs]).T

lorenz_data = simulate_lorenz(n=5000)[500:3500]  # discard transient
print(f"Lorenz: {lorenz_data.shape}")

# %% [markdown]
# ## Cell 4 — Core TDA functions

# %%
def mutual_information_tau(x, max_lag=100, n_bins=16):
    """
    Estimate optimal delay tau as the first local minimum of mutual information.
    MI captures nonlinear dependence; autocorrelation only captures linear
    structure, which is insufficient for chaotic/nonlinear signals.
    """
    mis = []
    for lag in range(1, max_lag + 1):
        x1, x2 = x[:-lag], x[lag:]
        hist2d, _, _ = np.histogram2d(x1, x2, bins=n_bins)
        hist2d = hist2d / hist2d.sum()
        px = hist2d.sum(axis=1, keepdims=True)
        py = hist2d.sum(axis=0, keepdims=True)
        outer = px @ py
        mask = (hist2d > 0) & (outer > 0)
        mi = np.sum(hist2d[mask] * np.log(hist2d[mask] / outer[mask]))
        mis.append(mi)
    mis = np.array(mis)
    for i in range(1, len(mis) - 1):
        if mis[i] < mis[i-1] and mis[i] < mis[i+1]:
            return i + 1
    return 1  # fallback if no local minimum found in range

def delay_embed(x, d, tau):
    """Takens delay embedding: x(t), x(t+tau), ..., x(t+(d-1)*tau)."""
    N = len(x) - (d - 1) * tau
    if N <= 0:
        raise ValueError(f"Signal too short for d={d}, tau={tau}: len={len(x)}")
    return np.stack([x[i*tau : i*tau + N] for i in range(d)], axis=1)

def subsample_cloud(cloud, n=800, seed=42):
    """Random subsample to bound O(n^2) Vietoris-Rips memory cost."""
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(cloud), size=min(n, len(cloud)), replace=False)
    return cloud[idx]

def compute_h1_persistence(cloud):
    """Run ripser, return finite H1 (birth, death) pairs."""
    result = ripser(cloud, maxdim=1)
    h1 = result['dgms'][1]
    h1 = h1[np.isfinite(h1[:, 1])] if len(h1) > 0 else h1
    return h1

def persistence_stats(h1_pairs):
    """Summary statistics from an H1 persistence diagram."""
    if len(h1_pairs) == 0:
        return {'max_pers': 0.0, 'total_pers': 0.0, 'n_features': 0}
    pers = h1_pairs[:, 1] - h1_pairs[:, 0]
    return {'max_pers': float(pers.max()), 'total_pers': float(pers.sum()), 'n_features': len(pers)}

def analyse_channel(x, d=3, max_tau=100, n_points=800, label=""):
    """Full pipeline: normalise -> find tau -> embed -> subsample -> ripser -> stats."""
    x = (x - x.mean()) / (x.std() + 1e-8)
    tau = mutual_information_tau(x, max_lag=max_tau)
    cloud = delay_embed(x, d=d, tau=tau)
    cloud = subsample_cloud(cloud, n=n_points)
    h1 = compute_h1_persistence(cloud)
    stats = persistence_stats(h1)
    stats['tau'] = tau
    stats['label'] = label
    return stats

# %% [markdown]
# ## Cell 5 — Run the pipeline on all datasets

# %%
datasets = {
    'Lorenz':  lorenz_data,
    'ETTh1':   etth1_data,
    'ETTh2':   etth2_data,
    'Weather': weather_data,
}

all_results = []

for dname, data in datasets.items():
    n_ch = data.shape[1]
    print(f"\n{dname} ({n_ch} channels):")
    ch_stats = []
    for ch in range(n_ch):
        x = data[:, ch].astype(float)
        stats = analyse_channel(x, d=3, max_tau=80, n_points=800, label=f"{dname}_ch{ch}")
        ch_stats.append(stats)
        print(f"  ch{ch}: tau={stats['tau']:2d}, max_pers={stats['max_pers']:.4f}, "
              f"total_pers={stats['total_pers']:.4f}, n_H1={stats['n_features']}")

    max_pers_vals = [s['max_pers'] for s in ch_stats]
    total_pers_vals = [s['total_pers'] for s in ch_stats]
    tau_vals = [s['tau'] for s in ch_stats]

    summary = {
        'dataset': dname,
        'n_channels': n_ch,
        'max_pers_median': np.median(max_pers_vals),
        'max_pers_iqr': np.percentile(max_pers_vals, 75) - np.percentile(max_pers_vals, 25),
        'total_pers_median': np.median(total_pers_vals),
        'total_pers_iqr': np.percentile(total_pers_vals, 75) - np.percentile(total_pers_vals, 25),
        'tau_median': np.median(tau_vals),
        'channel_stats': ch_stats,
        'max_pers_vals': max_pers_vals,
        'total_pers_vals': total_pers_vals,
    }
    all_results.append(summary)
    print(f"  -> max_pers: median={summary['max_pers_median']:.4f}, IQR={summary['max_pers_iqr']:.4f}")
    print(f"  -> total_pers: median={summary['total_pers_median']:.4f}")

# %% [markdown]
# ## Cell 6 — Save results

# %%
rows = []
for s in all_results:
    for ch_s in s['channel_stats']:
        rows.append({
            'dataset': s['dataset'],
            'channel': ch_s['label'],
            'tau': ch_s['tau'],
            'max_pers': ch_s['max_pers'],
            'total_pers': ch_s['total_pers'],
            'n_H1_features': ch_s['n_features'],
        })
df_results = pd.DataFrame(rows)
df_results.to_csv('tda_results_real.csv', index=False)

summary_rows = []
for s in all_results:
    summary_rows.append({
        'dataset': s['dataset'],
        'n_channels': s['n_channels'],
        'max_pers_median': round(s['max_pers_median'], 4),
        'max_pers_iqr': round(s['max_pers_iqr'], 4),
        'total_pers_median': round(s['total_pers_median'], 4),
        'total_pers_iqr': round(s['total_pers_iqr'], 4),
        'tau_median': round(s['tau_median'], 1),
    })
df_summary = pd.DataFrame(summary_rows)
df_summary.to_csv('tda_summary_real.csv', index=False)
print(df_summary.to_string(index=False))

# %% [markdown]
# ## Cell 7 — Visualisation

# %%
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle('TDA Persistent Homology Analysis\n(H1 = loops in delay-embedded attractor, d=3, tau=MI-first-minimum)',
             fontsize=12, fontweight='bold')

colors = {'Lorenz': '#e74c3c', 'ETTh1': '#3498db', 'ETTh2': '#2980b9', 'Weather': '#27ae60'}
datasets_order = ['Lorenz', 'ETTh1', 'ETTh2', 'Weather']

# Panel A: max persistence boxplot
ax = axes[0]
box_data = [next(r for r in all_results if r['dataset'] == d)['max_pers_vals'] for d in datasets_order]
bp = ax.boxplot(box_data, patch_artist=True, widths=0.5)
for patch, dname in zip(bp['boxes'], datasets_order):
    patch.set_facecolor(colors[dname]); patch.set_alpha(0.7)
ax.set_xticks(range(1, 5)); ax.set_xticklabels(datasets_order, fontsize=9)
ax.set_ylabel('Max H1 Persistence')
ax.set_title('(A) Dominant Topological Feature')
ax.grid(axis='y', alpha=0.3)

# Panel B: total persistence boxplot
ax = axes[1]
total_data = [next(r for r in all_results if r['dataset'] == d)['total_pers_vals'] for d in datasets_order]
bp2 = ax.boxplot(total_data, patch_artist=True, widths=0.5)
for patch, dname in zip(bp2['boxes'], datasets_order):
    patch.set_facecolor(colors[dname]); patch.set_alpha(0.7)
ax.set_xticks(range(1, 5)); ax.set_xticklabels(datasets_order, fontsize=9)
ax.set_ylabel('Total H1 Persistence')
ax.set_title('(B) Aggregate Loop Structure')
ax.grid(axis='y', alpha=0.3)

# Panel C: scatter, max vs total, per channel
ax = axes[2]
for s in all_results:
    dname = s['dataset']
    for ch_s in s['channel_stats']:
        ax.scatter(ch_s['max_pers'], ch_s['total_pers'], color=colors[dname], alpha=0.6, s=40)
handles = [mpatches.Patch(color=colors[d], label=d, alpha=0.7) for d in datasets_order]
ax.legend(handles=handles, fontsize=8, loc='upper right')
ax.set_xlabel('Max H1 Persistence (per channel)')
ax.set_ylabel('Total H1 Persistence (per channel)')
ax.set_title('(C) Max vs Total Persistence')
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('tda_homology_results_real.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved tda_homology_results_real.png")

# %% [markdown]
# ## Cell 8 — Interpretation checklist (fill in after running)
#
# Before drawing any conclusion, check:
#
# 1. Does Weather's max_pers median sit closer to Lorenz or to ETTh1/ETTh2?
#    - Closer to Lorenz -> consistent with topology hypothesis (correlation only, not causal)
#    - Closer to ETTh -> hypothesis not supported on this statistic
#    - In between with high IQR -> inconclusive, heterogeneous channel structure
#
# 2. Does total_pers tell the same story as max_pers, or the opposite?
#    - If opposite (as in the synthetic pilot), report both and do not collapse to one number.
#
# 3. Remember: even a clean separation is correlational, not mechanistic.
#    It does not establish that Panda generalises BECAUSE of shared topology.
#    Confounds to consider: amplitude range, stationarity, periodicity strength,
#    channel count, noise level — any of these could independently track both
#    topology and Panda's performance gap.
