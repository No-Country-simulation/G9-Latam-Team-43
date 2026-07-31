# Servicio de modelo de Tecnoteca (API interna, consumida por el back-end Java).
# Carga el artefacto entrenado, clasifica contenido técnico, extrae palabras
# clave, agrupa por temas y calcula similitud entre documentos.
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from servicio_modelo import oci_almacen
from servicio_modelo.indice import IndiceVectorial
from servicio_modelo.nucleo import Cerebro

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("tecnoteca.modelo")

RUTA_MODELO = Path(os.getenv("MODELO_RUTA", "models/modelo.joblib"))

cerebro: Cerebro | None = None
indice: IndiceVectorial | None = None


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    global cerebro, indice
    if not RUTA_MODELO.exists() and oci_almacen.habilitado():
        log.info("Modelo no encontrado en local; intentando descargar de OCI...")
        oci_almacen.descargar_modelo(RUTA_MODELO)
    if RUTA_MODELO.exists():
        cerebro = Cerebro(str(RUTA_MODELO))
        indice = IndiceVectorial(cerebro)
        log.info("Modelo v%s cargado (%d categorías).", cerebro.version,
                 len(cerebro.categorias))
    else:
        log.error("No existe %s. Ejecuta ./run.bash entrenar (o habilita OCI).",
                  RUTA_MODELO)
    yield


app = FastAPI(
    title="Tecnoteca · Servicio de Modelo",
    description="API interna de ciencia de datos: clasificación de contenido "
                "técnico, palabras clave, agrupación por temas y similitud.",
    version="1.0.0",
    lifespan=ciclo_de_vida,
)


def obtener_cerebro() -> Cerebro:
    if cerebro is None:
        raise HTTPException(status_code=503,
                            detail="El modelo no está cargado. Ejecuta ./run.bash entrenar.")
    return cerebro


def obtener_indice() -> IndiceVectorial:
    obtener_cerebro()
    assert indice is not None
    return indice


@app.exception_handler(RequestValidationError)
async def entrada_invalida(_: Request, exc: RequestValidationError):
    detalles = [{"campo": ".".join(str(p) for p in e["loc"] if p != "body"),
                 "mensaje": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422,
                        content={"error": "Entrada inválida", "detalles": detalles})


@app.exception_handler(Exception)
async def error_interno(_: Request, exc: Exception):
    log.exception("Error no controlado: %s", exc)
    return JSONResponse(status_code=500, content={"error": "Error interno del servicio de modelo"})


# ── Esquemas de entrada ────────────────────────────────────────────────────
class EntradaAnalisis(BaseModel):
    titulo: str = Field(min_length=3, max_length=300)
    texto: str = Field(min_length=10, max_length=50_000)

    @field_validator("titulo", "texto")
    @classmethod
    def _no_vacio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("no puede estar vacío")
        return v


class DocumentoIndice(BaseModel):
    id: int
    titulo: str
    texto: str
    categoria: str | None = None


class EntradaReindexar(BaseModel):
    documentos: list[DocumentoIndice]


class EntradaSimilares(BaseModel):
    texto: str = Field(min_length=3, max_length=50_000)
    k: int = Field(default=3, ge=1, le=20)
    excluir_id: int | None = None
    categoria: str | None = None


class EntradaBusqueda(BaseModel):
    consulta: str = Field(min_length=2, max_length=500)
    k: int = Field(default=5, ge=1, le=50)
    categoria: str | None = None


# ── Endpoints ──────────────────────────────────────────────────────────────
@app.get("/salud")
def salud():
    return {
        "estado": "ok",
        "modelo_cargado": cerebro is not None,
        "version_modelo": cerebro.version if cerebro else None,
        "categorias": cerebro.categorias if cerebro else [],
        "documentos_indexados": indice.tamano if indice else 0,
        "oci": oci_almacen.estado(),
    }


@app.post("/analizar")
def analizar(entrada: EntradaAnalisis, modelo: Cerebro = Depends(obtener_cerebro)):
    return modelo.analizar(entrada.titulo, entrada.texto)


@app.post("/indexar")
def indexar(doc: DocumentoIndice, idx: IndiceVectorial = Depends(obtener_indice)):
    total = idx.indexar(doc.model_dump())
    return {"indexado": True, "total": total}


@app.post("/reindexar")
def reindexar(entrada: EntradaReindexar, idx: IndiceVectorial = Depends(obtener_indice)):
    total = idx.reindexar([d.model_dump() for d in entrada.documentos])
    return {"indexados": total}


@app.post("/similares")
def similares(entrada: EntradaSimilares, idx: IndiceVectorial = Depends(obtener_indice)):
    return {"resultados": idx.similares(entrada.texto, k=entrada.k,
                                        excluir_id=entrada.excluir_id,
                                        categoria=entrada.categoria)}


@app.post("/buscar")
def buscar(entrada: EntradaBusqueda, idx: IndiceVectorial = Depends(obtener_indice)):
    return {"resultados": idx.similares(entrada.consulta, k=entrada.k,
                                        categoria=entrada.categoria, umbral=0.01)}
