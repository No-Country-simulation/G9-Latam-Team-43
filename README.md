# G9-Latam-Team-43

# TechMind
### Organización Inteligente del Conocimiento Técnico

TechMind es una plataforma que utiliza técnicas de Ciencia de Datos y Procesamiento de Lenguaje Natural (NLP) para organizar, clasificar y enriquecer contenidos técnicos de manera automática.

Su propósito es transformar grandes volúmenes de documentación, tutoriales, artículos, anotaciones de estudio y materiales de referencia en una base de conocimiento estructurada, searchable y reutilizable.

---

# Objetivo

Permitir que usuarios, estudiantes, comunidades técnicas y organizaciones puedan:

- Organizar automáticamente contenidos técnicos.
- Clasificar documentos por categorías.
- Extraer palabras clave relevantes.
- Identificar contenidos similares.
- Realizar búsquedas semánticas.
- Construir repositorios inteligentes de conocimiento.

---

# Problema que Resuelve

Los profesionales de tecnología consumen diariamente grandes cantidades de información:

- Documentación técnica
- Cursos
- Tutoriales
- Blogs especializados
- Notas personales
- Material de capacitación

Con el tiempo, encontrar información previamente consultada se vuelve difícil y costoso.

TechMind automatiza esta tarea mediante técnicas de Machine Learning y NLP.

---

# Funcionalidades MVP

✅ Clasificación automática de contenidos

✅ Extracción de palabras clave

✅ Identificación de temas relevantes

✅ API REST para procesamiento de documentos

✅ Respuesta en formato JSON

✅ Integración con Oracle Cloud Infrastructure (OCI)

---

# 👥  Equipo del Proyecto



| Nombre                       | Rol                    |
|------------------------------|-------------------------|
| Sergio Ceballos              | Backend Developer       |
| David De La Cruz             | Backend Developer       |
| Mauricio Rojas               | Backend Developer       |
| Ruben Hidalgo                | Project Manager         |
| Jose Ernesto Velasquez       | Data Analyst            |
| Melissa Lopez                | Data Analyst            |
| Miguel Tapiero               | Data Scientist          |
| Flor Humpiri                 | Backend Developer       |


---

# Arquitectura de la Solución (en desarollo).

---

# Propuesta de Organización del Equipo

Para maximizar la productividad durante el hackathon y permitir el desarrollo en paralelo, se propone dividir el trabajo en tres áreas principales. Cada área tendrá objetivos claros y entregables definidos, asegurando una integración fluida de todos los componentes del proyecto.

## 1. Data Science e Inteligencia Artificial

### Objetivo
Desarrollar la inteligencia del sistema encargada de analizar y comprender los contenidos técnicos.

### Responsabilidades
- Construcción y preparación de la base de conocimiento.
- Limpieza y procesamiento de texto (NLP).
- Extracción de palabras clave.
- Clasificación automática de contenidos.
- Evaluación y selección de modelos.
- Entrenamiento, validación y serialización del modelo.
- Definición de la estructura JSON de salida.

### Entregables
- Notebook de exploración y entrenamiento.
- Modelo entrenado (pickle/joblib).
- Métricas de desempeño.
- Documentación del proceso de modelado.

---

## 2. Backend y APIs

### Objetivo
Construir la capa de servicios que conectará la aplicación con el modelo de Inteligencia Artificial.

### Responsabilidades
- Diseño de la arquitectura de la solución.
- Desarrollo de API REST.
- Integración con el modelo de IA.
- Validación de datos de entrada.
- Manejo de errores y excepciones.
- Integración con OCI (Object Storage, Compute, etc.).
- Generación de respuestas estructuradas en JSON.

### Entregables
- API funcional y documentada.
- Endpoints operativos.
- Documentación Swagger/OpenAPI.
- Integración con servicios OCI.

---

## 3. Frontend, UX/UI y Experiencia de Usuario

### Objetivo
Diseñar una experiencia intuitiva y atractiva que permita demostrar fácilmente el valor de la solución.

### Responsabilidades
- Diseño de la interfaz de usuario.
- Creación del flujo de interacción.
- Desarrollo de formularios de consulta.
- Visualización de resultados.
- Integración con la API.
- Preparación de la demostración para jurados y evaluadores.

### Entregables
- Interfaz web funcional.
- Conexión con la API.
- Pantalla de consulta y visualización de resultados.
- Demo lista para presentación.

---

## Coordinación General

### Integración
Todos los equipos trabajarán sobre contratos de integración previamente definidos:

**Data Science → Backend**
- Modelo serializado.
- Formato de entrada y salida.
- Variables requeridas.

**Backend → Frontend**
- Endpoints disponibles.
- Estructura JSON de respuesta.
- Manejo de errores.

### Reuniones de Seguimiento
- Checkpoint técnico cada 2 horas.
- Revisión de avances e impedimentos.
- Integración continua de componentes.

---

## Distribución Inicial del Equipo

| Área | Integrantes |
|--------|------------|
| **Data Science e IA** | Jose Velasquez, Melissa Lopez, Miguel Tapiero, Ruben Hidalgo    |
| **Backend** | Sergio Ceballos, David De La Cruz, Mauricio Rojas, Flor Humpiri           |
| **Frontend y UX/UI** | Por definir  |

----

# Entrenamiento del Modelo  (Propuesta a revisar) 

# Entrenamiento del Modelo

## Preprocesamiento de Datos

Antes del entrenamiento, los textos son preparados mediante las siguientes etapas:

- Limpieza de texto.
- Tokenización.
- Eliminación de stopwords.
- Lematización o normalización lingüística.

## Modelado

### Modelo Base Propuesto

Para el MVP se propone una solución simple, explicable y de rápida implementación:

- TF-IDF (Term Frequency - Inverse Document Frequency) para representación vectorial de los textos.
- Regresión Logística (Logistic Regression) para clasificación de contenidos.

### Modelos Alternativos

Según el tiempo disponible y los resultados obtenidos, se pueden evaluar otras técnicas:

- Random Forest
- XGBoost
- Naive Bayes
- Support Vector Machines (SVM)
- Agrupamiento mediante K-Means
- Análisis de Similaridad Coseno

## Evaluación del Modelo

El desempeño será medido mediante métricas estándar de clasificación:

- Accuracy
- Precision
- Recall
- F1-Score

### Resultados de Referencia

| Métrica | Valor |
|----------|--------|
| Accuracy | 0.91 |
| Precision | 0.89 |
| Recall | 0.88 |
| F1 Score | 0.88 |

## Entregables de Data Science

- Exploración y análisis de datos (EDA).
- Preparación y limpieza del corpus documental.
- Extracción de características textuales.
- Entrenamiento y evaluación del modelo.
- Generación de métricas de desempeño.
- Serialización del modelo (Joblib/Pickle).
- Documentación de resultados y conclusiones.
