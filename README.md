# Framework Genérico de Automatización de Pipelines y Control de Calidad de Datos para Machine Learning

Entorno de desarrollo

El proyecto fue desarrollado y probado utilizando el siguiente entorno tecnológico:

Sistema operativo: Windows.

Lenguaje de programación: Python 3.14.3.

Manipulación de datos: pandas 3.1.1.

Machine Learning: scikit-learn 1.9.1.

Persistencia de modelos: joblib 1.6.0.

Pruebas automatizadas: pytest 9.2.0.

Versionamiento de datos: DVC 3.67.1.

Control de versiones de código: Git 2.48.1.

Las versiones de las dependencias se registran para facilitar la reproducción del entorno de ejecución.

## 1. Descripción del proyecto

Este proyecto implementa un framework de automatización de pipelines de Machine Learning (MLOps), diseñado para facilitar la preparación, validación, entrenamiento y evaluación de modelos predictivos.

La solución busca estandarizar el flujo de trabajo mediante configuraciones externas en formato JSON, contratos de calidad de datos y automatización de tareas. Su diseño permite incorporar diferentes conjuntos de datos sin modificar la lógica principal del entrenamiento y la evaluación, siempre que se proporcione la configuración y el contrato correspondientes.

Para demostrar su funcionamiento se utilizan dos conjuntos de datos de ejemplo:

- **Iris:** clasificación de tres especies de flores a partir de cuatro características numéricas.
- **Wine:** clasificación de tres clases de vino a partir de trece características numéricas.

## 2. Objetivos

- Automatizar la ejecución del pipeline de Machine Learning.
- Validar la estructura, los tipos de datos, los valores nulos y los rangos permitidos.
- Definir contratos de datos mediante archivos JSON.
- Estandarizar el entrenamiento y la evaluación de modelos.
- Incorporar pruebas automáticas de calidad.
- Utilizar Git y DVC para el control de versiones del código y los artefactos.

## 3. Arquitectura del proyecto

La estructura principal del repositorio es:

```text
mlops-pipeline-framework/
│
├── configs/
│   ├── iris.json
│   └── wine.json
│
├── contracts/
│   ├── iris_contract.json
│   └── wine_contract.json
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── reports/
│
├── src/
│   ├── __init__.py
│   ├── prepare_data.py
│   ├── validate_data.py
│   ├── train.py
│   ├── evaluate.py
│   └── pipeline.py
│
├── tests/
│   └── test_validation.py
│
├── Makefile
├── requirements.txt
├── dvc.yaml
├── README.md
├── run.py
└── .gitignore
```

### Descripción de los componentes

| Componente | Función |
|---|---|
| `configs/` | Contiene la configuración de cada conjunto de datos. |
| `contracts/` | Define las reglas de calidad de los datos en JSON. |
| `data/raw/` | Almacena los datos originales. |
| `data/processed/` | Almacena los datos preparados para evaluación. |
| `models/` | Almacena los modelos entrenados. |
| `reports/` | Contiene las métricas de evaluación. |
| `src/prepare_data.py` | Descarga o prepara los conjuntos de datos de ejemplo. |
| `src/validate_data.py` | Comprueba el cumplimiento del contrato de datos. |
| `src/train.py` | Ejecuta el entrenamiento del modelo. |
| `src/evaluate.py` | Calcula las métricas de rendimiento. |
| `src/pipeline.py` | Coordina la validación, el entrenamiento y la evaluación. |
| `tests/` | Contiene las pruebas automáticas. |
| `run.py` | Orquesta la ejecución completa del proyecto. |
| `dvc.yaml` | Define las etapas controladas por DVC. |

## 4. Requisitos previos

Para ejecutar el proyecto se requiere:

- Windows, Linux o macOS.
- Python 3.12 o superior compatible con las dependencias instaladas.
- Git.
- DVC.
- Conexión a Internet para preparar los conjuntos de datos de ejemplo por primera vez.

Las dependencias de Python están especificadas en `requirements.txt`.

## 5. Instalación y configuración del entorno

### Paso 1. Clonar o descargar el proyecto

Si se encuentra publicado en un repositorio Git:

```bash
git clone URL_DEL_REPOSITORIO
cd mlops-pipeline-framework
```

Si se recibió como carpeta comprimida, se debe descomprimir y abrir una terminal en el directorio principal.

### Paso 2. Crear un entorno virtual

En Windows PowerShell:

```powershell
python -m venv venv
```

Activar el entorno:

```powershell
.\venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### Paso 3. Instalar las dependencias

```bash
python -m pip install --upgrade pip

# Instalar dependencias principales
pip install -r requirements.txt

