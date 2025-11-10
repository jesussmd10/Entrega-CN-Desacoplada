# Pokedex Serverless API (Desacoplada)

Este proyecto implementa una API RESTful para una Pokedex utilizando una arquitectura serverless en AWS. La aplicación está desacoplada, lo que significa que cada operación CRUD (Crear, Leer, Actualizar, Eliminar) para los Pokémon se maneja mediante funciones AWS Lambda separadas, desplegadas como imágenes Docker. La base de datos utilizada es Amazon DynamoDB.

## Características

*   **API RESTful:** Proporciona endpoints para gestionar la información de Pokémon.
*   **Operaciones CRUD:**
    *   `POST /pokemon`: Crea un nuevo Pokémon.
    *   `GET /pokemon/{id}`: Obtiene un Pokémon por su ID.
    *   `GET /pokemon`: Obtiene todos los Pokémon.
    *   `PUT /pokemon/{id}`: Actualiza un Pokémon existente.
    *   `DELETE /pokemon/{id}`: Elimina un Pokémon.
*   **Serverless:** Construido con AWS Lambda y Amazon API Gateway.
*   **Contenedores Docker:** Las funciones Lambda se empaquetan y despliegan como imágenes Docker.
*   **Base de Datos NoSQL:** Utiliza Amazon DynamoDB para el almacenamiento de datos.
*   **Infraestructura:** Despliegue gestionado a través de AWS CloudFormation.

## Arquitectura

La arquitectura del proyecto se basa en los siguientes servicios de AWS:

*   **AWS Lambda:** Ejecuta el código de las funciones de la API sin necesidad de provisionar o gestionar servidores. Cada operación CRUD tiene su propia función Lambda.
*   **Amazon API Gateway:** Actúa como el "front-door" para la aplicación, enrutando las solicitudes HTTP a las funciones Lambda correspondientes.
*   **Amazon DynamoDB:** Una base de datos NoSQL rápida y flexible que almacena la información de los Pokémon.
*   **Amazon ECR (Elastic Container Registry):** Almacena las imágenes Docker de las funciones Lambda.
*   **AWS CloudFormation:** Define y provisiona todos los recursos de AWS necesarios para la aplicación de manera declarativa.

```
[Cliente] --(HTTP)--> [API Gateway] --(Invoca)--> [AWS Lambda (Docker Image)] --(Lee/Escribe)--> [DynamoDB]
```

## Configuración y Despliegue

Este proyecto utiliza AWS CloudFormation para el despliegue.

### Prerrequisitos

*   Cuenta de AWS configurada con credenciales.
*   AWS CLI instalado y configurado.
*   Docker instalado.
*   Python 3.11+ y `pip` instalados.
*   `boto3`, `botocore`, `pydantic` (ver `requirements.txt`).

### Pasos de Despliegue

1.  **Construir y Etiquetar la Imagen Docker:**
    Navega al directorio raíz del proyecto (`Entrega CN Desacoplada`).
    ```powershell
    docker build -t pokedex-lambda-image:latest .
    ```

2.  **Autenticar Docker con ECR:**
    ```powershell
    aws ecr get-login-password --region <tu-region> | docker login --username AWS --password-stdin <tu-cuenta-aws>.dkr.ecr.<tu-region>.amazonaws.com
    ```

3.  **Etiquetar la Imagen para ECR y Subir:**
    ```powershell
    docker tag pokedex-lambda-image:latest <tu-cuenta-aws>.dkr.ecr.<tu-region>.amazonaws.com/pokedex-lambda-image:latest
    docker push <tu-cuenta-aws>.dkr.ecr.<tu-region>.amazonaws.com/pokedex-lambda-image:latest
    ```
    Asegúrate de reemplazar `<tu-cuenta-aws>` y `<tu-region>` con tus valores reales.

4.  **Desplegar la Pila de CloudFormation:**
    Despliega la pila de CloudFormation utilizando tu método preferido (por ejemplo, a través de la consola de AWS o un script de CI/CD). El `template.yml` define todos los recursos de AWS, incluyendo las funciones Lambda, API Gateway y DynamoDB.

## Estructura del Proyecto

*   `Dockerfile`: Define el entorno Docker para las funciones Lambda.
*   `ecr.yml`: Configuración para Amazon ECR (posiblemente para la creación del repositorio).
*   `frontend.html`: Un archivo HTML de ejemplo para interactuar con la API.
*   `requirements.txt`: Lista las dependencias de Python para las funciones Lambda.
*   `template.yml`: La plantilla principal de AWS CloudFormation para desplegar la infraestructura.
*   `app/`: Contiene el código de las funciones Lambda.
    *   `CreatePokemon.py`: Lógica para crear un Pokémon.
    *   `DeletePokemon.py`: Lógica para eliminar un Pokémon.
    *   `GetAllPokemon.py`: Lógica para obtener todos los Pokémon.
    *   `GetPokemon.py`: Lógica para obtener un Pokémon por ID.
    *   `UpdatePokemon.py`: Lógica para actualizar un Pokémon.
    *   `app/db/`: Módulos de la base de datos.
        *   `db.py`: Interfaz genérica de la base de datos.
        *   `dynamodb_db.py`: Implementación específica para DynamoDB.
    *   `app/model/`: Modelos de datos.
        *   `pokemon.py`: Define el modelo de datos para un Pokémon.

## Uso de la API

Una vez desplegada, la URL base de tu API Gateway estará disponible en la sección "Outputs" de tu pila de CloudFormation.

### Ejemplos de Prueba

Para probar la API, puedes utilizar el archivo `frontend.html` incluido en el proyecto o importar las colecciones de Postman que tengas disponibles. Asegúrate de reemplazar `<api-gateway-id>`, `<region>` y `<tu-api-key>` con los valores de tu despliegue. La API Key se genera automáticamente con el despliegue de CloudFormation.
