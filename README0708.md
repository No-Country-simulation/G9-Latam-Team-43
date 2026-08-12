# TechMind Model — Clasificador Modular de Texto Técnico

Este proyecto implementa una arquitectura modular de Machine Learning para la clasificación de texto técnico (consultas, tickets, publicaciones e incidencias). Utiliza **Scikit-learn** con un **Pipeline unificado** que integra vectorización de texto via **TF-IDF** y modelos de clasificación como Regresión Logística, LinearSVC o Ensamble por votación.

---

## 📁 Estructura del Proyecto

```text
techmind_model/
│
├── data/
│   └── dataset.csv             # Dataset de entrenamiento (CSV con columnas 'texto_completo' y 'categoria')
│
├── models/
│   └── pipeline_techmind.pkl   # Modelo entrenado persistido (artefacto serializado con Joblib)
│
├── reports/
│   ├── metrics.json            # Reporte de métricas de desempeño (Accuracy, Precision, Recall, F1)
│   └── confusion_matrix.png    # Matriz de confusión visual en formato PNG
│
├── src/                        # Código fuente modular
│   ├── __init__.py             # Identificador de paquete Python
│   ├── config.py               # Configuración global, constantes y rutas
│   ├── text_cleaner.py         # Limpieza, normalización y preservación de jerga técnica (.NET, C#, React 18, etc.)
│   ├── dataset_loader.py       # Carga, validación de esquema y preprocesamiento de datos
│   ├── model_factory.py        # Fábrica de pipelines de clasificación (Logistic Regression, LinearSVC, Voting)
│   ├── model_trainer.py        # División de datos (Train/Test) y entrenamiento del pipeline
│   ├── model_evaluator.py      # Generación de métricas cuantitativas y matriz de confusión en imagen
│   ├── model_optimizer.py      # Búsqueda sistemática de hiperparámetros con GridSearchCV (F1 Macro)
│   └── predictor.py            # Interfaz de inferencia para producción o consumo de API
│
├── scripts/                    # Scripts de orquestación y flujo principal
│   ├── __init__.py
│   ├── train_model.py          # Entrenamiento base y exportación del pipeline
│   ├── optimize_model.py       # Optimización por grilla de hiperparámetros y selección del mejor pipeline
│   └── predict_text.py         # Script para probar inferencia con salida en formato JSON estricto
│
├── requirements.txt            # Dependencias del entorno Python
└── README.md                   # Documentación del proyecto
```

---

## ⚙️ Guía de Uso Paso a Paso

### 1. Preparación del Dataset
Coloca tu conjunto de datos de entrenamiento en:
```bash
data/dataset.csv
```
> **Requisito del CSV:** Debe contener las columnas `texto_completo` (texto de entrada) y `categoria` (etiqueta objetivo).

---

### 2. Instalación de Dependencias
Crea y activa un entorno virtual antes de instalar los paquetes requeridos:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Linux/macOS)
source venv/bin/activate

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

### 3. Entrenamiento Base del Modelo
Para ejecutar un entrenamiento inicial rápido, generar el pipeline y los reportes de métricas:

```bash
python -m scripts.train_model
```

**Flujo interno de ejecución:**
1. `DatasetLoader` carga el dataset y valida columnas.
2. `TextCleaner` procesa el texto conservando variantes técnicas (`Node.js`, `C#`, `React 18`, `HTTP 500`, etc.).
3. `ModelFactory` y `ModelTrainer` construyen, entrenan y evalúan el pipeline.
4. Genera y guarda:
   - Pipeline compilado en `models/pipeline_techmind.pkl`.
   - Reporte de métricas en `reports/metrics.json`.
   - Gráfico de la matriz de confusión en `reports/confusion_matrix.png`.

---

### 4. Búsqueda y Optimización de Hiperparámetros (GridSearchCV)
Para optimizar sistemáticamente los parámetros de TF-IDF (`max_features`, `ngram_range`, `sublinear_tf`) y del modelo ($C$, `class_weight`, `loss`) maximizando **F1 Macro**:

```bash
python -m scripts.optimize_model
```

Este proceso ejecuta una validación cruzada de 5 pliegues ($5	ext{-fold CV}$), selecciona la mejor combinación y re-exporta el archivo final en `models/pipeline_techmind.pkl`.

---

### 5. Inferencia y Generación de JSON Estricto
Para clasificar un nuevo texto desde la terminal:

```bash
python -m scripts.predict_text
```

**Uso programático en Python (con salida JSON estricta):**

```python
import json
from src.config import MODEL_PATH
from src.predictor import TechMindPredictor

# 1. Cargar el predictor con el pipeline serializado
predictor = TechMindPredictor(MODEL_PATH)

# 2. Texto de consulta
texto = "Tengo un problema de deadlock en PostgreSQL al ejecutar consultas concurrentes."

# 3. Predecir (obtiene un diccionario Python)
resultado_dict = predictor.predict(texto)

# 4. Formatear a JSON estricto e imprimir
resultado_json = json.dumps(resultado_dict, indent=4, ensure_ascii=False)
print(resultado_json)
```

**Salida JSON obtenida:**
```json
{
    "texto_limpio": "tengo un problema de deadlock en postgresql al ejecutar consultas concurrentes.",
    "categoria_predicha": "Base de Datos",
    "top_categorias": [
        {
            "categoria": "Base de Datos",
            "probabilidad": 0.8945
        },
        {
            "categoria": "Backend",
            "probabilidad": 0.0721
        },
        {
            "categoria": "DevOps",
            "probabilidad": 0.0334
        }
    ],
    "confianza": 0.8945
}
```

---

## 🚀 Ventajas Principales de la Arquitectura

1. **Pipeline Unificado de Scikit-Learn:** Encapsula el vectorizador TF-IDF y el clasificador en un único objeto binario (`.pkl`). Evita diferencias de vocabulario o fugas de datos (*Data Leakage*) entre entrenamiento y producción.
2. **Limpieza Especializada en Tecnología:** Mantiene puntuaciones y símbolos indispensables para jerga de software (`.`, `#`, `+`, `-`, `_`, `/`).
3. **Optimización centrada en F1 Macro:** Permite balancear la precisión en categorías históricamente más complejas (como Backend o Frontend) sin descuidar el desempeño general.
4. **Listo para Producción:** El módulo `TechMindPredictor` permite integrarse sin fricción a microservicios web (FastAPI, Flask, etc.).
