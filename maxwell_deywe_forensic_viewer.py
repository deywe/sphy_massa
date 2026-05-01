import pandas as pd
import numpy as np
import hashlib
import sys

def validate_and_view(file_path):
    try:
        # Carrega o dataset gerado anteriormente
        df = pd.read_parquet(file_path)
        print(f"--- [MAXWELL-DEYWE FORENSIC VIEWER] Analisando: {file_path} ---")
    except Exception as e:
        print(f"❌ Erro ao abrir o arquivo: {e}")
        sys.exit(1)
    
    corrupted_frames = []

    for index, row in df.iterrows():
        # RECONSTRUÇÃO DO HASH VETORIAL
        # Convertemos o wave_vector de volta para bytes hex para bater com o gerador
        wave_vector_hex = np.array(row['wave_vector'], dtype=np.float32).tobytes().hex()
        
        # A string de conferência deve ser idêntica à usada no momento da assinatura
        check_str = f"{int(row['frame_id'])}-{row['veracity']:.4f}-{wave_vector_hex}"
        recalculated_hash = hashlib.sha256(check_str.encode()).hexdigest()
        
        if recalculated_hash != row['sha256']:
            corrupted_frames.append(int(row['frame_id']))
            print(f"❌ VIOLAÇÃO DETECTADA no Frame {int(row['frame_id'])}")
        
    if not corrupted_frames:
        print("💎 INTEGRIDADE ABSOLUTA: Todos os hashes conferem com a malha de Planck.")
        print(f"📊 Total de Frames Validados: {len(df)}")
        print(f"✅ Média de Veracidade do Nó (η): {df['veracity'].mean():.6f}")
        # Aqui o sistema está pronto para alimentar o motor Ursina ou Matplotlib
    else:
        print(f"⚠️ ALERTA CRÍTICO: {len(corrupted_frames)} frames foram comprometidos.")
        sys.exit(1)

if __name__ == "__main__":
    # Certifique-se de que o arquivo Parquet foi gerado com a versão vetorial do script
    validate_and_view("harpia_forensic_data.parquet")
