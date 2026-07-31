# Generador del dataset propio del equipo (requisito del hackathon: cada equipo
# construye su propia base de contenidos). Componemos descripciones de cursos,
# tutoriales, apuntes y documentación en español a partir de un catálogo de
# temas por categoría y plantillas de redacción, con semilla fija para que el
# dataset sea reproducible.
import csv
import random
from pathlib import Path

from ciencia_datos.datos_evaluacion import EVALUACION_MANUAL

SEMILLA = 42
POR_CATEGORIA = 150
RAIZ = Path(__file__).resolve().parent.parent
DIR_DATOS = RAIZ / "data"

TIPOS = ["curso", "tutorial", "artículo", "guía", "apunte de estudio", "taller",
         "video", "material de referencia", "módulo de la formación", "webinar"]

PUBLICOS = ["principiantes", "estudiantes de la formación", "desarrolladores junior",
            "equipos técnicos", "profesionales que cambian de área", "autodidactas"]

PLANTILLAS_TEXTO = [
    "En este {tipo} se presentan los conceptos básicos de {frase}, utilizando {tecs}.",
    "{Tipo} orientado a {publico} donde aprenderás a {accion} con {tecs}. {detalle}",
    "Apuntes de estudio sobre {frase}. {detalle}",
    "Guía práctica: cómo {accion} paso a paso usando {tecs}. Pensada para {publico}.",
    "Material de referencia sobre {frase}. Explica cómo {accion} y {accion2}, con ejemplos de {tecs}.",
    "Resumen de la clase sobre {frase}: vimos cómo {accion} y repasamos {tecs}. {detalle}",
    "Este {tipo} explica {frase} desde cero: {accion}, {accion2} y ejercicios con {tecs}.",
    "Documentación interna del equipo sobre {frase}. {detalle} Herramientas utilizadas: {tecs}.",
    "Notas rápidas sobre {frase}: lo esencial para {accion} utilizando {tecs}.",
    "{Tipo} avanzado sobre {frase} para {publico}: aprenderás a {accion2} con {tecs}. {detalle}",
    "Tutorial en el que se muestra cómo {accion}; se utiliza {tecs} y se comentan errores comunes.",
    "Transcripción de la charla sobre {frase}: por qué importa, cómo {accion} y una demo con {tecs}.",
    "Contenido del {tipo} de {nombre}: {detalle} Incluye ejercicios resueltos con {tecs}.",
]

PLANTILLAS_TITULO = [
    "Introducción a {nombre}",
    "{nombre} desde cero",
    "Curso de {nombre}",
    "Guía completa de {nombre}",
    "Buenas prácticas de {nombre}",
    "Taller práctico: {nombre}",
    "{nombre} para {publico}",
    "Apuntes de {nombre}",
    "Cómo dominar {nombre}",
    "{nombre}: conceptos clave",
]