# Para reproducir el entorno completo con versiones registradas
pip install -r requirements-lock.txt
```

### Paso 4. Verificar las herramientas

```bash
python --version
git --version
dvc --version
```

## 6. Ejecución del pipeline

El proyecto cuenta con un orquestador principal llamado `run.py`, que permite ejecutar las etapas del proceso mediante un solo comando.

### Ejecutar con Iris

```bash
python run.py --config configs/iris.json
```

### Ejecutar con Wine

```bash
python run.py --config configs/wine.json
```

El orquestador ejecuta las siguientes etapas:

1. Preparación del conjunto de datos.
2. Validación de calidad mediante el contrato JSON.
3. Entrenamiento del modelo de Machine Learning.
4. Evaluación del modelo.
5. Ejecución de las pruebas automáticas.

Si una etapa falla, el proceso se detiene y muestra el error correspondiente.

## 7. Contratos de calidad de datos

Cada conjunto de datos cuenta con un contrato independiente en formato JSON.

Los contratos establecen:

- Columnas obligatorias.
- Tipos de datos esperados.
- Restricciones de valores nulos.
- Rangos mínimos y máximos.
- Valores permitidos para variables categóricas.

Ejemplo ilustrativo de una regla:

```json
{
    "sepal length (cm)": {
        "type": "number",
        "nullable": false,
        "min": 0,
        "max": 10
    }
}
```

La validación se implementa utilizando bibliotecas estándar de Python, sin depender de librerías externas de validación de datos.

### Ejemplo de registro válido

```csv
sepal length (cm),sepal width (cm),petal length (cm),petal width (cm),target
5.1,3.5,1.4,0.2,setosa
```

### Ejemplo de registro inválido

```csv
sepal length (cm),sepal width (cm),petal length (cm),petal width (cm),target
11,3.5,1.4,0.2,unknown
```

El segundo registro incumple las reglas ilustrativas del contrato porque presenta un valor fuera del rango permitido y una categoría no reconocida.

## 8. Pruebas automáticas

El proyecto utiliza `pytest` para comprobar el funcionamiento del módulo de validación.

Ejecutar las pruebas:

```bash
python -m pytest tests -v
```

Se contemplan cuatro escenarios:

1. Datos válidos.
2. Presencia de valores nulos.
3. Valores fuera de los rangos permitidos.
4. Categorías no autorizadas.

Las pruebas permiten verificar que el validador identifica correctamente los incumplimientos definidos en el contrato.

## 9. Versionamiento y reproducibilidad con DVC

DVC se utiliza para gestionar los datos y artefactos generados por el pipeline.

El archivo `dvc.yaml` define las etapas, dependencias, salidas y métricas del proceso.

Comandos principales:

Consultar el flujo de ejecución:

```bash
dvc dag
```

Ejecutar o actualizar las etapas necesarias:

```bash
dvc repro
```

Forzar la ejecución:

```bash
dvc repro --force
```

Consultar el estado del pipeline:

```bash
dvc status
```

Consultar la sincronización con el almacenamiento remoto:

```bash
dvc status -c
```

Enviar los artefactos al almacenamiento remoto:

```bash
dvc push
```

En el desarrollo de este proyecto se configuró un almacenamiento remoto local llamado `localremote`. Esta configuración permite demostrar la transferencia y sincronización de los artefactos mediante DVC. No corresponde a un almacenamiento en la nube.

## 10. Resultados de referencia

Durante las ejecuciones de prueba se obtuvieron los siguientes resultados:

| Métrica | Iris | Wine |
|---|---:|---:|
| Accuracy | 0.9000 | 1.0000 |
| Precision macro | 0.9024 | 1.0000 |
| Recall macro | 0.9000 | 1.0000 |
| F1 macro | 0.8997 | 1.0000 |

Los resultados corresponden a las ejecuciones realizadas con la configuración y partición de datos establecidas en el proyecto. Un resultado alto en una partición de prueba no garantiza el mismo desempeño con datos nuevos.

## 11. Extensión a otros conjuntos de datos

El framework está organizado para facilitar la incorporación de nuevos conjuntos de datos.

Para incorporar uno nuevo se deben realizar, como mínimo, las siguientes actividades:

1. Preparar el archivo CSV con las variables predictoras y la variable objetivo.
2. Crear un contrato JSON con las columnas, tipos, restricciones y valores permitidos.
3. Crear un archivo de configuración JSON que indique la ruta de los datos, el contrato, la variable objetivo, las características y el tipo de modelo.
4. Adaptar el módulo de preparación para reconocer la nueva fuente de datos, si se requiere preparación automatizada.
5. Ejecutar el pipeline y comprobar los resultados.

La lógica de validación, entrenamiento y evaluación está diseñada para reutilizarse mediante configuraciones. La preparación de nuevas fuentes puede requerir una adaptación adicional.

## 12. Limitaciones y consideraciones

- Los conjuntos Iris y Wine son ejemplos académicos y no representan necesariamente datos de producción.
- La evaluación utiliza una partición de entrenamiento y prueba; para una validación más robusta se recomienda incorporar validación cruzada.
- El almacenamiento remoto configurado es local, no una plataforma de nube.
- Los resultados dependen de las características del conjunto de datos, la configuración y los parámetros del modelo.
- Antes de utilizar el framework en producción se deben incorporar controles adicionales de seguridad, monitoreo, trazabilidad y gestión de datos.

## 13. Conclusión

El proyecto implementa una estructura reutilizable para automatizar pipelines de Machine Learning y controlar la calidad de los datos antes del entrenamiento.

La integración de configuraciones JSON, contratos de datos, pruebas automáticas, orquestación mediante Python y versionamiento con Git y DVC permite establecer un flujo reproducible y organizado.

Las pruebas realizadas con Iris y Wine demuestran que la misma estructura puede utilizarse con diferentes conjuntos de datos, manteniendo separadas las reglas de validación y configuración de cada uno.

## 14. Evidencias de validación

Se probaron cuatro archivos CSV:

- `examples/valid_iris.csv`
- `examples/invalid_iris.csv`
- `examples/valid_wine.csv`
- `examples/invalid_wine.csv`

Los archivos válidos generaron listas vacías de errores (`[]`).

Los archivos inválidos permitieron detectar cuatro incumplimientos:
dos relacionados con rangos numéricos y dos con categorías no permitidas.

Los resultados confirman el funcionamiento del módulo de validación
para los dos conjuntos de datos.