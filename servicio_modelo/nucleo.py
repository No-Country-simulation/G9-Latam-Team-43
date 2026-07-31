# Núcleo del servicio de modelo: carga el artefacto serializado y expone las
# operaciones de análisis (clasificación, palabras clave, tema, explicación).
import numpy as np
import joblib

from ciencia_datos.tecnologias import palabras_clave


class Cerebro:
    def __init__(self, ruta_artefacto: str):
        artefacto = joblib.load(ruta_artefacto)
        self.version = artefacto["version"]
        self.vectorizador = artefacto["vectorizador"]
        self.clasificador = artefacto["clasificador"]
        self.categorias = artefacto["categorias"]
        self.kmeans = artefacto.get("kmeans")
        self.temas_clusters = artefacto.get("temas_clusters", {})
        self.metricas = artefacto.get("metricas", {})

    @staticmethod
    def _unir(titulo: str, texto: str) -> str:
        return f"{titulo.strip()}. {texto.strip()}"

    def vector(self, titulo: str, texto: str):
        return self.vectorizador.transform([self._unir(titulo, texto)])

    def vector_texto(self, texto: str):
        return self.vectorizador.transform([texto])

    def _explicacion(self, X, categoria: str, cuantos: int = 5) -> list[dict]:
        """Términos del documento que más aportan a la categoría predicha
        (peso = coeficiente de la regresión logística × TF-IDF del término)."""
        indice = list(self.clasificador.classes_).index(categoria)
        contribuciones = X.multiply(self.clasificador.coef_[indice]).toarray()[0]
        nombres = self.vectorizador.get_feature_names_out()
        mejores = np.argsort(contribuciones)[::-1][:cuantos]
        return [{"termino": str(nombres[i]), "peso": round(float(contribuciones[i]), 4)}
                for i in mejores if contribuciones[i] > 0]

    def analizar(self, titulo: str, texto: str) -> dict:
        X = self.vector(titulo, texto)
        probabilidades = self.clasificador.predict_proba(X)[0]
        ganadora = int(np.argmax(probabilidades))
        categoria = str(self.clasificador.classes_[ganadora])
        distribucion = {str(c): round(float(p), 4)
                        for c, p in zip(self.clasificador.classes_, probabilidades)}
        distribucion = dict(sorted(distribucion.items(), key=lambda kv: -kv[1]))

        resultado = {
            "categoria": categoria,
            "probabilidad": round(float(probabilidades[ganadora]), 4),
            "distribucion": distribucion,
            "palabras_clave": palabras_clave(self._unir(titulo, texto), self.vectorizador),
            "explicacion": self._explicacion(X, categoria),
        }
        if self.kmeans is not None:
            grupo = int(self.kmeans.predict(X)[0])
            resultado["tema"] = {"id": grupo,
                                 "etiqueta": self.temas_clusters.get(grupo, "")}
        return resultado