# Catálogo: cada tema tiene un nombre corto (para títulos), una frase (para la
# prosa), tecnologías asociadas, acciones (infinitivos) y detalles opcionales.
CATALOGO: dict[str, list[dict]] = {
    "Backend": [
        {"nombre": "APIs REST con Spring Boot", "frase": "la creación de APIs REST",
         "tecs": ["Java", "Spring Boot", "API REST"],
         "acciones": ["crear endpoints", "validar peticiones", "manejar errores HTTP", "documentar rutas"],
         "detalles": ["Se cubren verbos HTTP, códigos de estado y diseño de rutas.",
                      "Incluye validación de entrada y manejo global de excepciones."]},
        {"nombre": "Node.js y Express", "frase": "el desarrollo de servidores con Node.js",
         "tecs": ["Node.js", "Express", "JavaScript"],
         "acciones": ["configurar middleware", "definir rutas", "conectar una base de datos"],
         "detalles": ["Se explica el event loop y el manejo asíncrono con promesas."]},
        {"nombre": "autenticación con JWT", "frase": "la autenticación y autorización en APIs",
         "tecs": ["JWT", "OAuth2", "Spring Security"],
         "acciones": ["emitir y validar tokens", "proteger rutas", "manejar sesiones sin estado"],
         "detalles": ["Se comparan sesiones tradicionales y tokens firmados."]},
        {"nombre": "microservicios", "frase": "la arquitectura de microservicios",
         "tecs": ["Java", "Spring Cloud", "RabbitMQ"],
         "acciones": ["dividir un monolito", "comunicar servicios", "manejar fallos parciales"],
         "detalles": ["Se discuten límites de contexto y consistencia eventual."]},
        {"nombre": "persistencia con JPA e Hibernate", "frase": "la persistencia de datos en Java",
         "tecs": ["JPA", "Hibernate", "Java"],
         "acciones": ["mapear entidades", "definir relaciones", "optimizar consultas"],
         "detalles": ["Se explican los problemas de carga perezosa y el N+1."]},
        {"nombre": "Django", "frase": "el desarrollo web con Django",
         "tecs": ["Python", "Django", "ORM"],
         "acciones": ["definir modelos", "crear vistas", "usar el admin"],
         "detalles": ["Incluye el sistema de migraciones y plantillas."]},
        {"nombre": "FastAPI", "frase": "la construcción de APIs con FastAPI",
         "tecs": ["Python", "FastAPI", "API REST"],
         "acciones": ["tipar los esquemas", "validar automáticamente", "generar documentación"],
         "detalles": ["La documentación interactiva se genera sola con OpenAPI."]},
        {"nombre": "pruebas unitarias en el backend", "frase": "las pruebas automatizadas del backend",
         "tecs": ["JUnit", "Mockito", "Java"],
         "acciones": ["aislar dependencias", "probar servicios", "medir cobertura"],
         "detalles": ["Se aplican dobles de prueba y aserciones expresivas."]},
        {"nombre": "GraphQL", "frase": "el diseño de APIs con GraphQL",
         "tecs": ["GraphQL", "Node.js"],
         "acciones": ["definir esquemas", "resolver consultas", "evitar sobrecarga de datos"],
         "detalles": ["Se compara con REST y se discute cuándo conviene cada uno."]},
        {"nombre": "mensajería con Kafka", "frase": "la mensajería asíncrona entre servicios",
         "tecs": ["Apache Kafka", "Java"],
         "acciones": ["publicar eventos", "consumir tópicos", "garantizar el orden"],
         "detalles": ["Se revisan particiones, offsets y grupos de consumidores."]},
        {"nombre": "el patrón MVC", "frase": "el patrón modelo-vista-controlador",
         "tecs": ["MVC", "Java", "Spring"],
         "acciones": ["separar responsabilidades", "organizar el proyecto"],
         "detalles": ["Se muestra cómo crece un proyecto bien estructurado."]},
        {"nombre": "documentación con Swagger", "frase": "la documentación de APIs",
         "tecs": ["Swagger/OpenAPI", "API REST"],
         "acciones": ["describir endpoints", "publicar la documentación", "probar desde el navegador"],
         "detalles": ["La especificación OpenAPI se convierte en un contrato del equipo."]},
        {"nombre": "WebSockets", "frase": "la comunicación en tiempo real",
         "tecs": ["WebSockets", "Node.js"],
         "acciones": ["abrir canales bidireccionales", "notificar eventos en vivo"],
         "detalles": ["Ejemplo con un chat y actualizaciones de estado en vivo."]},
    ],
    "Frontend": [
        {"nombre": "React", "frase": "el desarrollo de interfaces con React",
         "tecs": ["React", "JavaScript"],
         "acciones": ["crear componentes", "manejar el estado", "usar hooks"],
         "detalles": ["Se explica el renderizado declarativo y las props."]},
        {"nombre": "hooks de React", "frase": "los hooks de React",
         "tecs": ["React", "TypeScript"],
         "acciones": ["usar useState y useEffect", "crear custom hooks", "memorizar cálculos"],
         "detalles": ["Se muestran errores típicos con dependencias de efectos."]},
        {"nombre": "Angular", "frase": "el desarrollo de aplicaciones con Angular",
         "tecs": ["Angular", "TypeScript"],
         "acciones": ["crear componentes y servicios", "inyectar dependencias", "manejar formularios"],
         "detalles": ["Incluye formularios reactivos y validadores personalizados."]},
        {"nombre": "CSS moderno", "frase": "la maquetación con CSS moderno",
         "tecs": ["CSS", "Flexbox", "CSS Grid"],
         "acciones": ["construir layouts", "alinear componentes", "crear diseños fluidos"],
         "detalles": ["Grid para el layout general y Flexbox para los detalles."]},
        {"nombre": "diseño responsive", "frase": "el diseño adaptable a distintos dispositivos",
         "tecs": ["CSS", "Diseño Responsive", "HTML"],
         "acciones": ["usar media queries", "definir puntos de quiebre", "probar en móviles"],
         "detalles": ["Se parte del enfoque mobile first."]},
        {"nombre": "JavaScript moderno", "frase": "las novedades de JavaScript",
         "tecs": ["JavaScript", "HTML"],
         "acciones": ["usar funciones flecha", "desestructurar objetos", "trabajar con promesas"],
         "detalles": ["Repaso de async/await y módulos."]},
        {"nombre": "TypeScript en el frontend", "frase": "el tipado estático en el frontend",
         "tecs": ["TypeScript", "React"],
         "acciones": ["tipar props y estados", "definir interfaces", "atrapar errores en compilación"],
         "detalles": ["Los tipos documentan el código y evitan bugs silenciosos."]},
        {"nombre": "accesibilidad web", "frase": "la accesibilidad de las interfaces",
         "tecs": ["Accesibilidad", "HTML"],
         "acciones": ["usar HTML semántico", "navegar con teclado", "probar con lector de pantalla"],
         "detalles": ["Checklist basado en las pautas WCAG."]},
        {"nombre": "estado global con Redux", "frase": "el manejo de estado global",
         "tecs": ["Redux", "React"],
         "acciones": ["definir slices", "despachar acciones", "conectar componentes"],
         "detalles": ["Cuándo conviene estado global y cuándo estado local."]},
        {"nombre": "Vue", "frase": "el desarrollo progresivo con Vue",
         "tecs": ["Vue", "JavaScript"],
         "acciones": ["crear componentes de un solo archivo", "reaccionar a cambios de datos"],
         "detalles": ["Se presenta la reactividad y las directivas de plantilla."]},
        {"nombre": "rendimiento web", "frase": "la optimización del rendimiento web",
         "tecs": ["Lighthouse", "Vite", "JavaScript"],
         "acciones": ["medir métricas web", "dividir bundles", "cargar rutas bajo demanda"],
         "detalles": ["Se optimizan imágenes y se mide el impacto en la carga."]},
        {"nombre": "consumo de APIs desde el navegador", "frase": "el consumo de APIs desde el frontend",
         "tecs": ["JavaScript", "API REST"],
         "acciones": ["hacer peticiones con fetch", "manejar errores de red", "mostrar estados de carga"],
         "detalles": ["Se cubren promesas encadenadas y cancelación de peticiones."]},
        {"nombre": "Tailwind CSS", "frase": "los estilos con clases utilitarias",
         "tecs": ["Tailwind CSS", "CSS"],
         "acciones": ["componer estilos", "mantener consistencia visual", "personalizar el tema"],
         "detalles": ["Se compara con hojas de estilo tradicionales."]},
    ],
    "Ciencia de Datos": [
        {"nombre": "pandas", "frase": "el análisis de datos con pandas",
         "tecs": ["Python", "Pandas"],
         "acciones": ["cargar datasets", "limpiar valores nulos", "agrupar y agregar"],
         "detalles": ["Se trabaja con un dataset real con datos sucios."]},
        {"nombre": "análisis exploratorio de datos", "frase": "el análisis exploratorio de datos",
         "tecs": ["EDA", "Pandas", "Matplotlib"],
         "acciones": ["describir variables", "detectar valores atípicos", "visualizar distribuciones"],
         "detalles": ["El EDA guía las decisiones de modelado posteriores."]},
        {"nombre": "clasificación con scikit-learn", "frase": "los modelos de clasificación",
         "tecs": ["scikit-learn", "Python", "Regresión Logística"],
         "acciones": ["entrenar un clasificador", "evaluar con métricas", "evitar el sobreajuste"],
         "detalles": ["Incluye la matriz de confusión y la validación cruzada."]},
        {"nombre": "TF-IDF y texto", "frase": "la vectorización de texto con TF-IDF",
         "tecs": ["TF-IDF", "NLP", "scikit-learn"],
         "acciones": ["tokenizar documentos", "ponderar términos", "clasificar textos"],
         "detalles": ["Se explica por qué las palabras raras pesan más."]},
        {"nombre": "clustering con K-Means", "frase": "el agrupamiento no supervisado",
         "tecs": ["K-Means", "scikit-learn"],
         "acciones": ["elegir el número de clusters", "interpretar centroides", "medir la silueta"],
         "detalles": ["Método del codo y coeficiente de silueta paso a paso."]},
        {"nombre": "visualización de datos", "frase": "la visualización de datos",
         "tecs": ["Matplotlib", "Seaborn", "Python"],
         "acciones": ["elegir el gráfico adecuado", "anotar hallazgos", "comunicar resultados"],
         "detalles": ["Buenas prácticas para gráficos que no engañan."]},
        {"nombre": "redes neuronales", "frase": "las redes neuronales",
         "tecs": ["TensorFlow", "Keras", "Deep Learning"],
         "acciones": ["definir capas", "entrenar por épocas", "regularizar el modelo"],
         "detalles": ["Se monitorea el sobreajuste con curvas de entrenamiento."]},
        {"nombre": "procesamiento de lenguaje natural", "frase": "el procesamiento de lenguaje natural",
         "tecs": ["NLP", "spaCy", "Python"],
         "acciones": ["lematizar texto", "extraer entidades", "medir similitud entre documentos"],
         "detalles": ["Del texto crudo a representaciones que un modelo entiende."]},
        {"nombre": "métricas de evaluación", "frase": "las métricas de evaluación de modelos",
         "tecs": ["scikit-learn", "Machine Learning"],
         "acciones": ["interpretar precision y recall", "elegir la métrica según el problema"],
         "detalles": ["Con clases desbalanceadas el accuracy no basta."]},
        {"nombre": "ingeniería de características", "frase": "la ingeniería de características",
         "tecs": ["Pandas", "scikit-learn"],
         "acciones": ["crear variables derivadas", "codificar categóricas", "escalar numéricas"],
         "detalles": ["Las buenas variables valen más que un modelo complejo."]},
        {"nombre": "series de tiempo", "frase": "el análisis de series de tiempo",
         "tecs": ["Series de Tiempo", "Pandas", "Python"],
         "acciones": ["descomponer tendencia y estacionalidad", "pronosticar valores futuros"],
         "detalles": ["Se valida con ventanas temporales, no con mezcla aleatoria."]},
        {"nombre": "validación cruzada", "frase": "la validación de modelos",
         "tecs": ["Validación Cruzada", "scikit-learn"],
         "acciones": ["particionar los datos", "estimar el error real", "comparar modelos"],
         "detalles": ["Evitamos la fuga de datos entre entrenamiento y prueba."]},
        {"nombre": "notebooks reproducibles", "frase": "el trabajo reproducible en notebooks",
         "tecs": ["Jupyter", "Python"],
         "acciones": ["ordenar las celdas", "fijar semillas", "serializar modelos"],
         "detalles": ["Un notebook que otro pueda ejecutar de principio a fin."]},
    ],
    "DevOps": [
        {"nombre": "Docker", "frase": "la contenedorización de aplicaciones",
         "tecs": ["Docker", "Linux"],
         "acciones": ["escribir un Dockerfile", "construir imágenes", "publicar en un registro"],
         "detalles": ["Capas, caché de build e imágenes livianas."]},
        {"nombre": "Kubernetes", "frase": "la orquestación de contenedores",
         "tecs": ["Kubernetes", "Docker"],
         "acciones": ["desplegar pods", "escalar réplicas", "exponer servicios"],
         "detalles": ["Deployments, services e ingress con manifiestos YAML."]},
        {"nombre": "integración continua", "frase": "la integración y entrega continua",
         "tecs": ["CI/CD", "GitHub Actions"],
         "acciones": ["automatizar pruebas", "construir en cada push", "desplegar a producción"],
         "detalles": ["Workflows con caché de dependencias y secretos."]},
        {"nombre": "Terraform", "frase": "la infraestructura como código",
         "tecs": ["Terraform", "Infraestructura como Código"],
         "acciones": ["declarar recursos", "planificar cambios", "versionar la infraestructura"],
         "detalles": ["El estado remoto evita conflictos entre miembros del equipo."]},
        {"nombre": "monitoreo y alertas", "frase": "el monitoreo de aplicaciones",
         "tecs": ["Prometheus", "Grafana"],
         "acciones": ["exponer métricas", "crear tableros", "definir alertas"],
         "detalles": ["Latencia, errores y saturación como señales básicas."]},
        {"nombre": "logs centralizados", "frase": "la gestión centralizada de logs",
         "tecs": ["ELK", "Docker"],
         "acciones": ["estructurar los logs", "correlacionar peticiones", "buscar incidentes"],
         "detalles": ["Formato JSON y correlación por id de petición."]},
        {"nombre": "administración de Linux", "frase": "la administración de servidores Linux",
         "tecs": ["Linux", "Bash"],
         "acciones": ["gestionar servicios", "programar tareas", "revisar permisos"],
         "detalles": ["systemd, cron y usuarios sin privilegios innecesarios."]},
        {"nombre": "scripts de automatización", "frase": "la automatización con scripts",
         "tecs": ["Bash", "Linux"],
         "acciones": ["encadenar comandos", "manejar errores en scripts", "parametrizar tareas"],
         "detalles": ["Pequeños scripts que ahorran horas de trabajo manual."]},
        {"nombre": "Ansible", "frase": "la configuración automatizada de servidores",
         "tecs": ["Ansible", "Linux"],
         "acciones": ["escribir playbooks", "aplicar cambios idempotentes", "gestionar inventarios"],
         "detalles": ["La misma configuración aplicada a decenas de máquinas."]},
        {"nombre": "Nginx", "frase": "los servidores web y proxies inversos",
         "tecs": ["Nginx", "Linux"],
         "acciones": ["configurar un proxy inverso", "servir contenido estático", "balancear carga"],
         "detalles": ["Terminación TLS y compresión de respuestas."]},
        {"nombre": "estrategias de despliegue", "frase": "las estrategias de despliegue",
         "tecs": ["CI/CD", "Kubernetes"],
         "acciones": ["desplegar sin caídas", "hacer rollback rápido", "liberar por etapas"],
         "detalles": ["Blue-green y canary con ejemplos concretos."]},
        {"nombre": "Jenkins", "frase": "los pipelines de construcción",
         "tecs": ["Jenkins", "CI/CD"],
         "acciones": ["definir etapas", "paralelizar trabajos", "publicar artefactos"],
         "detalles": ["Pipelines declarativos versionados junto al código."]},
    ],
    "Bases de Datos": [
        {"nombre": "SQL", "frase": "las consultas SQL",
         "tecs": ["SQL", "PostgreSQL"],
         "acciones": ["escribir consultas con JOIN", "agrupar resultados", "filtrar con subconsultas"],
         "detalles": ["De consultas simples a agregaciones complejas."]},
        {"nombre": "modelado relacional", "frase": "el modelado de datos relacional",
         "tecs": ["SQL", "Normalización"],
         "acciones": ["diseñar tablas", "definir claves", "normalizar el esquema"],
         "detalles": ["Formas normales explicadas con un caso de inventario."]},
        {"nombre": "índices y rendimiento", "frase": "la optimización de consultas",
         "tecs": ["PostgreSQL", "SQL"],
         "acciones": ["leer planes de ejecución", "crear índices adecuados", "detectar consultas lentas"],
         "detalles": ["Cada índice acelera lecturas y encarece escrituras."]},
        {"nombre": "MongoDB", "frase": "las bases de datos de documentos",
         "tecs": ["MongoDB", "NoSQL"],
         "acciones": ["modelar documentos", "decidir entre embeber y referenciar", "consultar colecciones"],
         "detalles": ["El modelo se diseña según los patrones de acceso."]},
        {"nombre": "Redis", "frase": "el caché en memoria",
         "tecs": ["Redis", "NoSQL"],
         "acciones": ["cachear consultas frecuentes", "definir expiraciones", "invalidar al escribir"],
         "detalles": ["Patrones cache-aside y trampas como la estampida de caché."]},
        {"nombre": "transacciones", "frase": "las transacciones y el aislamiento",
         "tecs": ["SQL", "Transacciones ACID"],
         "acciones": ["agrupar operaciones", "elegir el nivel de aislamiento", "evitar lecturas sucias"],
         "detalles": ["Ejemplos de anomalías y cómo prevenirlas."]},
        {"nombre": "PL/SQL y Oracle", "frase": "la programación en la base de datos",
         "tecs": ["PL/SQL", "Oracle Database"],
         "acciones": ["escribir procedimientos almacenados", "recorrer cursores", "programar jobs"],
         "detalles": ["Lógica cercana a los datos para procesos por lotes."]},
        {"nombre": "migraciones de esquema", "frase": "las migraciones de bases de datos",
         "tecs": ["Flyway", "SQL"],
         "acciones": ["versionar el esquema", "aplicar cambios en orden", "migrar sin downtime"],
         "detalles": ["Cada cambio es un script numerado y revisado."]},
        {"nombre": "MySQL", "frase": "la administración de MySQL",
         "tecs": ["MySQL", "SQL"],
         "acciones": ["configurar réplicas", "hacer respaldos", "restaurar a un punto en el tiempo"],
         "detalles": ["Respaldos probados: un respaldo sin prueba no existe."]},
        {"nombre": "SQL vs NoSQL", "frase": "la elección entre SQL y NoSQL",
         "tecs": ["SQL", "NoSQL", "MongoDB"],
         "acciones": ["comparar modelos de datos", "evaluar consistencia", "elegir según el caso"],
         "detalles": ["No hay bala de plata: depende del patrón de acceso."]},
        {"nombre": "SQLite embebida", "frase": "las bases de datos embebidas",
         "tecs": ["SQLite", "SQL"],
         "acciones": ["persistir datos locales", "consultar sin servidor"],
         "detalles": ["Ideal para prototipos, pruebas y aplicaciones locales."]},
        {"nombre": "particionamiento", "frase": "el particionamiento y la réplica",
         "tecs": ["PostgreSQL", "SQL"],
         "acciones": ["particionar tablas grandes", "distribuir lecturas", "planificar el crecimiento"],
         "detalles": ["Particiones por fecha para históricos que no dejan de crecer."]},
    ],
    "Seguridad": [
        {"nombre": "OWASP Top 10", "frase": "las vulnerabilidades web más comunes",
         "tecs": ["OWASP", "HTTPS/TLS"],
         "acciones": ["identificar riesgos", "priorizar mitigaciones", "revisar aplicaciones"],
         "detalles": ["Un recorrido con ejemplos reproducibles en laboratorio autorizado."]},
        {"nombre": "prevención de inyección SQL", "frase": "la prevención de inyección SQL",
         "tecs": ["Inyección SQL", "SQL", "ORM"],
         "acciones": ["usar consultas parametrizadas", "validar la entrada", "probar los formularios"],
         "detalles": ["El clásico error de concatenar texto del usuario en la consulta."]},
        {"nombre": "XSS y CSRF", "frase": "los ataques del lado del cliente",
         "tecs": ["XSS", "CSRF"],
         "acciones": ["escapar la salida", "configurar cabeceras de seguridad", "usar tokens anti falsificación"],
         "detalles": ["Cómo un script inyectado roba sesiones y cómo evitarlo."]},
        {"nombre": "almacenamiento de contraseñas", "frase": "el almacenamiento seguro de contraseñas",
         "tecs": ["bcrypt", "Hashing"],
         "acciones": ["aplicar hash con salt", "elegir el factor de costo", "diseñar la recuperación de cuenta"],
         "detalles": ["Nunca texto plano, nunca algoritmos rápidos."]},
        {"nombre": "HTTPS y certificados", "frase": "el cifrado en tránsito",
         "tecs": ["HTTPS/TLS", "Criptografía"],
         "acciones": ["emitir certificados", "forzar HTTPS", "configurar HSTS"],
         "detalles": ["Qué garantiza TLS y qué queda fuera de su alcance."]},
        {"nombre": "gestión de secretos", "frase": "la gestión de secretos y credenciales",
         "tecs": ["Vault", "CI/CD"],
         "acciones": ["sacar las claves del código", "rotar credenciales", "auditar accesos"],
         "detalles": ["Las claves de API no viven en el repositorio."]},
        {"nombre": "autenticación multifactor", "frase": "la autenticación multifactor",
         "tecs": ["MFA", "OAuth2"],
         "acciones": ["añadir un segundo factor", "balancear seguridad y usabilidad"],
         "detalles": ["Códigos temporales, llaves físicas y códigos de respaldo."]},
        {"nombre": "criptografía aplicada", "frase": "la criptografía aplicada",
         "tecs": ["Criptografía", "Hashing"],
         "acciones": ["cifrar datos en reposo", "firmar mensajes", "elegir algoritmos vigentes"],
         "detalles": ["Simétrico frente a asimétrico explicado sin fórmulas."]},
        {"nombre": "análisis de vulnerabilidades", "frase": "el análisis de vulnerabilidades",
         "tecs": ["Pentesting", "OWASP"],
         "acciones": ["escanear dependencias", "reportar hallazgos", "verificar correcciones"],
         "detalles": ["Auditorías periódicas dentro de un programa autorizado."]},
        {"nombre": "cabeceras de seguridad", "frase": "las cabeceras de seguridad HTTP",
         "tecs": ["HTTPS/TLS", "XSS"],
         "acciones": ["configurar CSP", "limitar orígenes", "endurecer las respuestas"],
         "detalles": ["Pequeños cambios de configuración con gran impacto."]},
        {"nombre": "mínimo privilegio", "frase": "el principio de mínimo privilegio",
         "tecs": ["IAM", "Linux"],
         "acciones": ["acotar permisos", "separar roles", "auditar accesos"],
         "detalles": ["Cada servicio con exactamente los permisos que necesita."]},
        {"nombre": "seguridad en el ciclo de desarrollo", "frase": "la seguridad desde el diseño",
         "tecs": ["OWASP", "CI/CD"],
         "acciones": ["revisar código con foco en seguridad", "automatizar análisis", "modelar amenazas"],
         "detalles": ["La seguridad entra al pipeline, no llega al final."]},
    ],
    "Móvil": [
        {"nombre": "Android con Kotlin", "frase": "el desarrollo Android",
         "tecs": ["Android", "Kotlin"],
         "acciones": ["crear pantallas", "manejar el ciclo de vida", "conservar el estado"],
         "detalles": ["Activities, fragments y ViewModel explicados con una app real."]},
        {"nombre": "Jetpack Compose", "frase": "las interfaces declarativas en Android",
         "tecs": ["Jetpack Compose", "Kotlin"],
         "acciones": ["componer funciones de interfaz", "reaccionar a cambios de estado"],
         "detalles": ["Menos XML, más funciones componibles."]},
        {"nombre": "iOS con Swift", "frase": "el desarrollo iOS",
         "tecs": ["iOS", "Swift", "SwiftUI"],
         "acciones": ["construir vistas", "consumir APIs", "decodificar JSON con Codable"],
         "detalles": ["Estados de carga y error manejados de forma explícita."]},
        {"nombre": "Flutter", "frase": "el desarrollo multiplataforma con Flutter",
         "tecs": ["Flutter", "Dart"],
         "acciones": ["componer widgets", "manejar el estado", "compilar para ambas tiendas"],
         "detalles": ["Un solo código para Android e iOS."]},
        {"nombre": "React Native", "frase": "las aplicaciones móviles con React Native",
         "tecs": ["React Native", "JavaScript"],
         "acciones": ["reutilizar componentes", "acceder a APIs nativas", "depurar en el dispositivo"],
         "detalles": ["El puente entre JavaScript y el mundo nativo."]},
        {"nombre": "persistencia móvil", "frase": "la persistencia local en el móvil",
         "tecs": ["SQLite", "Room", "Android"],
         "acciones": ["guardar datos sin conexión", "definir entidades", "migrar el esquema"],
         "detalles": ["La app sigue funcionando aunque no haya red."]},
        {"nombre": "notificaciones push", "frase": "las notificaciones push",
         "tecs": ["Firebase", "Android"],
         "acciones": ["registrar dispositivos", "enviar mensajes segmentados", "pedir permisos"],
         "detalles": ["Notificar sin ser invasivo: canales y frecuencia."]},
        {"nombre": "publicación en tiendas", "frase": "la publicación de aplicaciones",
         "tecs": ["Android", "iOS"],
         "acciones": ["firmar la aplicación", "preparar la ficha de la tienda", "pasar la revisión"],
         "detalles": ["Del build firmado a la aprobación en la tienda."]},
        {"nombre": "consumo de APIs en móvil", "frase": "el consumo de APIs desde el móvil",
         "tecs": ["API REST", "Kotlin"],
         "acciones": ["hacer peticiones", "cachear respuestas", "manejar la falta de conexión"],
         "detalles": ["Reintentos con espera exponencial y modo sin conexión."]},
        {"nombre": "diseño para móviles", "frase": "el diseño de interfaces móviles",
         "tecs": ["Android", "iOS"],
         "acciones": ["seguir guías de diseño", "adaptar a distintos tamaños", "cuidar los gestos"],
         "detalles": ["Material Design y las guías de interfaz humanas comparadas."]},
        {"nombre": "pruebas en móvil", "frase": "las pruebas de aplicaciones móviles",
         "tecs": ["Android", "JUnit"],
         "acciones": ["probar la interfaz", "automatizar flujos", "correr en emuladores"],
         "detalles": ["Pruebas de interfaz estables sin esperas frágiles."]},
    ],
    "Cloud": [
        {"nombre": "Object Storage en OCI", "frase": "el almacenamiento de objetos en la nube",
         "tecs": ["Oracle Cloud (OCI)", "Object Storage"],
         "acciones": ["crear buckets", "subir y versionar objetos", "generar URLs prefirmadas"],
         "detalles": ["Políticas de acceso y ciclo de vida de los objetos."]},
        {"nombre": "OCI Compute", "frase": "las máquinas virtuales en la nube",
         "tecs": ["OCI Compute", "Oracle Cloud (OCI)", "Linux"],
         "acciones": ["crear una instancia", "configurar la red", "desplegar una aplicación"],
         "detalles": ["De cero a una aplicación pública en una VM."]},
        {"nombre": "redes en la nube", "frase": "las redes virtuales en la nube",
         "tecs": ["VCN", "Oracle Cloud (OCI)"],
         "acciones": ["diseñar subredes", "abrir puertos con listas de seguridad", "aislar entornos"],
         "detalles": ["Subredes públicas y privadas bien separadas."]},
        {"nombre": "serverless", "frase": "las funciones serverless",
         "tecs": ["Serverless", "Python"],
         "acciones": ["desplegar funciones", "reaccionar a eventos", "controlar el costo"],
         "detalles": ["Arranque en frío y límites de ejecución a considerar."]},
        {"nombre": "IAM y permisos", "frase": "la gestión de identidades en la nube",
         "tecs": ["IAM", "Oracle Cloud (OCI)"],
         "acciones": ["crear grupos y políticas", "aplicar mínimo privilegio", "auditar el acceso"],
         "detalles": ["Compartimentos para ordenar recursos y permisos."]},
        {"nombre": "costos en la nube", "frase": "la optimización de costos",
         "tecs": ["Oracle Cloud (OCI)", "AWS"],
         "acciones": ["etiquetar recursos", "apagar entornos ociosos", "configurar presupuestos"],
         "detalles": ["Alertas antes de que la factura sorprenda."]},
        {"nombre": "alta disponibilidad", "frase": "la alta disponibilidad",
         "tecs": ["Alta Disponibilidad", "Balanceador de Carga"],
         "acciones": ["repartir tráfico", "replicar datos", "probar la recuperación"],
         "detalles": ["Diseñar asumiendo que algo va a fallar."]},
        {"nombre": "bases de datos gestionadas", "frase": "las bases de datos gestionadas",
         "tecs": ["Oracle Database", "Oracle Cloud (OCI)"],
         "acciones": ["aprovisionar la base", "configurar respaldos automáticos", "escalar según demanda"],
         "detalles": ["La base autónoma se ajusta y parcha sola."]},
        {"nombre": "colas y eventos", "frase": "la mensajería en la nube",
         "tecs": ["Serverless", "Apache Kafka"],
         "acciones": ["desacoplar servicios", "procesar eventos", "absorber picos de carga"],
         "detalles": ["Las colas amortiguan los picos de tráfico."]},
        {"nombre": "CDN y contenido estático", "frase": "la distribución de contenido",
         "tecs": ["CDN", "Cloud"],
         "acciones": ["cachear en el borde", "reducir latencia", "invalidar contenido"],
         "detalles": ["El contenido cerca del usuario, el origen tranquilo."]},
        {"nombre": "migración a la nube", "frase": "la migración de aplicaciones a la nube",
         "tecs": ["Oracle Cloud (OCI)", "Docker"],
         "acciones": ["evaluar dependencias", "elegir la estrategia", "migrar por etapas"],
         "detalles": ["Rehospedar, replataformar o rediseñar: costos y riesgos."]},
    ],
}

