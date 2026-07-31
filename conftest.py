# Configuración de pytest: garantiza que el dataset y el modelo existan antes
# de correr las pruebas del servicio de modelo.
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))


def pytest_configure(config):
    if not (RAIZ / "data" / "contenidos.csv").exists():
        subprocess.run([sys.executable, "-m", "ciencia_datos.generar_dataset"],
                       cwd=RAIZ, check=True)
    if not (RAIZ / "models" / "modelo.joblib").exists():
        subprocess.run([sys.executable, "-m", "ciencia_datos.entrenar"],
                       cwd=RAIZ, check=True)
