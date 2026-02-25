import pandas as pd
import requests
import json
from newsapi import NewsApiClient

# --- CONFIGURACIÓN DE LLAVES ---
# Reemplaza con tus llaves reales
NEWS_API_KEY = 'd08d22081da74311acad48ed81f36444'
GNEWS_API_KEY = '0288f7e42296510ee333d4d106755c1a'
busqueda = 'Nemesio Oseguera "El Mencho"'

def get_newsapi_data(query):
    try:
        api = NewsApiClient(api_key=NEWS_API_KEY)
        res = api.get_everything(q=query, language='es', sort_by='relevancy')
        # Guardamos el título, fuente y el método
        return [{
            'fuente': a['source']['name'], 
            'titulo': a['title'], 
            'url': a['url'], 
            'metodo': 'NewsAPI'
        } for a in res['articles']]
    except Exception as e:
        print(f"⚠️ Error NewsAPI: {e}")
        return []

def get_gnews_data(query):
    url = f"https://gnews.io/api/v4/search?q={query}&lang=es&token={GNEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        res = response.json()
        return [{
            'fuente': a['source']['name'], 
            'titulo': a['title'], 
            'url': a['url'], 
            'metodo': 'GNews'
        } for a in res.get('articles', [])]
    except Exception as e:
        print(f"⚠️ Error GNews: {e}")
        return []

# 1. EJECUCIÓN DE LA RECOLECCIÓN
print("Buscando noticias...")
data_total = get_newsapi_data(busqueda) + get_gnews_data(busqueda)
df = pd.DataFrame(data_total)

if not df.empty:
    # 2. ANÁLISIS DE RIESGO (EDA APLICADO)
    clickbait_keywords = ['INCREÍBLE', 'MIRA EL VIDEO', 'NO CREERÁS', 'CONFIRMADO 100%', '¡', 'REVELADO', 'URGENTE']
    fuentes_verificadas = ['REUTERS', 'AP', 'EL UNIVERSAL', 'MILENIO', 'SEDENA', 'FGR', 'BBC', 'UNIVISION', 'CNN']

    def calcular_riesgo(row):
        score = 0
        titulo_up = row['titulo'].upper()
        
        # Criterio A: Palabras sensacionalistas
        if any(k in titulo_up for k in clickbait_keywords): 
            score += 2
            
        # Criterio B: Exceso de mayúsculas (clásico de fakes)
        # Si más del 30% del título son mayúsculas, es sospechoso
        mayusculas = sum(1 for c in row['titulo'] if c.isupper())
        if mayusculas > len(row['titulo']) * 0.3:
            score += 1
            
        # Criterio C: Validación de fuente
        if any(f in row['fuente'].upper() for f in fuentes_verificadas):
            score -= 2 # Restamos riesgo si la fuente es confiable
            
        return max(0, score) # No permitimos scores negativos

    df['nivel_riesgo'] = df.apply(calcular_riesgo, axis=1)

    # 3. GUARDAR EN JSON
    # 'orient=records' crea una lista de objetos JSON muy fácil de leer
    nombre_archivo = 'analisis_mencho_2026.json'
    df.to_json(nombre_archivo, orient='records', force_ascii=False, indent=4)
    
    print(f"✅ Proceso terminado. Se guardaron {len(df)} registros en {nombre_archivo}")

    # 4. MINI EXPLORACIÓN DE RESULTADOS
    print("\n--- RESUMEN DE RIESGO ---")
    print(df['nivel_riesgo'].value_counts().sort_index(ascending=False))
    
    # Mostrar las noticias más "sospechosas"
    print("\n--- NOTICIAS CON MAYOR RIESGO ---")
    print(df.sort_values(by='nivel_riesgo', ascending=False)[['fuente', 'titulo', 'nivel_riesgo']].head())

else:
    print("No se encontraron resultados. Verifica tus API Keys o la conexión.")