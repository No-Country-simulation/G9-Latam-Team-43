# Stopwords en español para el vectorizador TF-IDF.
# sklearn compara las stopwords contra los tokens YA preprocesados (minúsculas y
# sin acentos, porque usamos strip_accents="unicode"), así que normalizamos la
# lista al importar el módulo para mantener la consistencia.
import unicodedata

_CRUDAS = """
a al algo alguna algunas alguno algunos ante antes aquel aquella aquellas aquellos aqui aquí
cada como cómo con contra cual cuál cuales cualquier cuando cuándo cuanto de del desde donde dónde
durante e el él ella ellas ello ellos en entre era erais eran eras eres es esa esas ese eso esos esta
estaba estabais estaban estabas estad estada estadas estado estados estamos estando estar estaremos
estará estarán estarás estaré estaréis estaría estaríais estaríamos estarían estarías estas
este estemos esto estos estoy estuve estuviera estuvieron estuvimos estuvo está estábamos estáis
están estás esté estéis estén fin fue fuera fueran fueron fui fuimos gran ha habida habido habiendo
habremos habrá habrán habrás habré habría habrían haber habida habidas había habíais habíamos habían
habías han has hasta hay haya hayamos hayan hayas he hemos hube hubiera hubieron hubo la las le les
lo los me mi mis mismo misma mismos mismas mucha muchas mucho muchos muy más mí mía mías mío míos
nada ni no nos nosotras nosotros nuestra nuestras nuestro nuestros o os otra otras otro otros para
pero poco por porque primero pues que quien quienes qué se sea seamos sean seas segun según ser
seremos será serán serás seré sería serían si sido siendo sin sobre sois somos son soy su sus suya
suyas suyo suyos sí también tanto te tenemos tener tenga tengan tengo tenida tenido tiene tienen
toda todas todavia todavía todo todos tras tu tus tuya tuyas tuyo tuyos tú un una unas uno unos
usted ustedes va vamos van varias varios ve veces ver vez vosotras vosotros voy vuestra vuestras
vuestro vuestros y ya yo
""".split()

# Palabras de "andamiaje" que aparecen por igual en cualquier contenido educativo
# (curso, tutorial, apuntes...) y no aportan señal de categoría: las excluimos
# del vocabulario para que no contaminen ni el modelo ni las etiquetas de clusters.
_GENERICAS = """
aprende aprender aprenderas aprenderás apunte apuntes articulo artículo avanzado basicos básicos
buenas charla clase clave completa comunes concepto conceptos contenido contenidos curso demo
desde cero detalle documentacion documentación dominar ejemplo ejemplos ejercicios equipo errores
estudiantes estudio explica formacion formación guia guía herramienta herramientas importa incluye
interna introduccion introducción material muestra notas orientado paso pensada practica practicas
práctica prácticas practico práctico presenta presentan principiantes profesionales rapidas rápidas
referencia repasamos resueltos resumen taller tema temas transcripcion transcripción tutorial
utiliza utilizando vimos video
""".split()


def _sin_acentos(palabra: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", palabra) if not unicodedata.combining(c)
    )


STOPWORDS_ES = sorted({_sin_acentos(p.lower()) for p in _CRUDAS})
GENERICAS_CONTENIDO = sorted({_sin_acentos(p.lower()) for p in _GENERICAS})

# Lista final que se pasa a TfidfVectorizer(stop_words=...)
STOPWORDS_VECTORIZADOR = sorted(set(STOPWORDS_ES) | set(GENERICAS_CONTENIDO))
