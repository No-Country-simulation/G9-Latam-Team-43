# Conjunto de evaluación escrito A MANO por el equipo (no proviene de las
# plantillas del generador). Sirve para medir la generalización real del modelo
# sobre redacciones distintas a las del dataset de entrenamiento.
# Formato: (titulo, texto, categoria)

EVALUACION_MANUAL = [
    # ── Backend ────────────────────────────────────────────────────────────
    ("Arquitectura hexagonal en la práctica",
     "Notas sobre cómo separar el dominio de la infraestructura usando puertos y adaptadores. "
     "Se implementa un caso de uso con Spring Boot, inyección de dependencias y pruebas unitarias "
     "con JUnit y Mockito para la capa de servicio.", "Backend"),
    ("Manejo global de excepciones en una API",
     "Cuando un endpoint lanza un error queremos devolver un JSON consistente con el código de "
     "estado correcto. Con RestControllerAdvice centralizamos el manejo de errores, validamos la "
     "entrada con Bean Validation y registramos los fallos en el log.", "Backend"),
    ("Autenticación con JWT paso a paso",
     "El tutorial muestra cómo generar y validar tokens JWT en un backend con Node.js y Express, "
     "proteger rutas con middleware y refrescar tokens expirados sin obligar al usuario a iniciar "
     "sesión de nuevo.", "Backend"),
    ("Del monolito a microservicios",
     "Apunte sobre cuándo conviene dividir un monolito: límites de contexto, comunicación entre "
     "servicios con colas de mensajes como RabbitMQ, y los problemas de consistencia eventual que "
     "aparecen al repartir los datos.", "Backend"),
    ("Documentar una API con OpenAPI",
     "Guía corta para describir endpoints, parámetros y respuestas con Swagger y OpenAPI, generar "
     "la documentación interactiva y mantenerla sincronizada con el código del backend en cada "
     "despliegue.", "Backend"),
    ("Paginación y filtrado eficientes",
     "Cómo diseñar endpoints REST que devuelven listas grandes: paginación por cursor frente a "
     "offset, filtros por parámetros de consulta y ordenamiento estable, con ejemplos en FastAPI "
     "y Python.", "Backend"),

    # ── Frontend ───────────────────────────────────────────────────────────
    ("Hooks de React que uso a diario",
     "Resumen personal de useState, useEffect y useMemo con ejemplos reales: sincronizar "
     "formularios, evitar renders innecesarios y extraer lógica repetida a custom hooks en una "
     "aplicación de React con TypeScript.", "Frontend"),
    ("Maquetación con CSS Grid y Flexbox",
     "Comparativa práctica: cuándo usar Grid para el layout general de la página y Flexbox para "
     "alinear componentes internos. Incluye trucos de diseño responsive con media queries y "
     "unidades relativas.", "Frontend"),
    ("Accesibilidad web sin excusas",
     "Checklist para que una interfaz cumpla WCAG: contraste suficiente, navegación por teclado, "
     "etiquetas aria y HTML semántico. Probamos la página con un lector de pantalla y corregimos "
     "los errores encontrados.", "Frontend"),
    ("Estado global con Redux Toolkit",
     "Apuntes del curso: slices, reducers y acciones asíncronas con createAsyncThunk. Cuándo "
     "conviene estado global y cuándo basta con el estado local de un componente de React.", "Frontend"),
    ("Optimizar el rendimiento de una SPA",
     "Medimos el tiempo de carga con Lighthouse y aplicamos lazy loading de rutas, división de "
     "bundles con Vite y compresión de imágenes para mejorar las métricas web vitales de la "
     "aplicación.", "Frontend"),
    ("Formularios en Angular con validación",
     "Cómo construir formularios reactivos en Angular: FormGroup, validadores personalizados y "
     "mensajes de error accesibles, mostrando el estado del campo mientras el usuario escribe.", "Frontend"),

    # ── Ciencia de Datos ───────────────────────────────────────────────────
    ("Limpieza de un dataset real con pandas",
     "El dataset traía fechas en tres formatos, nulos disfrazados de cadenas vacías y duplicados. "
     "Documento el proceso de limpieza con pandas: normalizar tipos, imputar valores faltantes y "
     "validar rangos antes del análisis.", "Ciencia de Datos"),
    ("Mi primer clasificador de texto",
     "Entrené una regresión logística sobre vectores TF-IDF para etiquetar tickets de soporte. "
     "Explico el preprocesamiento del texto, la validación cruzada y cómo interpretar la matriz "
     "de confusión del modelo.", "Ciencia de Datos"),
    ("Clustering de clientes con K-Means",
     "Agrupamos clientes por comportamiento de compra usando K-Means y scikit-learn. Elegimos el "
     "número de clusters con el método del codo y el coeficiente de silueta, y describimos cada "
     "segmento resultante.", "Ciencia de Datos"),
    ("Visualización efectiva con matplotlib",
     "Buenas prácticas para gráficos que comunican: elegir el tipo de gráfico según la variable, "
     "evitar el exceso de tinta y anotar los hallazgos. Ejemplos con matplotlib y seaborn sobre "
     "datos de ventas.", "Ciencia de Datos"),
    ("Redes neuronales para imágenes",
     "Introducción a las redes convolucionales con PyTorch: capas de convolución, pooling y "
     "regularización con dropout. Entrenamos un modelo pequeño para clasificar imágenes y "
     "monitoreamos el sobreajuste.", "Ciencia de Datos"),
    ("Métricas más allá del accuracy",
     "Cuando las clases están desbalanceadas el accuracy engaña: precision, recall, F1 y la curva "
     "ROC cuentan la historia completa. Ejemplos numéricos y cómo elegir la métrica según el costo "
     "de cada error.", "Ciencia de Datos"),

    # ── DevOps ─────────────────────────────────────────────────────────────
    ("Mi pipeline de CI/CD con GitHub Actions",
     "Cada push ejecuta linters, pruebas y construye la imagen de Docker; si la rama es main, "
     "despliega automáticamente. Explico los workflows, los secretos y el caché de dependencias "
     "para acelerar el pipeline.", "DevOps"),
    ("Kubernetes para impacientes",
     "Lo mínimo para desplegar una aplicación: pods, deployments, services e ingress. Aplicamos "
     "manifiestos con kubectl, escalamos réplicas y hacemos un rollout sin tiempo de caída.", "DevOps"),
    ("Infraestructura como código con Terraform",
     "Definimos la red, las instancias y el almacenamiento en archivos declarativos, versionados "
     "en Git. El plan muestra los cambios antes de aplicarlos y el estado remoto evita conflictos "
     "en el equipo.", "DevOps"),
    ("Monitoreo con Prometheus y Grafana",
     "Instrumentamos la aplicación con métricas de latencia y errores, las recolectamos con "
     "Prometheus y armamos tableros en Grafana con alertas cuando el percentil 95 supera el "
     "umbral acordado.", "DevOps"),
    ("Logs centralizados que sí se leen",
     "Enviamos los logs de todos los contenedores a un stack ELK, con formato JSON estructurado y "
     "correlación por id de petición, para depurar incidentes de producción sin entrar servidor "
     "por servidor.", "DevOps"),
    ("Automatizar servidores con Ansible",
     "Escribimos playbooks idempotentes para instalar paquetes, copiar configuraciones y reiniciar "
     "servicios en decenas de máquinas Linux a la vez, con inventarios por entorno y variables por "
     "grupo.", "DevOps"),

    # ── Bases de Datos ─────────────────────────────────────────────────────
    ("Índices que aceleran y los que estorban",
     "Analizamos planes de ejecución en PostgreSQL para decidir qué índices crear: por qué un "
     "índice compuesto sirve para unas consultas y no para otras, y el costo que pagan las "
     "escrituras por cada índice extra.", "Bases de Datos"),
    ("Transacciones y niveles de aislamiento",
     "Ejemplos concretos de lecturas sucias, no repetibles y fantasma. Cómo elegir el nivel de "
     "aislamiento en SQL y cuándo usar bloqueos optimistas frente a pesimistas en la base de "
     "datos.", "Bases de Datos"),
    ("Modelado de datos en MongoDB",
     "Documentos embebidos o referencias: decidimos según los patrones de acceso. Diseñamos las "
     "colecciones de un carrito de compras y comparamos las consultas resultantes con un modelo "
     "relacional.", "Bases de Datos"),
    ("Migraciones de esquema sin sustos",
     "Usamos Flyway para versionar el esquema: cada cambio es un script SQL numerado que se aplica "
     "en orden. Estrategias para migrar columnas con datos en producción sin bloquear la tabla.", "Bases de Datos"),
    ("Caché con Redis: patrones y trampas",
     "Cache-aside con expiración, invalidación al escribir y qué hacer con la estampida de caché. "
     "Medimos el impacto en la latencia de las consultas más frecuentes del sistema.", "Bases de Datos"),
    ("PL/SQL para tareas programadas",
     "Procedimientos almacenados en Oracle Database que consolidan ventas cada noche: cursores, "
     "manejo de excepciones y jobs del planificador, con registro de cada corrida en una tabla de "
     "auditoría.", "Bases de Datos"),

    # ── Seguridad ──────────────────────────────────────────────────────────
    ("Así evitamos la inyección SQL",
     "Repaso del ataque clásico: concatenar entrada del usuario en la consulta. Lo corregimos con "
     "consultas parametrizadas y un ORM, añadimos validación de entrada y pruebas que intentan "
     "explotar el fallo.", "Seguridad"),
    ("XSS y CSRF explicados con ejemplos",
     "Cómo un script inyectado roba cookies de sesión y cómo un formulario falso dispara acciones "
     "en nombre de la víctima. Mitigaciones: escapar la salida, cabeceras de seguridad y tokens "
     "anti CSRF.", "Seguridad"),
    ("Guardar contraseñas como corresponde",
     "Nunca en texto plano: usamos bcrypt con factor de costo adecuado, salt por usuario y "
     "política de rotación. También cubrimos el flujo seguro de recuperación de contraseña por "
     "correo.", "Seguridad"),
    ("HTTPS de punta a punta",
     "Qué garantiza TLS y qué no: emitimos certificados con Let's Encrypt, forzamos la redirección "
     "a HTTPS, configuramos HSTS y verificamos la cadena de certificados en el balanceador.", "Seguridad"),
    ("Gestión de secretos en el equipo",
     "Las claves de API no van al repositorio: las movimos a un gestor de secretos con Vault, "
     "rotación automática y permisos por rol, y auditamos quién accede a cada credencial.", "Seguridad"),
    ("Primeros pasos con el OWASP Top 10",
     "Recorremos las vulnerabilidades más comunes en aplicaciones web con ejemplos reproducibles "
     "en un laboratorio local autorizado, y priorizamos las mitigaciones según el riesgo de cada "
     "una.", "Seguridad"),

    # ── Móvil ──────────────────────────────────────────────────────────────
    ("Ciclo de vida de una Activity",
     "Qué pasa cuando el usuario rota la pantalla o la app pasa a segundo plano: onCreate, onPause "
     "y onDestroy, y cómo conservar el estado con ViewModel en una aplicación Android escrita en "
     "Kotlin.", "Móvil"),
    ("Flutter: widgets con estado y sin estado",
     "La interfaz se declara componiendo widgets; cuando el estado cambia, el framework "
     "reconstruye el árbol. Ejemplo con setState, claves y separación de la lógica en un contador "
     "y una lista de tareas.", "Móvil"),
    ("Persistencia local con Room",
     "Guardamos las notas del usuario en SQLite a través de Room: entidades, DAOs y migraciones. "
     "La interfaz observa los cambios con Flow y se actualiza sola al insertar un registro.", "Móvil"),
    ("Notificaciones push bien hechas",
     "Integramos Firebase Cloud Messaging para avisar al usuario sin ser invasivos: canales de "
     "notificación, permisos en tiempo de ejecución y deep links que abren la pantalla correcta "
     "de la app móvil.", "Móvil"),
    ("Publicar en la App Store y Google Play",
     "Checklist de publicación: firmas y perfiles de aprovisionamiento, capturas y textos de la "
     "ficha, pruebas internas, revisión por etapas y qué hacer cuando la tienda rechaza la "
     "aplicación.", "Móvil"),
    ("Consumir una API desde iOS",
     "Con Swift y URLSession pedimos datos JSON, los decodificamos con Codable y los mostramos en "
     "una lista de SwiftUI, manejando estados de carga y error para una experiencia móvil fluida.", "Móvil"),

    # ── Cloud ──────────────────────────────────────────────────────────────
    ("Subir archivos a Object Storage",
     "Configuramos un bucket en Oracle Cloud (OCI), políticas de acceso y URLs prefirmadas para "
     "descargas temporales. Automatizamos la carga de respaldos con la CLI y reglas de ciclo de "
     "vida para archivar objetos viejos.", "Cloud"),
    ("Mi primera instancia en la nube",
     "Creamos una máquina virtual en OCI Compute: elegimos la forma, configuramos la red virtual "
     "VCN, abrimos el puerto 8080 en la lista de seguridad y desplegamos la aplicación con "
     "systemd.", "Cloud"),
    ("Serverless: cuándo sí y cuándo no",
     "Las funciones se facturan por invocación y escalan solas, pero el arranque en frío y los "
     "límites de tiempo condicionan el diseño. Casos de uso buenos: procesamiento de eventos y "
     "tareas puntuales.", "Cloud"),
    ("Ahorrar en la factura de la nube",
     "Etiquetamos recursos por proyecto, apagamos entornos de desarrollo por la noche, usamos "
     "instancias reservadas para cargas estables y alertas de presupuesto antes de que llegue la "
     "sorpresa.", "Cloud"),
    ("Alta disponibilidad multi región",
     "Diseñamos la aplicación para sobrevivir a la caída de una zona: balanceadores, réplicas de "
     "la base de datos, colas para desacoplar y pruebas de caos para validar el plan de "
     "recuperación.", "Cloud"),
    ("IAM: permisos con mínimo privilegio",
     "Organizamos usuarios en grupos y compartimentos, escribimos políticas que conceden solo lo "
     "necesario y auditamos con los registros de la cuenta de la nube quién hizo qué y cuándo.", "Cloud"),
]
