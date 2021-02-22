# Introducción

Aquí yacen los archivos necesarios para desarrollar y ejecutar el núcleo de la Misión Observatorio Electoral (MOE). El mismo consta de un _BackEnd_ monolítico basado en Python que compone una API a disposición de los diferentes métodos:

* Autenticación
* Votación
* Permisos

Estos métodos propios de la API están autodocumentados mediante OpenAPI.

# Desarrollo

A continuación listan las diferentes opciones al momento de replicar y configurar el entorno necesario para el desarrollo del proyecto. Además figura una breve descripción y explicación de las tareas comunes a los procesos del desarrollo.

Finalmente, un apartado facilita instrucciones para efectuar la virtualización.

## Package managers

Las dependencias, y el versionado de las mismas, están dadas en el archivo `pyproject.toml` (estándar sucesor a `requirements.txt`) y este proyecto es gestionado mediante el package manager `poetry`.

### Poetry

Instalar los requerimientos dados por `pyproject.toml` mediante: `poetry install`.

### Nix

Una de las características del proyecto es fomentar _builds  reproducibles_.

Es posible acceder a un entorno pre-configurado mediante Nix: `nix develop`.

Dicho entorno está declarado en el archivo `flake.nix`.

**Nota:** _La similitud entre las referencias `flake.nix` y `.flake8` es coincidencia._

## Tasks

Las tareas comunes del desarollo están implementadas gracias a PyInvoke, con especificación en el archivo `tasks.py`. El motivo por el cual es preferible utilizar esta librería, a diferencia de los clásicos `Make/CMake`, es porque al estar basada 100% en Python la misma es cross-platform ó multiplataforma.

Es posible visualizar las tareas disponibles mediante la ejecución: `inv -l`.

| Comando | Descripción |
| :-----: | :---------: |
| serve   | Ejecuta `uvicorn/gunicorn` según la instancia desarrollo/producción |
| lint    | Ejecuta el linter `flake8` en base a los estándares PEPs requeridos
| cc      | Ejecuta el linter `radon` para medir la complejidad ciclomática |

## Virtualización

Los archivos necesarios están dados bajo el formato estándar.

Utilizando `docker` ó `podman` bastaría con ejecutar: `docker-compose up -d`
para instanciar los contenedores necesarios en base a las imágenes dadas.

## Pipelines

_To-Do ..._

# Arquitectura

A continuación una lista de características del sistema:

* Implementación asíncrona
* Autodocumentación (OpenAPI)
* Evaluaciones de performance (CC)

Los diferentes motivos por los cuales rigen ciertas tecnologías por sobre otras, respecto de las diversas partes que componen al sistema en su totalidad, están deteallados en el directorio `/docs/adr-*`. A su vez, dicha ruta contendrá otra clase de documentación como lo son los `guidelines` ó las guías de trabajo.

Esto debería no sólo justificar sino también facilitar el por qué de las decisiones y opiniones de arquitectura tomadas durante las etapas del desarrollo a quienes corresponda heredar el mismo.
