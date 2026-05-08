import logging
import math
from uuid import uuid4

from sdk_challenge import storage
from tests.debug_helpers import debug_print

INITIAL_RATING = 8.5
RELEASE_YEAR = 2016
UPDATED_RATING = 9.0


def test_crud_operations() -> None:
    # Create and save an anime info
    anime_info = storage.AnimeInfo(
        uuid=uuid4(),
        title="My Hero Academia",
        rating=INITIAL_RATING,
        year=RELEASE_YEAR,
        synopsis=(
            "A story about a boy born without superpowers in a world where "
            "they are common, but still dreams of becoming a hero."
        ),
        season="Spring",
    )

    # Initialize storage and save the anime info
    anime_storage = storage.AnimeInfoStorage()

    # Save the anime info and verify it is saved correctly
    anime_storage.save(anime_id=anime_info.uuid, anime_data=anime_info)
    anime_storage.print_storage(anime_id=anime_info.uuid)

    # Load the anime info and verify it
    loaded_anime_info = anime_storage.load(anime_id=anime_info.uuid)
    debug_print(f"Loaded anime info: {loaded_anime_info}")

    # Verify that the loaded anime info matches the saved one
    assert loaded_anime_info == anime_info, "Loaded anime info does not match the saved one."

    # Update the anime info
    loaded_anime_info.rating = UPDATED_RATING
    anime_storage.save(anime_id=anime_info.uuid, anime_data=loaded_anime_info)

    # Load the updated anime info and verify the update
    updated_anime_info = anime_storage.load(anime_id=anime_info.uuid)
    debug_print(f"Updated anime info: {updated_anime_info}")

    # Verify that the rating was updated correctly
    assert updated_anime_info is not None, "Updated anime info should not be None."
    assert math.isclose(updated_anime_info.rating, UPDATED_RATING), "Anime rating was not updated correctly."

    # Delete the anime info
    anime_storage.delete(anime_id=anime_info.uuid)

    # Try to load the deleted anime info and verify it returns None
    deleted_anime_info = anime_storage.load(anime_id=anime_info.uuid)

    # Verify that the deleted anime info returns None
    assert deleted_anime_info is None, "Deleted anime info should return None when loaded."
    debug_print(f"Deleted anime info: {deleted_anime_info}")


if __name__ == "__main__":
    test_crud_operations()
    logging.info("All CRUD operation tests passed successfully.")
