import os
import time
import hashlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def audit_and_visualize_sphy():
    csv_filename = "sphy_clifford_audit_trail.csv"
    
    if not os.path.exists(csv_filename):
        print(f"Error: The file '{csv_filename}' was not found in the current directory.")
        return

    # 1. Dataset Loading
    df = pd.read_csv(csv_filename)
    records = df.to_dict(orient="records")
    
    # 2. SHA-512 Cryptographic Chain Audit
    chain_valid = True
    for i, rec in enumerate(records):
        if i == 0:
            expected_prev = "0" * 128
        else:
            expected_prev = records[i-1]["sha512_hash"]
            
        if rec["prev_hash"] != expected_prev:
            chain_valid = False
            
        re_raw = f"{int(rec['atomic_timestamp_ns'])}|{int(rec['batch_id'])}|{int(rec['total_qubits'])}|{float(rec['clock_ghz']):.1f}|{float(rec['thermal_noise']):.1f}|{rec['bit_flip_status']}|{int(rec['batch_cycles'])}|{float(rec['avg_cycles_per_step']):.2f}|{float(rec['energy_metric']):.6f}|{float(rec['variance_metric']):.7f}|{rec['prev_hash']}"
        re_hash = hashlib.sha512(re_raw.encode('utf-8')).hexdigest()
        
        if re_hash != rec["sha512_hash"]:
            chain_valid = False

    print("=================================================================")
    print("       SPHY PYTHON AUDITOR & MATHEMATICAL VISUALIZER             ")
    print("=================================================================")
    print(f" SHA-512 Chain Integrity       : {'APPROVED (100% INTEGRITY)' if chain_valid else 'INTEGRITY FAILURE'}")
    print(f" Total Audited Batches         : {len(df)}")
    print(f" Total Torus Qubits (S^3)      : {df['total_qubits'].iloc[0]} Qubits (40x30)")
    print(f" Clock Frequency (Si x e-)     : {df['clock_ghz'].iloc[0]:.1f} GHz")
    print("=================================================================")

    # 3. Summary Statistics
    mean_energy = df['energy_metric'].mean()
    std_energy = df['energy_metric'].std()
    mean_variance = df['variance_metric'].mean()
    mean_cycles = df['avg_cycles_per_step'].mean()

    print("[Statistical Metrics]")
    print(" • Mean Field Energy (mathcal{E}) : " + f"{mean_energy:.6f} (± {std_energy:.6f})")
    print(" • Mean Grid Variance (sigma^2)   : " + f"{mean_variance:.7f}")
    print(" • Mean Cycles per Step        : " + f"{mean_cycles:.2f} cycles/step")
    print("=================================================================")

    # 4. Plot Generation with LaTeX-style Mathematical Notation
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm"
    })

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(df['batch_id'], df['energy_metric'], marker='o', color='#1f77b4', linewidth=2, label=r'Energy Metric $\int |\Phi|^2 d\Omega$')
    axes[0].set_ylabel(r'Elastic Field Energy ($\mathcal{E}$)', fontsize=12)
    axes[0].set_title(r'\textbf{SPHY Bare Metal Engine} -- Clifford Torus Validation ($S^3$ | $N = 1200$ Qubits)', fontsize=13)
    axes[0].grid(True, linestyle='--', alpha=0.6)
    axes[0].legend(loc='upper right', fontsize=11)

    axes[1].plot(df['batch_id'], df['variance_metric'], marker='s', color='#ff7f0e', linewidth=2, label=r'Variance $\sigma^2(\Phi)$ under Thermal Noise $1.0$')
    axes[1].set_xlabel(r'Processing Batches ($Batch\ ID$)', fontsize=12)
    axes[1].set_ylabel(r'Stabilized Variance ($\sigma^2$)', fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.6)
    axes[1].legend(loc='upper right', fontsize=11)

    plt.tight_layout()
    chart_filename = "sphy_clifford_validation_plot.png"
    plt.savefig(chart_filename, dpi=300)
    plt.close()
    
    print(f" High-resolution chart saved to: {chart_filename}")
    print("=================================================================\n")

if __name__ == "__main__":
    audit_and_visualize_sphy()
