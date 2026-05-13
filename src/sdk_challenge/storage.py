"""In-memory storage for anime data."""
import logging
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class AnimeInfo:
    """Domain object describing a single anime entry."""

    mal_id: int
    title: str
    rating: float
    year: int
    synopsis: str
    season: str


class AnimeInfoStorage:
    """In-memory dictionary-backed storage with full CRUD support."""

    def __init__(self) -> None:
        self.storage: Dict[int, AnimeInfo] = {}

    def save(self, mal_id: int, anime_data: AnimeInfo) -> None:
        """Save anime information to the storage.

        Args:
            mal_id (int): The unique identifier for the anime.
            anime_data (AnimeInfo): The anime information to be saved.
        """
        self.storage[mal_id] = anime_data

    def load(self, mal_id: int) -> Optional[AnimeInfo]:
        """Load anime information from the storage.

        Args:
            mal_id (int): The unique identifier for the anime.

        Returns:
            AnimeInfo: The anime information if found, else None.
        """
        return self.storage.get(mal_id)

    def update(self, mal_id: int, anime_data: AnimeInfo) -> None:
        """Update existing anime information in the storage.

        Args:
            mal_id (int): The unique identifier for the anime.
            anime_data (AnimeInfo): The updated anime information.
        """
        if self.storage.get(mal_id):
            self.storage[mal_id] = anime_data

    def delete(self, mal_id: int) -> None:
        """Delete anime information from the storage.

        Args:
            mal_id (int): The unique identifier for the anime.
        """
        self.storage.pop(mal_id, None)

    def get_all(self) -> Dict[int, AnimeInfo]:
        """Get all anime information stored.

        Returns:
            Dict[int, AnimeInfo]: A dictionary of all stored anime information.
        """
        return self.storage

    def print_storage(self, mal_id: Optional[int] = None) -> None:
        """Print the anime information stored in the storage.

        Args:
            mal_id (int, optional): The unique identifier for the anime. If None, prints all anime information.
        """
        if mal_id:
            anime_data = self.storage.get(mal_id, None)
            if anime_data:
                logging.info("Anime ID: %s, Info: %s", mal_id, anime_data)
                return
            else:
                logging.info("No anime found with ID: %s", mal_id)
                return
        for stored_id, anime_data in self.storage.items():
            logging.info("Anime ID: %s, Info: %s", stored_id, anime_data)
