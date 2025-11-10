from pydantic import BaseModel, Field
from typing import Optional

class Pokemon(BaseModel):
    pokedex_id: int = Field(..., gt=0)
    name: str
    pokemon_type: str

class PokemonUpdate(BaseModel):
    name: Optional[str] = None
    pokemon_type: Optional[str] = None