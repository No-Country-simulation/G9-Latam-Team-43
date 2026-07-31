# Índice vectorial en memoria para similitud entre documentos (recomendación y
# búsqueda semántica). La fuente de verdad de los contenidos es la base de datos
# del back-end Java: al arrancar, el back-end sincroniza el índice con
# POST /reindexar y lo mantiene al día con POST /indexar.
import threading

from sklearn.metrics.pairwise import linear_kernel

from servicio_modelo.nucleo import Cerebro


class IndiceVectorial:
    def __init__(self, cerebro: Cerebro):
        self._cerebro = cerebro
        self._candado = threading.Lock()
        self._documentos: dict[int, dict] = {}  # id -> {texto_completo, categoria}
        self._ids: list[int] = []
        self._categorias: list[str] = []
        self._matriz = None
        self._sucio = False

    @property
    def tamano(self) -> int:
        return len(self._documentos)

    def reindexar(self, documentos: list[dict]) -> int:
        with self._candado:
            self._documentos = {
                int(d["id"]): {
                    "texto": f"{d['titulo'].strip()}. {d['texto'].strip()}",
                    "categoria": d.get("categoria") or "",
                }
                for d in documentos
            }
            self._sucio = True
        return len(self._documentos)

    def indexar(self, doc: dict) -> int:
        with self._candado:
            self._documentos[int(doc["id"])] = {
                "texto": f"{doc['titulo'].strip()}. {doc['texto'].strip()}",
                "categoria": doc.get("categoria") or "",
            }
            self._sucio = True
        return len(self._documentos)

    def _reconstruir_si_hace_falta(self):
        with self._candado:
            if not self._sucio:
                return
            self._ids = list(self._documentos.keys())
            self._categorias = [self._documentos[i]["categoria"] for i in self._ids]
            textos = [self._documentos[i]["texto"] for i in self._ids]
            self._matriz = (self._cerebro.vectorizador.transform(textos)
                            if textos else None)
            self._sucio = False

    def similares(self, texto: str, k: int = 3, excluir_id: int | None = None,
                  categoria: str | None = None, umbral: float = 0.03) -> list[dict]:
        self._reconstruir_si_hace_falta()
        if self._matriz is None:
            return []
        consulta = self._cerebro.vector_texto(texto)
        similitudes = linear_kernel(consulta, self._matriz)[0]
        orden = similitudes.argsort()[::-1]
        resultados = []
        for posicion in orden:
            doc_id = self._ids[posicion]
            if excluir_id is not None and doc_id == excluir_id:
                continue
            if categoria and self._categorias[posicion].lower() != categoria.lower():
                continue
            similitud = float(similitudes[posicion])
            if similitud < umbral:
                break
            resultados.append({"id": doc_id, "similitud": round(similitud, 4)})
            if len(resultados) >= k:
                break
        return resultados
