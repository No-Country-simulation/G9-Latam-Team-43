# Diccionario de tecnologías (gazetteer) para extraer palabras clave con nombre
# canónico a partir de texto libre. Complementa al TF-IDF: primero buscamos
# tecnologías conocidas y, si el texto casi no menciona ninguna, completamos con
# los términos de mayor peso TF-IDF del documento.
import re

TECNOLOGIAS: dict[str, str] = {
    # Lenguajes
    "Java": r"\bjava\b(?!\s*script)",
    "JavaScript": r"\bjavascript\b|\becmascript\b|\bes6\b",
    "TypeScript": r"\btypescript\b",
    "Python": r"\bpython\b",
    "Kotlin": r"\bkotlin\b",
    "Swift": r"\bswift\b",
    "Dart": r"\bdart\b",
    "C#": r"\bc#|\bc sharp\b",
    "C++": r"c\+\+",
    "Go": r"\bgolang\b",
    "Rust": r"\brust\b",
    "PHP": r"\bphp\b",
    "Ruby": r"\bruby\b",
    "SQL": r"\bsql\b(?!\s*injection)",
    "PL/SQL": r"\bpl\s*/?\s*sql\b",
    "HTML": r"\bhtml5?\b",
    "CSS": r"\bcss3?\b",
    "Bash": r"\bbash\b|\bscripting\b",
    # Backend / frameworks
    "Spring Boot": r"spring\s*boot",
    "Spring": r"\bspring\b(?!\s*(boot|security|cloud|data))",
    "Spring Security": r"spring\s*security",
    "Spring Data": r"spring\s*data",
    "Hibernate": r"\bhibernate\b",
    "JPA": r"\bjpa\b",
    "JUnit": r"\bjunit\b",
    "Mockito": r"\bmockito\b",
    "Maven": r"\bmaven\b",
    "Gradle": r"\bgradle\b",
    "API REST": r"apis?\s+rest(ful)?|rest(ful)?\s+apis?|\brestful\b|\bapi\s*rest\b|\brest\b",
    "GraphQL": r"\bgraphql\b",
    "JWT": r"\bjwt\b|json\s*web\s*token",
    "OAuth2": r"\boauth\s*2?\b",
    "Node.js": r"node\.?js|\bnode\b",
    "Express": r"\bexpress\b",
    "NestJS": r"\bnestjs\b",
    "Django": r"\bdjango\b",
    "Flask": r"\bflask\b",
    "FastAPI": r"\bfastapi\b",
    "Microservicios": r"\bmicroservicios?\b",
    "MVC": r"\bmvc\b|modelo[\s-]vista[\s-]controlador",
    "Swagger/OpenAPI": r"\bswagger\b|\bopenapi\b",
    "Postman": r"\bpostman\b",
    "WebSockets": r"\bwebsockets?\b",
    "ORM": r"\borm\b",
    "RabbitMQ": r"\brabbitmq\b",
    "Apache Kafka": r"\bkafka\b",
    # Frontend
    "React": r"\breact(\.?js)?\b(?!\s*native)",
    "React Native": r"react\s*native",
    "Angular": r"\bangular\b",
    "Vue": r"\bvue(\.?js)?\b",
    "Next.js": r"next\.?js",
    "Redux": r"\bredux\b",
    "Tailwind CSS": r"\btailwind\b",
    "Bootstrap": r"\bbootstrap\b",
    "Vite": r"\bvite\b",
    "Webpack": r"\bwebpack\b",
    "Jest": r"\bjest\b",
    "Sass": r"\bsass\b|\bscss\b",
    "Flexbox": r"\bflexbox\b",
    "CSS Grid": r"css\s*grid",
    "PWA": r"\bpwa\b|aplicaci[oó]n web progresiva",
    "Accesibilidad": r"\baccesibilidad\b|\bwcag\b|\ba11y\b|lector(es)? de pantalla",
    "Diseño Responsive": r"\bresponsive\b|dise[nñ]o adaptable|media\s*quer(y|ies)",
    "Lighthouse": r"\blighthouse\b",
    # Móvil
    "Android": r"\bandroid\b",
    "iOS": r"\bios\b",
    "Flutter": r"\bflutter\b",
    "Jetpack Compose": r"jetpack\s*compose",
    "SwiftUI": r"\bswiftui\b",
    "Room": r"\broom\b",
    "Firebase": r"\bfirebase\b",
    # Datos / ML
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "scikit-learn": r"scikit[\s-]?learn|\bsklearn\b",
    "TensorFlow": r"\btensorflow\b",
    "PyTorch": r"\bpytorch\b",
    "Keras": r"\bkeras\b",
    "Matplotlib": r"\bmatplotlib\b",
    "Seaborn": r"\bseaborn\b",
    "Jupyter": r"\bjupyter\b|\bnotebooks?\b",
    "TF-IDF": r"tf[\s-]?idf",
    "NLP": r"\bnlp\b|procesamiento de(l)? lenguaje natural",
    "Machine Learning": r"machine\s*learning|aprendizaje (autom[aá]tico|de m[aá]quina)|\bml\b",
    "Deep Learning": r"deep\s*learning|aprendizaje profundo",
    "Regresión Logística": r"regresi[oó]n log[ií]stica",
    "K-Means": r"k[\s-]?means",
    "Redes Neuronales": r"redes? neuronales?|\bcnn\b|convolucional(es)?",
    "spaCy": r"\bspacy\b",
    "NLTK": r"\bnltk\b",
    "Validación Cruzada": r"validaci[oó]n cruzada|cross[\s-]?validation",
    "EDA": r"\beda\b|an[aá]lisis exploratorio",
    "Series de Tiempo": r"series? (de )?tiempo|series? temporales?",
    # Bases de datos
    "PostgreSQL": r"postgres(ql)?",
    "MySQL": r"\bmysql\b",
    "MongoDB": r"mongo\s*db|\bmongo\b",
    "Redis": r"\bredis\b",
    "Oracle Database": r"\boracle\b(?!\s*cloud)",
    "SQLite": r"\bsqlite\b",
    "H2": r"\bh2\b",
    "Cassandra": r"\bcassandra\b",
    "Elasticsearch": r"\belasticsearch\b",
    "NoSQL": r"\bnosql\b",
    "Flyway": r"\bflyway\b",
    "Liquibase": r"\bliquibase\b",
    "Transacciones ACID": r"\bacid\b|transacciones",
    "Normalización": r"normalizaci[oó]n|forma normal",
    # DevOps / infraestructura
    "Docker": r"\bdocker\b|contenedor(es)?",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b|\bkubectl\b",
    "Terraform": r"\bterraform\b",
    "Ansible": r"\bansible\b",
    "Jenkins": r"\bjenkins\b",
    "GitHub Actions": r"github\s*actions",
    "GitLab CI": r"gitlab\s*ci|\bgitlab\b",
    "Git": r"\bgit\b(?!\s*(hub|lab))",
    "CI/CD": r"ci\s*/?\s*cd|integraci[oó]n continua|entrega continua|despliegue continuo",
    "Nginx": r"\bnginx\b",
    "Prometheus": r"\bprometheus\b",
    "Grafana": r"\bgrafana\b",
    "ELK": r"\belk\b|logstash|kibana",
    "Linux": r"\blinux\b|\bubuntu\b",
    "systemd": r"\bsystemd\b",
    "Infraestructura como Código": r"infraestructura como c[oó]digo|\biac\b",
    # Cloud
    "Oracle Cloud (OCI)": r"\boci\b|oracle\s*cloud",
    "Object Storage": r"object\s*storage",
    "OCI Compute": r"oci\s*compute",
    "AWS": r"\baws\b|amazon web services",
    "Azure": r"\bazure\b",
    "Google Cloud": r"google\s*cloud|\bgcp\b",
    "Serverless": r"\bserverless\b|funciones? (lambda|en la nube)|\blambda\b",
    "VCN": r"\bvcn\b|red(es)? virtual(es)?",
    "IAM": r"\biam\b|m[ií]nimo privilegio",
    "Balanceador de Carga": r"balanceador(es)? de carga|load\s*balancer",
    "CDN": r"\bcdn\b",
    "Alta Disponibilidad": r"alta disponibilidad|multi[\s-]?regi[oó]n",
    # Seguridad
    "OWASP": r"\bowasp\b",
    "XSS": r"\bxss\b|cross[\s-]site\s*scripting",
    "CSRF": r"\bcsrf\b",
    "Inyección SQL": r"inyecci[oó]n (de )?sql|sql\s*injection",
    "HTTPS/TLS": r"\bhttps\b|\btls\b|\bssl\b|certificados?",
    "Criptografía": r"cifrado|criptograf[ií]a|encriptaci[oó]n",
    "bcrypt": r"\bbcrypt\b",
    "Hashing": r"\bhash(ing|es)?\b",
    "Pentesting": r"\bpentest(ing)?\b|pruebas de penetraci[oó]n",
    "MFA": r"\bmfa\b|multifactor|doble factor",
    "Vault": r"\bvault\b|gestor de secretos",
    "Firewall": r"\bfirewall\b|lista de seguridad",
    "HSTS": r"\bhsts\b",
}

