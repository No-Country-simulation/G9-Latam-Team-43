#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════
#  Tecnoteca · Hackathon ONE G9 (Alura + Oracle)
#  Orquestador del proyecto: prepara el entorno, genera el dataset, entrena
#  el modelo, corre las pruebas, construye la API Java y levanta todo
#  (incluido un emulador local de OCI Object Storage, activo por defecto).
# ══════════════════════════════════════════════════════════════════════════
set -euo pipefail
cd "$(dirname "$0")"

PUERTO_API="${PUERTO_API:-8080}"
PUERTO_MODELO="${PUERTO_MODELO:-8001}"
PUERTO_OCI="${PUERTO_OCI:-8021}"
PYTHON_BIN="${PYTHON:-python3}"
VENV=".venv"
JAR="api/target/tecnoteca-api-1.0.0.jar"
mkdir -p logs

# ── Integración OCI: activa por defecto contra el emulador local ──────────
# Para usar el Object Storage REAL de tu tenancy:
#   OCI_AUTH=config ./run.bash            (usa ~/.oci/config; no definas OCI_ENDPOINT)
#   OCI_AUTH=instance_principal ...       (desde una instancia de OCI Compute)
# Para desactivar la integración por completo: OCI_ENABLED=false ./run.bash
export OCI_ENABLED="${OCI_ENABLED:-true}"
export OCI_BUCKET="${OCI_BUCKET:-tecnoteca-artefactos}"
if [ "$OCI_ENABLED" = "true" ] && [ -z "${OCI_AUTH:-}" ] && [ -z "${OCI_ENDPOINT:-}" ]; then
    export OCI_AUTH="local"
    export OCI_ENDPOINT="http://localhost:$PUERTO_OCI"
fi

# ── CPUs x86-64 antiguas (sin SSE4.2): kernels BLAS portables ─────────────
# La autodetección de OpenBLAS puede elegir kernels con instrucciones que la
# CPU no tiene (típico en VMs qemu64/kvm64) y el proceso muere con
# "Illegal instruction"; PRESCOTT (SSE3) funciona en cualquier x86-64.
if [ -z "${OPENBLAS_CORETYPE:-}" ] && grep -qs '^flags' /proc/cpuinfo \
        && ! { grep -m1 '^flags' /proc/cpuinfo | grep -qw sse4_2; }; then
    export OPENBLAS_CORETYPE=PRESCOTT
fi

PID_MODELO=""
PID_API=""
PID_OCI=""

azul()  { printf '\n\033[1;36m▸ %s\033[0m\n' "$*"; }
ok()    { printf '\033[1;32m✔ %s\033[0m\n' "$*"; }
fallo() { printf '\033[1;31m✘ %s\033[0m\n' "$*" >&2; }

uso() {
    cat <<'FIN'
Uso: ./run.bash [comando]
  todo        (por defecto) configurar → datos → emulador OCI → entrenar →
              probar → construir → levantar servicios → demo
  configurar  entorno de Python (uv si está instalado, si no venv+pip)
  datos       genera el dataset propio del equipo (CSV)
  entrenar    entrena, serializa el modelo (joblib) y lo sube a OCI
  probar      pruebas de Python (pytest, incluye la integración OCI local)
  probar-java pruebas de la API Java (mvn test)
  construir   empaqueta la API Java (mvn package)
  servir      levanta emulador OCI (8021), modelo (8001) y API Java (8080)
  demo        igual que servir + ejecuta los ejemplos de uso
  notebook    ejecuta el notebook de ciencia de datos de punta a punta
  limpiar     borra entorno, artefactos y datos generados

Variables: PUERTO_API, PUERTO_MODELO, PUERTO_OCI, PYTHON,
           OCI_ENABLED / OCI_AUTH / OCI_ENDPOINT / OCI_BUCKET (ver README)
FIN
}

# ── Descubrimiento de JDK 17+ (brew, java_home o PATH) ────────────────────
version_java() { "$1" -version 2>&1 | awk -F'"' '/version/ {print $2}' | cut -d. -f1; }

buscar_java() {
    candidatos=""
    [ -n "${JAVA_HOME:-}" ] && candidatos="$JAVA_HOME"
    for prefijo in openjdk@21 openjdk@17 openjdk; do
        ruta="$(brew --prefix "$prefijo" 2>/dev/null || true)"
        [ -n "$ruta" ] && candidatos="$candidatos $ruta"
    done
    ruta="$(/usr/libexec/java_home 2>/dev/null || true)"
    [ -n "$ruta" ] && candidatos="$candidatos $ruta"
    for c in $candidatos; do
        for bin in "$c/bin/java" "$c/libexec/openjdk.jdk/Contents/Home/bin/java"; do
            if [ -x "$bin" ]; then
                v="$(version_java "$bin")"
                if [ "${v:-0}" -ge 17 ] 2>/dev/null; then
                    JAVA_HOME="${bin%/bin/java}"
                    export JAVA_HOME
                    export PATH="$JAVA_HOME/bin:$PATH"
                    return 0
                fi
            fi
        done
    done
    if command -v java >/dev/null 2>&1; then
        v="$(version_java java)"
        [ "${v:-0}" -ge 17 ] 2>/dev/null && return 0
    fi
    return 1
}

