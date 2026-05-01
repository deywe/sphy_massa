import pandas as pd
import hashlib
import sys

def validate_and_view(file_path):
    df = pd.read_parquet(file_path)
    print(f"--- [MAXWELL-DEYWE FORENSIC VIEWER] Analisando: {file_path} ---")
    
    corrupted_frames = []

    for index, row in df.iterrows():
        # Recalcular o Hash para conferência
        check_str = f"{int(row['frame_id'])}-{row['wave_amplitude']:.10f}-{row['veracity']:.4f}"
        recalculated_hash = hashlib.sha256(check_str.encode()).hexdigest()
        
        if recalculated_hash != row['sha256']:
            corrupted_frames.append(int(row['frame_id']))
            print(f"❌ VIOLAÇÃO DETECTADA no Frame {int(row['frame_id'])}")
        
    if not corrupted_frames:
        print("💎 INTEGRIDADE ABSOLUTA: Todos os hashes conferem com a malha de Planck.")
        # Aqui você chamaria a lógica do seu visualizador Ursina ou Matplotlib
        print(f"Média de Veracidade do Nó: {df['veracity'].mean():.6f}")
    else:
        print(f"⚠️ ALERTA: {len(corrupted_frames)} frames foram comprometidos ou alterados.")
        sys.exit(1)

if __name__ == "__main__":
    validate_and_view("harpia_forensic_data.parquet")
