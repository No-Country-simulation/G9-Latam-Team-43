# Pruebas automatizadas del servicio de modelo (FastAPI + modelo entrenado real).
import pytest
from fastapi.testclient import TestClient

from servicio_modelo.main import app

EJEMPLO_SPEC = {
    "titulo": "Introducción a Spring Boot",
    "texto": "En este contenido se presentan los conceptos básicos para la creación "
             "de APIs REST utilizando Java y Spring Boot.",
}


@pytest.fixture(scope="module")
def cliente():
    with TestClient(app) as c:  # el contexto dispara el ciclo de vida (carga el modelo)
        yield c


def test_salud_reporta_modelo_cargado(cliente):
    r = cliente.get("/salud")
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["modelo_cargado"] is True
    assert "Backend" in cuerpo["categorias"]
    assert "habilitado" in cuerpo["oci"]  # el estado OCI siempre se reporta


def test_analizar_ejemplo_del_enunciado(cliente):
    r = cliente.post("/analizar", json=EJEMPLO_SPEC)
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["categoria"] == "Backend"
    assert 0 < cuerpo["probabilidad"] <= 1
    assert "Spring Boot" in cuerpo["palabras_clave"]
    assert "Java" in cuerpo["palabras_clave"]
    assert cuerpo["explicacion"], "debe explicar qué términos pesaron"
    assert "tema" in cuerpo


def test_analizar_contenido_de_datos(cliente):
    r = cliente.post("/analizar", json={
        "titulo": "Clasificación de textos",
        "texto": "Entrenamos una regresión logística sobre vectores TF-IDF con "
                 "scikit-learn y evaluamos con validación cruzada y matriz de confusión.",
    })
    assert r.status_code == 200
    assert r.json()["categoria"] == "Ciencia de Datos"


def test_validacion_texto_muy_corto(cliente):
    r = cliente.post("/analizar", json={"titulo": "Hola", "texto": "corto"})
    assert r.status_code == 422
    assert r.json()["error"] == "Entrada inválida"
    assert any(d["campo"] == "texto" for d in r.json()["detalles"])


def test_validacion_falta_campo(cliente):
    r = cliente.post("/analizar", json={"titulo": "Sin texto"})
    assert r.status_code == 422


def test_flujo_indexar_similares_buscar(cliente):
    documentos = [
        {"id": 1, "titulo": "Curso de Spring Boot",
         "texto": "Creación de APIs REST con Java y Spring Boot, validación y JPA.",
         "categoria": "Backend"},
        {"id": 2, "titulo": "Análisis con pandas",
         "texto": "Limpieza de datos y análisis exploratorio con pandas y matplotlib.",
         "categoria": "Ciencia de Datos"},
        {"id": 3, "titulo": "Docker desde cero",
         "texto": "Contenedores, imágenes y despliegue de aplicaciones con Docker.",
         "categoria": "DevOps"},
    ]
    r = cliente.post("/reindexar", json={"documentos": documentos})
    assert r.status_code == 200 and r.json()["indexados"] == 3

    r = cliente.post("/indexar", json={
        "id": 4, "titulo": "JPA e Hibernate",
        "texto": "Persistencia de datos en Java con JPA e Hibernate y sus relaciones.",
        "categoria": "Backend"})
    assert r.status_code == 200 and r.json()["total"] == 4

    r = cliente.post("/similares", json={
        "texto": "APIs REST con Java y Spring Boot", "k": 2, "excluir_id": 1})
    ids = [x["id"] for x in r.json()["resultados"]]
    assert 1 not in ids and len(ids) >= 1

    r = cliente.post("/buscar", json={"consulta": "pandas análisis de datos", "k": 3})
    resultados = r.json()["resultados"]
    assert resultados and resultados[0]["id"] == 2

    r = cliente.post("/buscar", json={"consulta": "java spring", "k": 5,
                                      "categoria": "Backend"})
    assert all(x["id"] in {1, 4} for x in r.json()["resultados"])


def test_buscar_consulta_invalida(cliente):
    r = cliente.post("/buscar", json={"consulta": "a"})
    assert r.status_code == 422
