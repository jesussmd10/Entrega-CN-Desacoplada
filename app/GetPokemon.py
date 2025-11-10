import json
import traceback
from app.db.dynamodb_db import DynamoDB

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
        pokedex_id = int(event['pathParameters']['id'])
        pokemon = db.get_pokemon(pokedex_id)
        if pokemon:
            return _build_response(200, pokemon.model_dump())
        else:
            return _build_response(404, {"error": "Pokémon no encontrado"})
    except ValueError:
        return _build_response(400, {"error": "El ID debe ser un número entero."})
    except Exception:
        traceback.print_exc()
        return _build_response(500, {"error": "Error interno del servidor"})
