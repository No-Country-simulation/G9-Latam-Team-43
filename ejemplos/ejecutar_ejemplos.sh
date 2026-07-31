#!/usr/bin/env bash
# Ejecuta los ejemplos de uso contra la API pública de Tecnoteca.
# Uso: bash ejemplos/ejecutar_ejemplos.sh [puerto]   (por defecto 8080)
set -euo pipefail
cd "$(dirname "$0")"

PUERTO="${1:-8080}"
BASE="http://localhost:$PUERTO"
PY="../.venv/bin/python"
[ -x "$PY" ] || PY="python3"

bonito() { "$PY" -m json.tool --no-ensure-ascii 2>/dev/null || cat; }

for archivo in ejemplo_*.json; do
    printf '\n\033[1;36m── POST /contenido  ←  %s ──\033[0m\n' "$archivo"
    cat "$archivo"
    printf '\033[1;33m→ Respuesta:\033[0m\n'
    curl -sf -X POST "$BASE/contenido" \
        -H "Content-Type: application/json" -d @"$archivo" | bonito
done

printf '\n\033[1;36m── GET /buscar?q=autenticación con tokens en una api ──\033[0m\n'
curl -sf --get "$BASE/buscar" \
    --data-urlencode "q=autenticación con tokens en una api" \
    --data-urlencode "k=3" | bonito

printf '\n\033[1;36m── GET /categorias ──\033[0m\n'
curl -sf "$BASE/categorias" | bonito

printf '\n\033[1;36m── GET /contenidos/1/relacionados ──\033[0m\n'
curl -sf "$BASE/contenidos/1/relacionados" | bonito

printf '\n\033[1;36m── Validación: texto demasiado corto (error esperado) ──\033[0m\n'
curl -s -X POST "$BASE/contenido" -H "Content-Type: application/json" \
    -d '{"titulo": "Hola", "texto": "corto"}' | bonito

if [ "${OCI_AUTH:-}" = "local" ] && [ -n "${OCI_ENDPOINT:-}" ]; then
    NS="${OCI_NAMESPACE_LOCAL:-tecnoteca-local}"
    CUBETA="${OCI_BUCKET:-tecnoteca-artefactos}"
    printf '\n\033[1;36m── OCI Object Storage (emulador local): objetos del bucket %s ──\033[0m\n' "$CUBETA"
    curl -sf "$OCI_ENDPOINT/n/$NS/b/$CUBETA/o" | bonito
fi
