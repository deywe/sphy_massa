from ursina import *
import pandas as pd
import numpy as np
import hashlib
import sys
import time as python_time # Import extra para evitar conflito

# --- Configurações de Janela FullHD ---
app = Ursina(
    title='HARPIA QOS | FORENSIC REAL-TIME INSPECTOR',
    borderless=False,
    fullscreen=False,
    size=(1920, 1080)
)

window.color = color.black
window.show_ursina_splash = False

# --- Carga de Dados ---
FILE_PATH = "harpia_forensic_data.parquet"
try:
    df = pd.read_parquet(FILE_PATH)
    total_frames = len(df)
    print(f"✅ Dataset carregado: {total_frames} frames.")
except Exception as e:
    print(f"❌ Erro ao ler Parquet: {e}")
    sys.exit()

# --- Entidades Visuais ---
n_points = 400 
points = [Entity(model='sphere', scale=0.07, color=color.cyan) for _ in range(n_points)]

status_text = Text(text='STATUS: VALIDANDO SHA-256', position=(-0.85, 0.45), scale=2, color=color.green)
info_text = Text(text='', position=(-0.85, 0.38), scale=1.2)

current_frame = 0
t = 0 # Contador de tempo manual para a câmera

def validate_sha256(row):
    """Validação rigorosa do SHA-256 do vetor completo."""
    wave_vector_hex = np.array(row['wave_vector'], dtype=np.float32).tobytes().hex()
    check_str = f"{int(row['frame_id'])}-{row['veracity']:.4f}-{wave_vector_hex}"
    recalculated_hash = hashlib.sha256(check_str.encode()).hexdigest()
    return recalculated_hash == row['sha256']

def update():
    global current_frame, t
    
    # Incremento do tempo para animação suave
    t += time.dt 
    
    # 1. Recuperar linha do Dataset
    row = df.iloc[current_frame]
    
    # 2. Auditoria Forense
    if not validate_sha256(row):
        status_text.text = "⚠️ VIOLAÇÃO DETECTADA!"
        status_text.color = color.red
        return 

    # 3. Reconstrução SPHY
    phi_golden = (1 + np.sqrt(5)) / 2
    R, r = 3, 1
    theta_vals = np.linspace(0, 2*np.pi, n_points)
    veracity = row['veracity']
    noise_vector = np.array(row['wave_vector'])[:n_points] 
    
    phi_vals = theta_vals * phi_golden * (1.0 / max(0.01, veracity))
    
    # 4. Atualização da Malha 3D
    for i in range(len(noise_vector)):
        noise = noise_vector[i]
        x = (R + (r + noise) * np.cos(phi_vals[i])) * np.cos(theta_vals[i])
        y = (R + (r + noise) * np.cos(phi_vals[i])) * np.sin(theta_vals[i])
        z = (r + noise) * np.sin(phi_vals[i])
        
        points[i].position = (x, y, z)
        points[i].color = lerp(color.magenta, color.cyan, veracity)

    # 5. Interface e Movimento
    info_text.text = f"FRAME: {current_frame}\nVERACIDADE: {veracity:.4f}\nHASH: {row['sha256'][:20]}..."
    current_frame = (current_frame + 1) % total_frames
    
    # Rotação da câmera usando o 't' acumulado (evita erro de tipo)
    camera.x = 15 * np.sin(t * 0.5)
    camera.z = 15 * np.cos(t * 0.5)
    camera.y = 3
    camera.look_at(Vec3(0,0,0))

def input(key):
    if key == 'escape':
        application.quit()

app.run()
