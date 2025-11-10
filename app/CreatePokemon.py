import json
import traceback
from app.db.dynamodb_db import DynamoDB
from app.model.pokemon import Pokemon
from pydantic import ValidationError

db = DynamoDB()

def _build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,x-api-key,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps(body)
    }

def handler(event, context):
    try:
        data = json.loads(event.get('body', '{}'))
        pokemon_in = Pokemon(**data)
        created_pokemon = db.create_pokemon(pokemon_in)
        return _build_response(201, created_pokemon.model_dump())
    except ValidationError as e:
        return _build_response(400, {"error": "Input inválido", "detalles": e.errors()})
    except Exception:
        traceback.print_exc()
        return _build_response(500, {"error": "Error interno del servidor"})
