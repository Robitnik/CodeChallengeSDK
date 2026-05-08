"""In-memory storage for anime data."""
import logging
from dataclasses import dataclass
from typing import Dict, Optional
from uuid import UUID


@dataclass
class AnimeInfo:
    """Domain object describing a single anime entry."""

    uuid: UUID
    title: str
    rating: float
    year: int
    synopsis: str
    season: str


class AnimeInfoStorage:
    """In-memory dictionary-backed storage with full CRUD support."""

    def __init__(self) -> None:
        self.storage: Dict[UUID, AnimeInfo] = {}

    def save(self, anime_id: UUID, anime_data: AnimeInfo) -> None:
        """Save anime information to the storage.

        Args:
            anime_id (str): The unique identifier for the anime.
            anime_data (AnimeInfo): The anime information to be saved.
        """
        self.storage[anime_id] = anime_data

    def load(self, anime_id: UUID) -> Optional[AnimeInfo]:
        """Load anime information from the storage.

        Args:
            anime_id (str): The unique identifier for the anime.

        Returns:
            AnimeInfo: The anime information if found, else None.
        """
        return self.storage.get(anime_id)

    def update(self, anime_id: UUID, anime_data: AnimeInfo) -> None:
        """Update existing anime information in the storage.

        Args:
            anime_id (str): The unique identifier for the anime.
            anime_data (AnimeInfo): The updated anime information.
        """
        if self.storage.get(anime_id):
            self.storage[anime_id] = anime_data

    def delete(self, anime_id: UUID) -> None:
        """Delete anime information from the storage.

        Args:
            anime_id (str): The unique identifier for the anime.
        """
        self.storage.pop(anime_id, None)

    def print_storage(self, anime_id: Optional[UUID] = None) -> None:
        """Print the anime information stored in the storage.

        Args:
            anime_id (str, optional): The unique identifier for the anime. If None, prints all anime information.
        """
        if anime_id:
            anime_data = self.storage.get(anime_id, None)
            if anime_data:
                logging.info("Anime ID: %s, Info: %s", anime_id, anime_data)
                return
            else:
                logging.info("No anime found with ID: %s", anime_id)
                return
        for stored_id, anime_data in self.storage.items():
            logging.info("Anime ID: %s, Info: %s", stored_id, anime_data)
