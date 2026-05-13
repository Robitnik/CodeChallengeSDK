import logging
from time import sleep

from sdk_challenge import api_client
from tests.debug_helpers import debug_print

ONE_PIECE_ID = 21
INVALID_ANIME_ID = 999999


def test_get_anime_info_valid() -> None:
    client = api_client.JikanAPIClient()
    anime_info = client.get_anime_info(ONE_PIECE_ID)  # One Piece ID
    debug_print(f"Anime info for ID {ONE_PIECE_ID}: {anime_info}")
    assert anime_info["data"]["title"] == "One Piece", "Anime title does not match expected value."


def test_get_anime_info_invalid() -> None:
    client = api_client.JikanAPIClient()
    try:
        client.get_anime_info(INVALID_ANIME_ID)
    except Exception as exc:
        debug_print(f"Error response for invalid ID {INVALID_ANIME_ID}: {exc}")
        assert "404" in str(exc), "Expected 404 error for non-existent anime ID."


def test_search_anime() -> None:
    client = api_client.JikanAPIClient()
    sleep(1)  # Avoid hitting API rate limits
    search_results = client.search_anime("Naruto")
    debug_print(f"Search results for 'Naruto': {search_results}")
    assert len(search_results["data"]) > 0, "Search results should contain at least one entry."


def test_get_top_anime() -> None:
    client = api_client.JikanAPIClient()
    top_anime = client.get_top_anime()
    debug_print(f"Top anime: {top_anime}")
    assert len(top_anime["data"]) > 0, "Top anime list should contain at least one entry."


if __name__ == "__main__":
    test_get_anime_info_valid()
    test_get_anime_info_invalid()
    test_search_anime()
    test_get_top_anime()
    logging.info("All API tests passed successfully.")
