# Prueba de integración de OCI Object Storage contra el emulador local:
# el SDK oficial `oci` firma y ejecuta put_object/get_object de verdad.
import socket
import threading
import time
from pathlib import Path

import pytest
import uvicorn

from servicio_modelo.oci_emulador import app as app_emulador


@pytest.fixture(scope="module")
def puerto_emulador():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        puerto = s.getsockname()[1]
    servidor = uvicorn.Server(uvicorn.Config(app_emulador, host="127.0.0.1",
                                             port=puerto, log_level="warning"))
    hilo = threading.Thread(target=servidor.run, daemon=True)
    hilo.start()
    limite = time.time() + 10
    while not servidor.started:
        assert time.time() < limite, "el emulador no arrancó"
        time.sleep(0.05)
    yield puerto
    servidor.should_exit = True
    hilo.join(timeout=5)


def test_subir_y_descargar_modelo_por_oci(puerto_emulador, tmp_path, monkeypatch):
    monkeypatch.setenv("OCI_ENABLED", "true")
    monkeypatch.setenv("OCI_AUTH", "local")
    monkeypatch.setenv("OCI_ENDPOINT", f"http://127.0.0.1:{puerto_emulador}")
    monkeypatch.setenv("OCI_BUCKET", "bucket-pruebas")
    monkeypatch.setenv("OCI_DIR_LOCAL", str(tmp_path / "oci"))

    from servicio_modelo import oci_almacen

    estado = oci_almacen.estado()
    assert estado["habilitado"] is True
    assert estado["conectado"] is True
    assert estado["namespace"] == "tecnoteca-local"

    origen = Path("models/modelo.joblib")
    assert oci_almacen.subir_modelo(origen) is True

    destino = tmp_path / "descargado.joblib"
    assert oci_almacen.descargar_modelo(destino) is True
    assert destino.read_bytes() == origen.read_bytes()


def test_descarga_de_objeto_inexistente_devuelve_false(puerto_emulador, tmp_path, monkeypatch):
    monkeypatch.setenv("OCI_ENABLED", "true")
    monkeypatch.setenv("OCI_AUTH", "local")
    monkeypatch.setenv("OCI_ENDPOINT", f"http://127.0.0.1:{puerto_emulador}")
    monkeypatch.setenv("OCI_BUCKET", "bucket-vacio")
    monkeypatch.setenv("OCI_OBJETO_MODELO", "no/existe.joblib")
    monkeypatch.setenv("OCI_DIR_LOCAL", str(tmp_path / "oci"))

    from servicio_modelo import oci_almacen

    assert oci_almacen.descargar_modelo(tmp_path / "nada.joblib") is False