_COMPILADAS = [(nombre, re.compile(patron, re.IGNORECASE)) for nombre, patron in TECNOLOGIAS.items()]


def extraer_tecnologias(texto: str, maximo: int = 8) -> list[str]:
    """Devuelve tecnologías canónicas mencionadas, ordenadas por frecuencia y
    posición de primera aparición."""
    encontradas = []
    for nombre, patron in _COMPILADAS:
        coincidencias = list(patron.finditer(texto))
        if coincidencias:
            encontradas.append((nombre, len(coincidencias), coincidencias[0].start()))
    encontradas.sort(key=lambda t: (-t[1], t[2]))
    return [nombre for nombre, _, _ in encontradas[:maximo]]


def palabras_clave(texto: str, vectorizador=None, maximo: int = 8) -> list[str]:
    """Palabras clave del documento: gazetteer de tecnologías + relleno con los
    términos de mayor peso TF-IDF cuando el texto menciona pocas tecnologías."""
    claves = extraer_tecnologias(texto, maximo)
    if vectorizador is not None and len(claves) < 3:
        X = vectorizador.transform([texto]).tocoo()
        nombres = vectorizador.get_feature_names_out()
        pares = sorted(zip(X.col, X.data), key=lambda p: -p[1])
        vistas = {c.lower() for c in claves}
        for columna, _ in pares:
            termino = str(nombres[columna])
            if len(termino) > 3 and not termino.isdigit() and termino not in vistas:
                claves.append(termino)
                vistas.add(termino)
            if len(claves) >= min(5, maximo):
                break
    return claves[:maximo]
