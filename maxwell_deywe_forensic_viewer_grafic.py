import pandas as pd
import numpy as np
import hashlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

def validate_frame(row):
    """
    Valida o hash SHA-256 do vetor completo para garantir integridade forense.
    Sincronizado com o novo formato vetorial.
    """
    # Convertemos o vetor de volta para hex para validar o hash exatamente como foi gerado
    wave_vector_hex = np.array(row['wave_vector'], dtype=np.float32).tobytes().hex()
    check_str = f"{int(row['frame_id'])}-{row['veracity']:.4f}-{wave_vector_hex}"
    recalculated_hash = hashlib.sha256(check_str.encode()).hexdigest()
    return recalculated_hash == row['sha256']

def get_torus_coords_from_dataset(row):
    """
    Reconstrói o nó usando o vetor real de 2000 pontos salvo no Parquet.
    """
    n_points = 2000
    phi_golden = (1 + np.sqrt(5)) / 2
    R, r = 3, 1
    
    theta = np.linspace(0, 2*np.pi, n_points)
    veracity = row['veracity']
    phi = theta * phi_golden * (1.0 / max(0.01, veracity))
    
    # Recupera o vetor de ruído detalhado que estava faltando no seu erro
    noise = np.array(row['wave_vector'])
    
    x = (R + (r + noise) * np.cos(phi)) * np.cos(theta)
    y = (R + (r + noise) * np.cos(phi)) * np.sin(theta)
    z = (r + noise) * np.sin(phi)
    return x, y, z

# --- Carga e Validação do Dataset ---
file_path = "harpia_forensic_data.parquet"
try:
    df = pd.read_parquet(file_path)
    print(f"--- [MAXWELL-DEYWE] Validando Dataset Vetorial: {file_path} ---")
except FileNotFoundError:
    print(f"❌ Erro: Arquivo {file_path} não encontrado. Gere o dataset primeiro!")
    sys.exit(1)

# Validação Forense Inicial (Agora conferindo o vetor completo)
print("🔍 Verificando assinaturas SHA-256 de cada nó...")
invalid_frames = df[~df.apply(validate_frame, axis=1)]

if not invalid_frames.empty:
    print(f"⚠️ ALERTA DE VIOLAÇÃO: {len(invalid_frames)} frames corrompidos detectados!")
    sys.exit(1)
print("💎 INTEGRIDADE CONFIRMADA: O Nó Informacional é autêntico.")

# --- Configuração da Visualização 3D ---
fig = plt.figure(figsize=(12, 8), facecolor='#050505')
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.2)

# Slider para navegar pelos Frames do Dataset
ax_frame = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='#1a1a1a')
slider_frame = Slider(ax_frame, 'FRAME DATASET ', 0, len(df)-1, valinit=0, valstep=1, color='#00f2ff')

# Renderização inicial (Frame 0)
initial_row = df.iloc[0]
x, y, z = get_torus_coords_from_dataset(initial_row)
line, = ax.plot(x, y, z, color='#00f2ff', lw=0.5, alpha=0.7)

ax.set_facecolor('#050505')
ax.grid(False)
ax.set_axis_off()
ax.set_title(f"HARPIA QOS | FORENSIC VIEWER (VETORIAL) | {file_path}", color='white', fontsize=12)

def update(val):
    frame_idx = int(slider_frame.val)
    row = df.iloc[frame_idx]
    
    # Atualiza a geometria com os 2000 pontos reais
    new_x, new_y, new_z = get_torus_coords_from_dataset(row)
    line.set_data(new_x, new_y)
    line.set_3d_properties(new_z)
    
    # Cor baseada na veracidade real do dataset
    v = row['veracity']
    line.set_color((1-v, v, 1))
    fig.canvas.draw_idle()

slider_frame.on_changed(update)

print("--- [SIMBIOTICA AI] MODO LEITURA DE DATASET VETORIAL ATIVO ---")
plt.show()
