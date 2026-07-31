# Integración con OCI Object Storage: registro de modelos.
# - Al entrenar, el artefacto se sube al bucket.
# - Al arrancar el servicio, si el modelo no existe localmente se descarga.
#
# Modos de autenticación (variable OCI_AUTH):
#   local              → firma con una clave desechable contra el EMULADOR local
#                        de Object Storage (OCI_ENDPOINT, lo levanta run.bash).
#                        Es el modo por defecto de run.bash: el código del SDK
#                        oficial se ejecuta completo, sin necesitar tenancy.
#   config             → archivo ~/.oci/config (OCI_CONFIG_FILE / OCI_PROFILE),
#                        para usar el Object Storage real de tu tenancy.
#   instance_principal → desde una instancia de OCI Compute, sin archivo.
#
# Con OCI_ENABLED=false todo queda en disco local y /salud lo reporta.
import logging
import os
from pathlib import Path

log = logging.getLogger("tecnoteca.oci")

_OCIDS_LOCALES = {
    "user": "ocid1.user.oc1..aaaaaaaalocallocallocallocallocallocallocallocallocal",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaalocallocallocallocallocallocallocallocal",
    "fingerprint": "aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99",
    "region": "us-ashburn-1",
}


def habilitado() -> bool:
    return os.getenv("OCI_ENABLED", "").lower() in {"1", "true", "si", "sí", "yes"}


def _bucket() -> str:
    return os.getenv("OCI_BUCKET", "tecnoteca-artefactos")


def _objeto_modelo() -> str:
    return os.getenv("OCI_OBJETO_MODELO", "modelos/modelo.joblib")


def _modo_auth() -> str:
    return os.getenv("OCI_AUTH", "config")


def _endpoint() -> str | None:
    return os.getenv("OCI_ENDPOINT") or None


def _config_local() -> dict:
    """Configuración desechable (clave RSA generada al vuelo) para firmar las
    peticiones del SDK contra el emulador local, que no valida firmas."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    directorio = Path(os.getenv("OCI_DIR_LOCAL", "data/oci_local"))
    directorio.mkdir(parents=True, exist_ok=True)
    ruta_clave = directorio / "clave_api.pem"
    if not ruta_clave.exists():
        privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        ruta_clave.write_bytes(privada.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()))
    return {**_OCIDS_LOCALES, "key_file": str(ruta_clave)}


def _cliente():
    import oci  # importación tardía: solo cuando la integración se usa

    extras: dict = {"timeout": (3, 60)}
    endpoint = _endpoint()
    if endpoint:
        extras["service_endpoint"] = endpoint

    modo = _modo_auth()
    if modo == "local":
        if not endpoint:
            raise RuntimeError("OCI_AUTH=local requiere OCI_ENDPOINT "
                               "(el emulador que levanta run.bash)")
        cliente = oci.object_storage.ObjectStorageClient(_config_local(), **extras)
    elif modo == "instance_principal":
        firmante = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        cliente = oci.object_storage.ObjectStorageClient(config={}, signer=firmante, **extras)
    else:
        ruta = os.getenv("OCI_CONFIG_FILE", oci.config.DEFAULT_LOCATION)
        perfil = os.getenv("OCI_PROFILE", "DEFAULT")
        cliente = oci.object_storage.ObjectStorageClient(
            oci.config.from_file(ruta, perfil), **extras)

    import oci.retry
    espacio = cliente.get_namespace(retry_strategy=oci.retry.NoneRetryStrategy()).data
    return cliente, espacio


def estado() -> dict:
    if not habilitado():
        return {"habilitado": False,
                "detalle": "Deshabilitado. Exporta OCI_ENABLED=true (run.bash lo hace por defecto)."}
    base = {"habilitado": True, "auth": _modo_auth(), "bucket": _bucket(),
            "objeto_modelo": _objeto_modelo()}
    if _endpoint():
        base["endpoint"] = _endpoint()
    try:
        _, espacio = _cliente()
        return {**base, "namespace": espacio, "conectado": True}
    except Exception as e:  # sin conexión/credenciales: seguimos en modo local
        return {**base, "conectado": False, "error": f"No fue posible conectar: {e}"}


def subir_modelo(origen: str | Path) -> bool:
    """Sube el artefacto del modelo al bucket. Devuelve True si se subió."""
    if not habilitado():
        log.info("OCI deshabilitado: el modelo queda solo en disco local.")
        return False
    try:
        cliente, espacio = _cliente()
        with open(origen, "rb") as f:
            cliente.put_object(espacio, _bucket(), _objeto_modelo(), f)
        destino = _endpoint() or "OCI Object Storage"
        log.info("Modelo subido a %s → %s/%s", destino, _bucket(), _objeto_modelo())
        print(f"OCI: modelo subido al bucket '{_bucket()}' como '{_objeto_modelo()}' "
              f"({'emulador local' if _modo_auth() == 'local' else 'Object Storage'})")
        return True
    except Exception as e:
        log.warning("No se pudo subir el modelo a OCI (%s). Continuamos en local.", e)
        print(f"OCI: no se pudo subir el modelo ({e}). El artefacto queda en local.")
        return False


def descargar_modelo(destino: str | Path) -> bool:
    """Descarga el artefacto del bucket al disco. Devuelve True si lo logró."""
    if not habilitado():
        return False
    try:
        cliente, espacio = _cliente()
        respuesta = cliente.get_object(espacio, _bucket(), _objeto_modelo())
        destino = Path(destino)
        destino.parent.mkdir(parents=True, exist_ok=True)
        with open(destino, "wb") as f:
            for trozo in respuesta.data.raw.stream(1024 * 1024, decode_content=False):
                f.write(trozo)
        log.info("Modelo descargado desde OCI Object Storage a %s", destino)
        return True
    except Exception as e:
        log.warning("No se pudo descargar el modelo desde OCI: %s", e)
        return False