requisitos_python() {
    command -v "$PYTHON_BIN" >/dev/null 2>&1 \
        || { fallo "No se encontró $PYTHON_BIN (se necesita Python 3.10+)."; exit 1; }
    command -v curl >/dev/null 2>&1 || { fallo "Se necesita curl."; exit 1; }
}

requisitos_java() {
    if ! buscar_java; then
        fallo "Se necesita un JDK 17 o superior para la API Java."
        echo "    macOS:  brew install openjdk@21"
        echo "    Ubuntu: sudo apt install openjdk-21-jdk"
        exit 1
    fi
    if ! command -v mvn >/dev/null 2>&1; then
        fallo "Se necesita Maven."
        echo "    macOS:  brew install maven"
        echo "    Ubuntu: sudo apt install maven"
        exit 1
    fi
}

# ── Etapas ────────────────────────────────────────────────────────────────
instalar_deps() {  # $1 = archivo de requisitos
    if command -v uv >/dev/null 2>&1; then
        uv pip install -q -r "$1" --python "$VENV/bin/python"
    else
        "$VENV/bin/pip" install -q -r "$1"
    fi
}

configurar() {
    azul "Preparando entorno de Python"
    if [ ! -d "$VENV" ]; then
        if command -v uv >/dev/null 2>&1; then
            uv venv "$VENV" >/dev/null
        else
            "$PYTHON_BIN" -m venv "$VENV"
            "$VENV/bin/pip" install -q --upgrade pip
        fi
    fi
    instalar_deps requirements.txt
    if command -v uv >/dev/null 2>&1; then
        ok "Dependencias de Python instaladas (con uv)"
    else
        ok "Dependencias de Python instaladas (con pip; instala 'uv' para acelerar)"
    fi
}

asegurar_venv() {
    [ -x "$VENV/bin/python" ] || configurar
}

datos() {
    asegurar_venv
    azul "Generando el dataset propio del equipo"
    "$VENV/bin/python" -m ciencia_datos.generar_dataset
}

entrenar() {
    asegurar_venv
    [ -f data/contenidos.csv ] || datos
    azul "Entrenando el modelo (TF-IDF + Regresión Logística + K-Means)"
    "$VENV/bin/python" -m ciencia_datos.entrenar
}

probar() {
    asegurar_venv
    azul "Pruebas de Python (servicio de modelo + integración OCI local)"
    "$VENV/bin/python" -m pytest pruebas -q
    ok "Pruebas de Python en verde"
}

probar_java() {
    requisitos_java
    azul "Pruebas de la API Java"
    (cd api && mvn -q test)
    ok "Pruebas de Java en verde"
}

construir() {
    requisitos_java
    azul "Empaquetando la API Java (Maven)"
    (cd api && mvn -q -DskipTests package)
    ok "Jar generado: $JAR"
}

# ── Servicios ─────────────────────────────────────────────────────────────
puerto_libre() {
    if lsof -ti tcp:"$1" -sTCP:LISTEN >/dev/null 2>&1; then
        fallo "El puerto $1 ($2) ya está en uso."
        echo "    Cambia el puerto: PUERTO_API=8090 PUERTO_MODELO=8011 PUERTO_OCI=8022 ./run.bash $comando"
        exit 1
    fi
}

esperar_url() {
    url="$1"; intentos="${2:-60}"
    i=0
    while [ "$i" -lt "$intentos" ]; do
        curl -sf "$url" >/dev/null 2>&1 && return 0
        sleep 1
        i=$((i + 1))
    done
    return 1
}

limpiar_procesos() {
    [ -n "$PID_API" ] && kill "$PID_API" 2>/dev/null || true
    [ -n "$PID_MODELO" ] && kill "$PID_MODELO" 2>/dev/null || true
    [ -n "$PID_OCI" ] && kill "$PID_OCI" 2>/dev/null || true
}

arrancar_oci_local() {
    [ "${OCI_AUTH:-}" = "local" ] || return 0
    asegurar_venv
    # si ya hay un emulador escuchando (p. ej. de otra terminal), lo reutilizamos
    if lsof -ti tcp:"$PUERTO_OCI" -sTCP:LISTEN >/dev/null 2>&1; then
        return 0
    fi
    azul "Levantando el emulador local de OCI Object Storage (puerto $PUERTO_OCI)"
    trap 'limpiar_procesos' INT TERM EXIT
    "$VENV/bin/uvicorn" servicio_modelo.oci_emulador:app --host 127.0.0.1 \
        --port "$PUERTO_OCI" >logs/oci.log 2>&1 &
    PID_OCI=$!
    esperar_url "http://localhost:$PUERTO_OCI/" 20 || {
        fallo "El emulador de OCI no arrancó. Últimas líneas de logs/oci.log:"
        tail -20 logs/oci.log; exit 1; }
    ok "Emulador OCI listo → bucket '$OCI_BUCKET' en $OCI_ENDPOINT"
}

