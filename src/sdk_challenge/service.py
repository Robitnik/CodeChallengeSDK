"""Service layer that fetches anime data and persists it to storage."""
from typing import Any, Dict, Final, List, Optional

from sdk_challenge.api_client import JikanAPIClient
from sdk_challenge.storage import AnimeInfo, AnimeInfoStorage
from sdk_challenge.string_utils import reduce_string

DEFAULT_RATING: Final[float] = float()
DEFAULT_YEAR: Final[int] = 0


class AnimeService:
    """Orchestrates API calls and storage operations for anime data."""

    def __init__(self, client: JikanAPIClient, storage: AnimeInfoStorage) -> None:
        self.client = client
        self.storage = storage

    def fetch_and_store(self, anime_id: int) -> Optional[AnimeInfo]:
        """Fetch anime by ID from the API and save it to storage.

        Args:
            anime_id (int): The Jikan/MyAnimeList anime ID.

        Returns:
            The persisted AnimeInfo on success, or None if the request fails.
        """
        success, anime_info = self.client.get_anime_info(anime_id)
        if not success:
            return None
        anime = self._to_anime_info(anime_info.get("data", {}))
        self.storage.save(anime.mal_id, anime)
        return anime

    def search_and_store(self, query: str) -> List[AnimeInfo]:
        """Search anime by title query and save all results to storage.

        Args:
            query (str): The search query string.

        Returns:
            A list of AnimeInfo objects that were stored.
        """
        success, search_results = self.client.search_anime(query)
        if not success:
            return []
        stored: List[AnimeInfo] = []
        for raw_anime in search_results.get("data", []):
            anime = self._to_anime_info(raw_anime)
            self.storage.save(anime.mal_id, anime)
            stored.append(anime)
        return stored

    def _to_anime_info(self, raw: Dict[str, Any]) -> AnimeInfo:
        """Map a raw Jikan payload item to an AnimeInfo dataclass.

        Args:
            raw (Dict[str, Any]): A single anime entry from the Jikan API.

        Returns:
            AnimeInfo populated from the raw payload, with safe defaults for
            missing or null fields.
        """
        if not raw or not raw.get("mal_id"):
            raise ValueError("Invalid anime data: missing mal_id")
        mal_id = int(raw.get("mal_id", 0))
        # for demo purposes, reduce the synopsis length to 10 characters
        reduced_synopsis = reduce_string(str(raw.get("synopsis") or ""), max_length=10)
        return AnimeInfo(
            mal_id=mal_id,
            title=str(raw.get("title", "")),
            rating=float(raw.get("score") or DEFAULT_RATING),
            year=int(raw.get("year") or DEFAULT_YEAR),
            synopsis=reduced_synopsis,
            season=str(raw.get("season") or ""),
        )
