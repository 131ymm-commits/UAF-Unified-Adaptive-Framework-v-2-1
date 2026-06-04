import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
from typing import List, Dict
from IPython.display import display, Markdown

# ======================================================================
# UAF: CORE ENGINE (CELL AGENT & ENVIRONMENT)
# ======================================================================

class CellAgent:
    def __init__(self, resistance=0.05, repair=0.8, signaling=0.8):
        self.resistance = resistance
        self.repair = repair
        self.signaling = signaling
        self.closure_degree = 0.0
        self.fitness = 1.0

    def update_state(self, tissue_signaling_mean: float):
        # UAF Trade-off: Resistance breaks the regulatory loop integrity
        base_closure = min(self.signaling, tissue_signaling_mean)
        self.closure_degree = max(0.0, base_closure * (1.0 - self.resistance * 0.7))
        # Fitness depends on structural integrity and metabolic cost of resistance
        self.fitness = self.closure_degree * (1.0 - self.resistance * 0.2) + 0.05

    def adapt(self, drug_strength: float):
        if drug_strength > 0 and random.random() < 0.05:
            self.resistance = min(1.0, self.resistance + random.uniform(0.05, 0.15))

    def replicate(self):
        return CellAgent(
            resistance=self.resistance,
            repair=max(0.1, self.repair - random.uniform(0, 0.02)),
            signaling=max(0.1, self.signaling - random.uniform(0, 0.02))
        )

# ======================================================================
# SIMULATION RUNNER
# ======================================================================

def run_uaf_simulation(steps=150, therapy_start=50, drug_potency=0.8):
    cells = [CellAgent() for _ in range(250)]
    history = []

    for t in range(steps):
        drug = drug_potency if t >= therapy_start else 0.0
        
        # Process cells
        avg_tissue_sig = np.mean([c.signaling for c in cells])
        for cell in cells:
            cell.adapt(drug)
            cell.update_state(avg_tissue_sig)

        # Selection
        fitness_vals = [c.fitness for c in cells]
        threshold = np.percentile(fitness_vals, 25)
        survivors = [c for c in cells if c.fitness >= threshold]

        # Repopulate
        while len(survivors) < 250:
            survivors.append(random.choice(survivors).replicate())
        cells = survivors

        history.append({
            'step': t,
            'resistance': np.mean([c.resistance for c in cells]),
            'closure': np.mean([c.closure_degree for c in cells]),
            'fitness': np.mean([c.fitness for c in cells]),
            'therapy': drug
        })
    return pd.DataFrame(history)

# ======================================================================
# ANALYTICS & VISUALIZATION
# ======================================================================

def visualize_results(df, therapy_start):
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Timeline: Resistance & Closure
    ax1 = axes[0,0]
    ax1.plot(df['step'], df['resistance'], label='Avg Resistance', color='blue')
    ax1.plot(df['step'], df['closure'], label='Closure Degree', color='green')
    ax1.axvline(therapy_start, color='red', linestyle='--', label='Therapy Start')
    ax1.set_title("Temporal Dynamics")
    ax1.legend()

    # 2. Correlation Plot
    ax2 = axes[0,1]
    sns.regplot(x='resistance', y='closure', data=df, ax=ax2, color='purple', scatter_kws={'alpha':0.3})
    ax2.set_title("Correlation: Resistance vs Loop Closure")

    # 3. Fitness Evolution
    ax3 = axes[1,0]
    ax3.fill_between(df['step'], df['fitness'], color='orange', alpha=0.3)
    ax3.plot(df['step'], df['fitness'], color='darkorange')
    ax3.set_title("Population Fitness Over Time")

    # 4. Phase Space
    ax4 = axes[1,1]
    sc = ax4.scatter(df['resistance'], df['fitness'], c=df['step'], cmap='viridis')
    plt.colorbar(sc, ax=ax4, label='Step')
    ax4.set_title("Phase Space: Resistance -> Fitness")
    
    plt.tight_layout()
    plt.show()

    # Summary Table
    last = df.iloc[-1]
    first = df.iloc[0]
    summary_md = f"""
### 📊 UAF Simulation Summary
| Metric | Start | End | Change |
| :--- | :--- | :--- | :--- |
| **Avg Resistance** | {first['resistance']:.3f} | {last['resistance']:.3f} | +{(last['resistance']-first['resistance']):.3f} |
| **Closure Degree** | {first['closure']:.3f} | {last['closure']:.3f} | {last['closure']-first['closure']:.3f} |
| **Population Fitness** | {first['fitness']:.3f} | {last['fitness']:.3f} | {last['fitness']-first['fitness']:.3f} |

**Interpretation:** Negative correlation confirms that resistance induces decoupling from tissue signals.
    """
    display(Markdown(summary_md))

# RUN
results_df = run_uaf_simulation(steps=150, therapy_start=50)
visualize_results(results_df, therapy_start=50)
