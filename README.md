# SPHY Theory: Mass as an Informational Node & Zero Inertia

This repository contains the digital proof and validation ecosystem for **SPHY Theory (Symbiotic Physics)**. The project demonstrates, through high-fidelity simulations and cryptographically signed datasets, how mass emerges not as an intrinsic property of matter, but as a phenomenon of **resonance and phase interference** within the background gravitational field (The Planck Mesh).

## 🌌 Overview: The Physics of Information
SPHY Theory proposes that what we perceive as "mass" is actually a **Toroidal Informational Node**.
*   **Classical Mass:** Result of a low-veracity state ($\eta \approx 0.52$), where phase noise creates inertia and resistance to motion.
*   **Zero Inertia:** Achieved through phase coherence ($\eta \to 1.0$), where the node aligns with the Golden Ratio ($\Phi$), allowing for displacement without inertial resistance (Antigravity).

## 🛠️ System Components

### 1. Reality Generators (Datasets)
The `.parquet` files contain 2,000 vector points per frame, representing the vibrational state of the node.
*   `massa_classica_052.parquet`: Demonstration of matter in a high-inertia state.
*   `inercia_zero_099.parquet`: Demonstration of the total coherence state and mass removal.
*   `harpia_forensic_data.parquet`: Primary dataset for training and validation.

### 2. Forensic Analyzers (Data Integrity)
Security and authenticity are guaranteed by a frame-by-frame SHA-256 audit layer.
*   `maxwell_deywe_forensic_viewer.py`: Terminal script for absolute integrity validation of hashes.
*   `maxwell_deywe_forensic_viewer_grafic.py`: Static Matplotlib viewer for harmonic analysis.

### 3. Real-Time Simulators (3D Visualization)
Developed using the **Ursina Engine** for visualizing phase dynamics in Full HD.
*   `maxwell_deywe_ursina_inspector.py`: Standard inspector with camera rotation and real-time hash monitoring.
*   `maxwell_deywe_ursina_inspector_inercia_zero.py`: Optimized version demonstrating syntropy flow and the "reversal" of the gravitational field.

## 🧪 How to Run

### Prerequisites
Install the necessary dependencies in your environment (Recommended: Pop!_OS or Ubuntu):
```bash
pip install -r requirements.txt
```

### Forensic Validation
To verify that the data has not been altered and matches the original signatures:
```bash
python3 maxwell_deywe_forensic_viewer.py
```

### Zero Inertia Demonstration
To visualize the phase transition and syntropy-based propulsion mechanics:
```bash
python3 maxwell_deywe_ursina_inspector_inercia_zero.py
```

## 📋 Security Protocol
Every frame in this repository is sealed with a SHA-256 signature that binds the `frame_id`, `veracity`, and the `wave_vector`. Any attempt to alter the dataset values will be immediately detected by the viewers, ensuring the **Sovereignty of Proof**.

---
**Author:** Deywe Okabe — SPHY Project  
**License:** Proprietary / Segregated Academic Research  
**Context:** Harpia QOS | Forensic Viewer Framework
