# SendosAI

proyecto diseñado como parte de un desafao técnico para la empresa SendosAI. El proposito central de este proyecto es desarrollar un sistema de inventario utilizando Python y FastAPI, integrado con PostgreSQL para almacenamiento de datos. Ademas, se aseguraron los endpoints utilizando tokens JWT para garantizar la seguridad de las operaciones.

El proyecto fue dockerizado utilizando Docker y Docker Compose para facilitar la gestion del entorno de desarrollo y despliegue. Se enfatizo en la realizacion de pruebas unitarias asincronicas utilizando pytest.

Este proyecto demuestra habilidades en el desarrollo de microservicios eficientes, integracion con bases de datos, implementacion de seguridad y buenas practicas de desarrollo agil y despliegue continuo (CI/CD).




## Requisitos

Los requisitos estan definidos en el archivo pyproject.toml


## Installation

Clonar el repositorio

crear dentro de la carpeta raiz del proyecto el archivo .env con el siguiente formato:

```bash
ENVIRONMENT=local
SECRET_KEY=secert_key
DEBUG=True
OPENAPI_PREFIX=""
ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_TOKEN_PREFIX="Bearer"
ALGORITHM="HS256"
JWT_SUBJECT="access"

POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_SERVER=db_host
POSTGRES_PORT=db_port
```

Instalar poetry y las dependencias del proyecto ejecutando los comando:
```bash
python -m pip install --upgrade pip
pip install poetry
poetry install
```

Una vez creado el entorno con poetry ejecutar el siguiente comando para iniciar el servidor:
```bash
poetry run uvicorn main:app
```


## Docker

Desplegar proyecto en docker:

Crear la red en docker:
```bash
docker network create "sendos-net"
```

Ejecutar el siguiente comando:
```bash
docker compose -f docker-compose.yml up --build -d
```


## Documentation

Ingresar al swaggwer desde la url:
```bash
http://127.0.0.1:8000/docs
```
