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
        pokemon_list = db.get_all_pokemon()
        return _build_response(200, [p.model_dump() for p in pokemon_list])
    except Exception:
        traceback.print_exc()
        return _build_response(500, {"error": "Error interno del servidor"})