COLETILLAS = [
    "Incluye ejercicios prácticos y material complementario.",
    "Al final hay un proyecto integrador para aplicar lo aprendido.",
    "Cada sección cierra con preguntas de repaso.",
    "Se recomienda tener nociones básicas de programación.",
    "El código de los ejemplos está disponible en el repositorio del curso.",
    "",
    "",
    "",
]


def _generar_documento(rng: random.Random, categoria: str) -> tuple[str, str]:
    tema = rng.choice(CATALOGO[categoria])
    tipo = rng.choice(TIPOS)
    publico = rng.choice(PUBLICOS)
    acciones = rng.sample(tema["acciones"], k=min(2, len(tema["acciones"])))
    tecs_muestra = rng.sample(tema["tecs"], k=min(len(tema["tecs"]), rng.choice([2, 2, 3])))
    tecs = tecs_muestra[0] if len(tecs_muestra) == 1 else (
        ", ".join(tecs_muestra[:-1]) + " y " + tecs_muestra[-1])
    plantilla = rng.choice(PLANTILLAS_TEXTO)
    texto = plantilla.format(
        tipo=tipo, Tipo=tipo.capitalize(), frase=tema["frase"], nombre=tema["nombre"],
        tecs=tecs, publico=publico, accion=acciones[0],
        accion2=acciones[-1], detalle=rng.choice(tema["detalles"]),
    )
    coletilla = rng.choice(COLETILLAS)
    if coletilla:
        texto = f"{texto} {coletilla}"
    titulo = rng.choice(PLANTILLAS_TITULO).format(nombre=tema["nombre"], publico=publico)
    return titulo, " ".join(texto.split())


