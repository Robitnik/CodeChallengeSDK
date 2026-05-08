"""Main entry point for the CodeChallengeSDK."""
import logging
import sys

from sdk_challenge.api_client import JikanAPIClient
from sdk_challenge.service import AnimeService
from sdk_challenge.storage import AnimeInfoStorage

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

ONE_PIECE_ID = 21


def main() -> None:
    """Demonstrate the service layer fetching and storing anime data."""
    client = JikanAPIClient()
    storage = AnimeInfoStorage()
    service = AnimeService(client=client, storage=storage)

    anime = service.fetch_and_store(ONE_PIECE_ID)
    if anime:
        logging.info("Fetched and stored: %s (rating: %s)", anime.title, anime.rating)

    found_results = service.search_and_store("Naruto")
    logging.info("Stored %d results for query 'Naruto'", len(found_results))
    storage.print_storage()


if __name__ == "__main__":
    main()
