import json
import traceback
from app.db.dynamodb_db import DynamoDB
from app.model.pokemon import PokemonUpdate
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
        pokedex_id = int(event['pathParameters']['id'])
        data = json.loads(event.get('body', '{}'))
        pokemon_data = PokemonUpdate(**data)
        updated_pokemon = db.update_pokemon(pokedex_id, pokemon_data)
        if updated_pokemon:
            return _build_response(200, updated_pokemon.model_dump())
        else:
            return _build_response(404, {"error": "Pokémon no encontrado o actualización fallida"})
    except ValueError:
        return _build_response(400, {"error": "El ID debe ser un número entero."})
    except ValidationError as e:
        return _build_response(400, {"error": "Input inválido", "detalles": e.errors()})
    except Exception:
        traceback.print_exc()
        return _build_response(500, {"error": "Error interno del servidor"})
