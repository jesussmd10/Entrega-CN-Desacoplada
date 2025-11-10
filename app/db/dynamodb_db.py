import os
import boto3
from typing import List, Optional
from app.model.pokemon import Pokemon, PokemonUpdate
from app.db.db import DBInterface
from botocore.exceptions import ClientError

class DynamoDB(DBInterface):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        # Usar variable de entorno con fallback a 'PokemonTable'
        self.table_name = os.environ.get('TABLE_NAME', 'PokemonTable')
        self.table = self.dynamodb.Table(self.table_name)
    def create_pokemon(self, pokemon: Pokemon) -> Pokemon:
        try:
            item = pokemon.model_dump()
            self.table.put_item(Item=item)
            return pokemon
        except ClientError as e:
            print(f"Error al crear: {e}")
            raise e
    def get_pokemon(self, pokedex_id: int) -> Optional[Pokemon]:
        try:
            response = self.table.get_item(Key={'pokedex_id': pokedex_id})
            if 'Item' in response:
                return Pokemon(**response['Item'])
            return None
        except ClientError as e:
            print(f"Error al obtener item: {e}")
            return None
    def get_all_pokemon(self) -> List[Pokemon]:
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            return [Pokemon(**item) for item in items]
        except ClientError as e:
            print(f"Error al escanear: {e}")
            return []
    def update_pokemon(self, pokedex_id: int, pokemon_data: PokemonUpdate) -> Optional[Pokemon]:
        update_values = pokemon_data.model_dump(exclude_unset=True)
        if not update_values:
            return self.get_pokemon(pokedex_id) 
        update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in update_values)
        expression_attribute_names = {f"#{k}": k for k in update_values}
        expression_attribute_values = {f":{k}": v for k, v in update_values.items()}
        try:
            response = self.table.update_item(
                Key={'pokedex_id': pokedex_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW", 
                ConditionExpression="attribute_exists(pokedex_id)" 
            )
            return Pokemon(**response['Attributes'])
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print(f"Pokémon no encontrado: {pokedex_id}")
            else:
                print(f"Error al actualizar item: {e}")
            return None
    def delete_pokemon(self, pokedex_id: int) -> bool:
        try:
            self.table.delete_item(
                Key={'pokedex_id': pokedex_id},
                ConditionExpression="attribute_exists(pokedex_id)"
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print(f"Pokémon no encontrado: {pokedex_id}")
            else:
                print(f"Error al eliminar item: {e}")
            return False