def generar(por_categoria: int = POR_CATEGORIA, semilla: int = SEMILLA) -> list[dict]:
    rng = random.Random(semilla)
    documentos, vistos = [], set()
    for categoria in CATALOGO:
        generados, intentos = 0, 0
        while generados < por_categoria and intentos < por_categoria * 40:
            intentos += 1
            titulo, texto = _generar_documento(rng, categoria)
            if texto in vistos:
                continue
            vistos.add(texto)
            documentos.append({"titulo": titulo, "texto": texto, "categoria": categoria})
            generados += 1
    rng.shuffle(documentos)
    return documentos


def _escribir_csv(ruta: Path, filas: list[dict], campos: list[str]) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def main() -> None:
    DIR_DATOS.mkdir(exist_ok=True)
    documentos = generar()
    _escribir_csv(DIR_DATOS / "contenidos.csv", documentos, ["titulo", "texto", "categoria"])

    manual = [{"titulo": t, "texto": x, "categoria": c} for t, x, c in EVALUACION_MANUAL]
    _escribir_csv(DIR_DATOS / "evaluacion_manual.csv", manual, ["titulo", "texto", "categoria"])

    # Semilla de la base de conocimiento: los ejemplos manuales + una muestra
    # del corpus generado, para que la aplicación arranque con contenido útil.
    rng = random.Random(SEMILLA)
    semilla_kb = [{"titulo": d["titulo"], "texto": d["texto"]} for d in manual]
    por_cat: dict[str, list[dict]] = {}
    for d in documentos:
        por_cat.setdefault(d["categoria"], []).append(d)
    for docs in por_cat.values():
        for d in rng.sample(docs, k=min(12, len(docs))):
            semilla_kb.append({"titulo": d["titulo"], "texto": d["texto"]})
    _escribir_csv(DIR_DATOS / "semilla_kb.csv", semilla_kb, ["titulo", "texto"])

    conteo: dict[str, int] = {}
    for d in documentos:
        conteo[d["categoria"]] = conteo.get(d["categoria"], 0) + 1
    print(f"Dataset generado: {len(documentos)} documentos en {DIR_DATOS/'contenidos.csv'}")
    for categoria, n in sorted(conteo.items()):
        print(f"  {categoria:<16} {n}")
    print(f"Evaluación manual: {len(manual)} documentos")
    print(f"Semilla de la base de conocimiento: {len(semilla_kb)} documentos")


if __name__ == "__main__":
    main()
