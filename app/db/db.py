from abc import ABC, abstractmethod
from typing import List, Optional
from app.model.pokemon import Pokemon, PokemonUpdate

class DBInterface(ABC):
    @abstractmethod
    def create_pokemon(self, pokemon: Pokemon) -> Pokemon: pass
    @abstractmethod
    def get_pokemon(self, pokedex_id: int) -> Optional[Pokemon]: pass
    @abstractmethod
    def get_all_pokemon(self) -> List[Pokemon]: pass
    @abstractmethod
    def update_pokemon(self, pokedex_id: int, pokemon_data: PokemonUpdate) -> Optional[Pokemon]: pass
    @abstractmethod
    def delete_pokemon(self, pokedex_id: int) -> bool: pass