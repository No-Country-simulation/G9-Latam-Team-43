import requests
import pandas as pd
import time
from tqdm import tqdm

OUTPUT_FILE = "Base_Contenido_1000_Registros_Reales.xlsx"

BASE_URL = "https://openlibrary.org/search.json"

REGISTROS_OBJETIVO = 1000

campos = [
    "titulo",
    "autores",
    "editorial",
    "isbn",
    "anio_publicacion",
    "descripcion",
    "idioma",
    "materias",
    "url_openlibrary"
]

registros = []
vistos = set()

querys = [
    "python",
    "java",
    "data science",
    "machine learning",
    "power bi",
    "cloud computing",
    "cybersecurity",
    "sql",
    "artificial intelligence",
    "software architecture",
    "devops",
    "spring boot",
    "azure",
    "aws",
    "kubernetes",
    "docker",
    "statistics",
    "big data",
    "analytics"
]

def obtener_descripcion(work_key):
    try:
        url = f"https://openlibrary.org{work_key}.json"
        r = requests.get(url, timeout=20)

        if r.status_code != 200:
            return ""

        data = r.json()

        descripcion = data.get("description")

        if isinstance(descripcion, dict):
            return descripcion.get("value", "")

        if isinstance(descripcion, str):
            return descripcion

        return ""

    except Exception:
        return ""


for consulta in querys:

    page = 1

    while len(registros) < REGISTROS_OBJETIVO:

        params = {
            "q": consulta,
            "page": page,
            "limit": 100
        }

        response = requests.get(BASE_URL, params=params, timeout=30)

        if response.status_code != 200:
            break

        resultado = response.json()

        docs = resultado.get("docs", [])

        if not docs:
            break

        for libro in tqdm(docs, desc=f"{consulta} página {page}"):

            if len(registros) >= REGISTROS_OBJETIVO:
                break

            titulo = libro.get("title")

            if not titulo:
                continue

            clave_unica = (
                titulo,
                str(libro.get("first_publish_year"))
            )

            if clave_unica in vistos:
                continue

            vistos.add(clave_unica)

            autores = "; ".join(
                libro.get("author_name", [])
            )

            editorial = "; ".join(
                libro.get("publisher", [])[:3]
            )

            isbn = ""

            if libro.get("isbn"):
                isbn = libro["isbn"][0]

            materias = ""

            if libro.get("subject"):
                materias = "; ".join(
                    libro["subject"][:10]
                )

            idioma = ""

            if libro.get("language"):
                idioma = "; ".join(
                    libro["language"][:5]
                )

            descripcion = ""

            if libro.get("key"):
                descripcion = obtener_descripcion(
                    libro["key"]
                )

            registros.append({
                "titulo": titulo,
                "autores": autores,
                "editorial": editorial,
                "isbn": isbn,
                "anio_publicacion":
                    libro.get("first_publish_year"),
                "descripcion": descripcion,
                "idioma": idioma,
                "materias": materias,
                "url_openlibrary":
                    f"https://openlibrary.org{libro.get('key', '')}"
            })

        page += 1

        time.sleep(1)

        if page > 50:
            break

df = pd.DataFrame(registros)

df.to_excel(
    OUTPUT_FILE,
    index=False
)

print(
    f"Archivo generado: {OUTPUT_FILE}"
)
print(
    f"Registros obtenidos: {len(df)}"
)
