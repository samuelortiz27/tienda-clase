import json
import os

import faiss
import pandas as pd
from django.conf import settings
from sentence_transformers import SentenceTransformer

ARTEFACTS_DIR = os.path.join(settings.BASE_DIR, "core", "ia", "artefactos")

with open(os.path.join(ARTEFACTS_DIR, "config.json"), encoding="utf-8") as cfg_file:
    CONFIG = json.load(cfg_file)

MODEL = SentenceTransformer(CONFIG["model_name"]) # Instancia del modelo de embeddings
INDEX = faiss.read_index(os.path.join(ARTEFACTS_DIR, "faiss.index")) # Carga el índice FAISS
CATALOGO = pd.read_csv(os.path.join(ARTEFACTS_DIR, "productos.csv")) # Lee el catálogo de productos

def buscar_productos(query, k = 5):
    query = query.strip()
    if not query:
        return []
    
    emb = MODEL.encode([query], normalize_embeddings=True).astype("float32")
    D, I = INDEX.search(emb, k)

    resultados = []

    for score, idx in zip(D[0], I[0]):
        if idx < 0:
            continue
        fila = CATALOGO.iloc[int(idx)].to_dict()
        fila["score"] = float(score)
        resultados.append(fila)
    
    return resultados