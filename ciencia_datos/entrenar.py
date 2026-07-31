# Entrenamiento del modelo de Tecnoteca (versión script del notebook).
# Pipeline: TF-IDF (1-2 gramas, stopwords en español) + Regresión Logística
# para clasificar, más K-Means para agrupar por temas. El artefacto final se
# serializa con joblib y, si OCI está habilitado, se sube a Object Storage.
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, silhouette_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline

from ciencia_datos.stopwords_es import STOPWORDS_VECTORIZADOR

RAIZ = Path(__file__).resolve().parent.parent
DIR_DATOS = RAIZ / "data"
DIR_MODELOS = RAIZ / "models"
SEMILLA = 42
VERSION = "1.0.0"


def construir_vectorizador() -> TfidfVectorizer:
    return TfidfVectorizer(
        stop_words=STOPWORDS_VECTORIZADOR,
        ngram_range=(1, 2),
        min_df=2,
        max_features=40000,
        sublinear_tf=True,
        strip_accents="unicode",
        lowercase=True,
    )


def construir_clasificador() -> LogisticRegression:
    return LogisticRegression(max_iter=2000, C=5.0, class_weight="balanced",
                              random_state=SEMILLA)


def texto_completo(df: pd.DataFrame) -> pd.Series:
    return df["titulo"].str.strip() + ". " + df["texto"].str.strip()


def cargar_datos() -> tuple[pd.DataFrame, pd.DataFrame]:
    contenidos = pd.read_csv(DIR_DATOS / "contenidos.csv")
    manual = pd.read_csv(DIR_DATOS / "evaluacion_manual.csv")
    contenidos = (contenidos.dropna(subset=["titulo", "texto", "categoria"])
                  .drop_duplicates(subset=["texto"]).reset_index(drop=True))
    return contenidos, manual


def etiquetas_de_clusters(vectorizador, kmeans, n_terminos: int = 4) -> dict[int, str]:
    nombres = vectorizador.get_feature_names_out()
    etiquetas = {}
    for c, centro in enumerate(kmeans.cluster_centers_):
        mejores = np.argsort(centro)[::-1]
        terminos = []
        for i in mejores:
            termino = str(nombres[i])
            if " " not in termino:  # preferimos unigramas como etiqueta legible
                terminos.append(termino)
            if len(terminos) == n_terminos:
                break
        etiquetas[c] = ", ".join(terminos)
    return etiquetas


def main() -> None:
    print("== Tecnoteca · Entrenamiento del modelo ==")
    contenidos, manual = cargar_datos()
    X, y = texto_completo(contenidos), contenidos["categoria"]
    print(f"Dataset: {len(contenidos)} documentos, {y.nunique()} categorías")

    # ── Evaluación honesta: partición de prueba + validación cruzada ──
    X_ent, X_pru, y_ent, y_pru = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=SEMILLA)
    vectorizador = construir_vectorizador()
    clasificador = construir_clasificador()
    clasificador.fit(vectorizador.fit_transform(X_ent), y_ent)
    y_pred = clasificador.predict(vectorizador.transform(X_pru))
    exactitud = accuracy_score(y_pru, y_pred)
    f1_macro = f1_score(y_pru, y_pred, average="macro")
    print(f"Partición de prueba (20%): exactitud {exactitud:.3f} | F1 macro {f1_macro:.3f}")

    cv = cross_val_score(make_pipeline(construir_vectorizador(), construir_clasificador()),
                         X, y, cv=5, scoring="f1_macro")
    print(f"Validación cruzada (5 pliegues): F1 macro {cv.mean():.3f} ± {cv.std():.3f}")

    # ── Generalización: ejemplos escritos a mano, fuera de las plantillas ──
    X_man = texto_completo(manual)
    y_man_pred = clasificador.predict(vectorizador.transform(X_man))
    exactitud_manual = accuracy_score(manual["categoria"], y_man_pred)
    print(f"Evaluación manual ({len(manual)} textos escritos a mano): "
          f"exactitud {exactitud_manual:.3f}")
    errores_manual = [
        {"titulo": fila.titulo, "real": fila.categoria, "predicha": pred}
        for fila, pred in zip(manual.itertuples(), y_man_pred) if fila.categoria != pred
    ]
    for e in errores_manual:
        print(f"  · «{e['titulo']}»: real {e['real']} → predicha {e['predicha']}")

    # ── Modelo final: reentrenado con TODO el corpus para producción ──
    vectorizador = construir_vectorizador()
    matriz = vectorizador.fit_transform(X)
    clasificador = construir_clasificador()
    clasificador.fit(matriz, y)

    # ── Agrupación por temas (no supervisada) ──
    kmeans = KMeans(n_clusters=y.nunique(), random_state=SEMILLA, n_init=10)
    kmeans.fit(matriz)
    muestra = np.random.RandomState(SEMILLA).choice(matriz.shape[0],
                                                    size=min(800, matriz.shape[0]),
                                                    replace=False)
    silueta = silhouette_score(matriz[muestra], kmeans.labels_[muestra], metric="cosine")
    temas = etiquetas_de_clusters(vectorizador, kmeans)
    print(f"K-Means (k={kmeans.n_clusters}): coeficiente de silueta {silueta:.3f}")

    metricas = {
        "version": VERSION,
        "entrenado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sklearn": sklearn.__version__,
        "documentos": int(len(contenidos)),
        "categorias": sorted(y.unique().tolist()),
        "exactitud_prueba": round(float(exactitud), 4),
        "f1_macro_prueba": round(float(f1_macro), 4),
        "cv_f1_macro_media": round(float(cv.mean()), 4),
        "cv_f1_macro_desv": round(float(cv.std()), 4),
        "exactitud_manual": round(float(exactitud_manual), 4),
        "errores_manual": errores_manual,
        "silueta_kmeans": round(float(silueta), 4),
        "reporte_clasificacion": classification_report(y_pru, y_pred),
        "matriz_confusion": confusion_matrix(y_pru, y_pred).tolist(),
    }

    artefacto = {
        "version": VERSION,
        "creado": metricas["entrenado_en"],
        "vectorizador": vectorizador,
        "clasificador": clasificador,
        "categorias": metricas["categorias"],
        "kmeans": kmeans,
        "temas_clusters": temas,
        "metricas": metricas,
    }
    DIR_MODELOS.mkdir(exist_ok=True)
    ruta_modelo = DIR_MODELOS / "modelo.joblib"
    joblib.dump(artefacto, ruta_modelo, compress=3)
    with open(DIR_MODELOS / "metricas.json", "w", encoding="utf-8") as f:
        json.dump(metricas, f, ensure_ascii=False, indent=2)
    tamano = ruta_modelo.stat().st_size / 1_048_576
    print(f"Artefacto serializado: {ruta_modelo} ({tamano:.1f} MB)")

    # ── Registro de modelos en OCI Object Storage (opcional) ──
    from servicio_modelo import oci_almacen
    if oci_almacen.habilitado():
        oci_almacen.subir_modelo(ruta_modelo)
    else:
        print("OCI: deshabilitado (exporta OCI_ENABLED=true para subir el artefacto).")


if __name__ == "__main__":
    main()