servicios() {
    asegurar_venv
    [ -f models/modelo.joblib ] || { fallo "No hay modelo entrenado. Ejecuta: ./run.bash entrenar"; exit 1; }
    [ -f "$JAR" ] || { fallo "No hay jar de la API. Ejecuta: ./run.bash construir"; exit 1; }
    puerto_libre "$PUERTO_MODELO" "servicio de modelo"
    puerto_libre "$PUERTO_API" "API Java"
    trap 'limpiar_procesos' INT TERM EXIT
    arrancar_oci_local

    azul "Levantando el servicio de modelo en el puerto $PUERTO_MODELO"
    "$VENV/bin/uvicorn" servicio_modelo.main:app --host 0.0.0.0 \
        --port "$PUERTO_MODELO" >logs/modelo.log 2>&1 &
    PID_MODELO=$!
    esperar_url "http://localhost:$PUERTO_MODELO/salud" 30 || {
        fallo "El servicio de modelo no arrancó. Últimas líneas de logs/modelo.log:"
        tail -20 logs/modelo.log; exit 1; }
    ok "Servicio de modelo listo → http://localhost:$PUERTO_MODELO/docs"

    azul "Levantando la API Java en el puerto $PUERTO_API"
    MODELO_URL="http://localhost:$PUERTO_MODELO" PUERTO_API="$PUERTO_API" \
        java -jar "$JAR" >logs/api.log 2>&1 &
    PID_API=$!
    esperar_url "http://localhost:$PUERTO_API/salud" 90 || {
        fallo "La API Java no arrancó. Últimas líneas de logs/api.log:"
        tail -30 logs/api.log; exit 1; }
    ok "API Java lista → http://localhost:$PUERTO_API"

    # Si hay semilla, esperamos a que la base de conocimiento tenga contenido
    if [ -f data/semilla_kb.csv ]; then
        azul "Esperando la carga de la semilla en la base de conocimiento"
        anterior=-1; n=0; i=0
        while [ "$i" -lt 120 ]; do
            n="$(curl -sf "http://localhost:$PUERTO_API/salud" \
                | "$VENV/bin/python" -c 'import json,sys; print(json.load(sys.stdin).get("contenidos",0))' \
                2>/dev/null || echo 0)"
            # listo cuando hay contenidos y el conteo dejó de crecer
            if [ "${n:-0}" -gt 0 ] && [ "$n" = "$anterior" ]; then
                break
            fi
            anterior="$n"
            sleep 2
            i=$((i + 1))
        done
        ok "Base de conocimiento con $n contenidos"
    fi
}

demo() {
    azul "Ejemplos de uso contra la API"
    bash ejemplos/ejecutar_ejemplos.sh "$PUERTO_API"
}

en_marcha() {
    printf '\n\033[1;35m════════════════════════════════════════════════════════════\033[0m\n'
    printf '  Interfaz web     →  http://localhost:%s\n' "$PUERTO_API"
    printf '  Swagger (Java)   →  http://localhost:%s/swagger-ui.html\n' "$PUERTO_API"
    printf '  Docs del modelo  →  http://localhost:%s/docs\n' "$PUERTO_MODELO"
    printf '  Salud            →  http://localhost:%s/salud\n' "$PUERTO_API"
    if [ "${OCI_AUTH:-}" = "local" ]; then
        printf '  OCI (emulador)   →  %s  (bucket %s)\n' "$OCI_ENDPOINT" "$OCI_BUCKET"
    fi
    printf '\n  Ctrl+C para detener los servicios.\n'
    printf '\033[1;35m════════════════════════════════════════════════════════════\033[0m\n'
    wait "$PID_MODELO" "$PID_API"
}

notebook() {
    asegurar_venv
    azul "Instalando dependencias del notebook y ejecutándolo de punta a punta"
    instalar_deps requirements-notebook.txt
    "$VENV/bin/jupyter" nbconvert --to notebook --execute --inplace \
        ciencia_datos/notebook_ciencia_de_datos.ipynb
    ok "Notebook ejecutado: ciencia_datos/notebook_ciencia_de_datos.ipynb"
}

limpiar() {
    azul "Limpiando artefactos generados"
    rm -rf "$VENV" api/target logs data models .pytest_cache
    find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
    ok "Proyecto limpio (los fuentes quedan intactos)"
}

# ── Comando principal ─────────────────────────────────────────────────────
comando="${1:-todo}"
case "$comando" in
    todo)
        requisitos_python; requisitos_java
        configurar; datos; arrancar_oci_local; entrenar; probar; construir
        servicios; demo; en_marcha ;;
    configurar)  requisitos_python; configurar ;;
    datos)       requisitos_python; datos ;;
    entrenar)    requisitos_python; arrancar_oci_local; entrenar ;;
    probar)      requisitos_python; probar ;;
    probar-java) probar_java ;;
    construir)   construir ;;
    servir)      requisitos_python; requisitos_java; servicios; en_marcha ;;
    demo)        requisitos_python; requisitos_java; servicios; demo; en_marcha ;;
    notebook)    requisitos_python; notebook ;;
    limpiar)     limpiar ;;
    ayuda|-h|--help) uso ;;
    *)
        fallo "Comando desconocido: $comando"
        uso
        exit 1 ;;
esac
