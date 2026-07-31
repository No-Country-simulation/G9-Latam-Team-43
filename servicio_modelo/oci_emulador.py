# Emulador local (mínimo) de OCI Object Storage.
#
# Implementa los endpoints de la API nativa que usa el SDK oficial `oci` en
# este proyecto — namespace, put_object, get_object y listado — guardando los
# objetos en disco (data/oci_local/objetos). Así la integración con OCI corre
# COMPLETA por defecto (firmas, cliente, streaming) sin necesitar una tenancy:
# para apuntar al Object Storage real basta cambiar variables de entorno
# (ver README, sección OCI). No valida las firmas: es solo para desarrollo.
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

app = FastAPI(
    title="Tecnoteca · Emulador local de OCI Object Storage",
    description="Réplica mínima de la API de Object Storage para desarrollo local.",
    version="1.0.0",
)


def _namespace() -> str:
    return os.getenv("OCI_NAMESPACE_LOCAL", "tecnoteca-local")


def _raiz() -> Path:
    return Path(os.getenv("OCI_DIR_LOCAL", "data/oci_local")) / "objetos"


def _ruta_objeto(cubeta: str, nombre: str) -> Path:
    base = (_raiz() / cubeta).resolve()
    ruta = (base / nombre).resolve()
    if base not in ruta.parents and ruta != base:
        raise ValueError("Nombre de objeto inválido")
    return ruta


@app.get("/")
def info():
    objetos = sum(1 for r in _raiz().rglob("*") if r.is_file()) if _raiz().exists() else 0
    return {"servicio": "emulador local de OCI Object Storage",
            "namespace": _namespace(), "objetos": objetos}


@app.get("/n/")
def namespace():
    return JSONResponse(content=_namespace())


@app.put("/n/{ns}/b/{cubeta}/o/{nombre:path}")
async def put_object(ns: str, cubeta: str, nombre: str, peticion: Request):
    try:
        ruta = _ruta_objeto(cubeta, nombre)
    except ValueError:
        return JSONResponse(status_code=400, content={"code": "InvalidObjectName",
                                                      "message": "Nombre inválido"})
    contenido = await peticion.body()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(contenido)
    md5 = hashlib.md5(contenido).hexdigest()
    return Response(status_code=200, headers={"etag": md5, "opc-request-id": "local",
                                              "opc-content-md5": md5})


@app.get("/n/{ns}/b/{cubeta}/o/{nombre:path}")
def get_object(ns: str, cubeta: str, nombre: str):
    try:
        ruta = _ruta_objeto(cubeta, nombre)
    except ValueError:
        return JSONResponse(status_code=400, content={"code": "InvalidObjectName",
                                                      "message": "Nombre inválido"})
    if not ruta.is_file():
        return JSONResponse(status_code=404, content={
            "code": "ObjectNotFound",
            "message": f"El objeto '{nombre}' no existe en el bucket '{cubeta}'"})
    contenido = ruta.read_bytes()
    return Response(content=contenido, media_type="application/octet-stream",
                    headers={"opc-request-id": "local",
                             "Content-Length": str(len(contenido))})


@app.get("/n/{ns}/b/{cubeta}/o")
def list_objects(ns: str, cubeta: str):
    base = _raiz() / cubeta
    objetos = []
    if base.exists():
        for ruta in sorted(base.rglob("*")):
            if ruta.is_file():
                objetos.append({
                    "name": str(ruta.relative_to(base)),
                    "size": ruta.stat().st_size,
                    "timeModified": datetime.fromtimestamp(
                        ruta.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
                })
    return {"objects": objetos, "prefixes": []}
