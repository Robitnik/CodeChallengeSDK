"""Jikan API client for anime data."""
from types import MappingProxyType
from typing import Any, Dict, Mapping

import requests

BASE_HEADERS: Mapping[str, str] = MappingProxyType({
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0",
})


class JikanAPIClient:
    """HTTP client for the Jikan v4 REST API."""

    def __init__(self, base_url: str = "https://api.jikan.moe/v4", timeout: int = 10) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def get_anime_info(self, anime_id: int) -> Dict[str, Any]:
        """
        Get information about a specific anime by its ID.
        Args:
            anime_id (int): The unique identifier for the anime.

        Returns:
            dict: A dictionary with the anime information.
        """
        response = requests.get(f"{self.base_url}/anime/{anime_id}", headers=BASE_HEADERS, timeout=self.timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def search_anime(self, query: str) -> Dict[str, Any]:
        """
        Search for anime based on a query string.
        Args:
            query (str): The search query string.
        Returns:
            dict: A dictionary with the search results.
        """
        response = requests.get(
            f"{self.base_url}/anime",
            params={"q": query},
            headers=BASE_HEADERS,
            timeout=self.timeout,
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def get_top_anime(self) -> Dict[str, Any]:
        """
        Get a list of top anime.
        Returns:
            dict: A dictionary with the top anime information.
        """
        response = requests.get(f"{self.base_url}/top/anime", headers=BASE_HEADERS, timeout=self.timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
