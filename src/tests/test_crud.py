import logging
import math

from sdk_challenge import storage

ONE_PIECE_ID = 21
INITIAL_RATING = 8.5
RELEASE_YEAR = 1980
UPDATED_YEAR = 1986
UPDATED_RATING = 9.0


def test_create() -> storage.AnimeInfoStorage:
    anime_info = storage.AnimeInfo(
        mal_id=ONE_PIECE_ID,
        title="One Piece",
        rating=INITIAL_RATING,
        year=RELEASE_YEAR,
        synopsis=(
            "A story about a boy born without superpowers in a world where "
            "they are common, but still dreams of becoming a hero."
        ),
        season="Spring",
    )
    anime_storage = storage.AnimeInfoStorage()
    anime_storage.save(mal_id=anime_info.mal_id, anime_data=anime_info)
    return anime_storage


def test_read(anime_storage: storage.AnimeInfoStorage) -> None:
    loaded_anime = anime_storage.load(mal_id=ONE_PIECE_ID)
    assert loaded_anime is not None
    assert loaded_anime.mal_id == ONE_PIECE_ID
    assert loaded_anime.title == "One Piece"
    assert math.isclose(loaded_anime.rating, INITIAL_RATING)
    assert loaded_anime.year == RELEASE_YEAR
    logging.info(f"Read anime: {loaded_anime}")


def test_update(anime_storage: storage.AnimeInfoStorage) -> None:
    loaded_anime = anime_storage.load(mal_id=ONE_PIECE_ID)
    assert loaded_anime is not None
    updated_anime = storage.AnimeInfo(
        mal_id=loaded_anime.mal_id,
        title=loaded_anime.title,
        rating=UPDATED_RATING,
        year=UPDATED_YEAR,
        synopsis=loaded_anime.synopsis,
        season=loaded_anime.season,
    )
    anime_storage.update(mal_id=ONE_PIECE_ID, anime_data=updated_anime)
    reloaded_anime = anime_storage.load(mal_id=ONE_PIECE_ID)
    assert reloaded_anime is not None
    assert math.isclose(reloaded_anime.rating, UPDATED_RATING)
    assert reloaded_anime.year == UPDATED_YEAR
    logging.info(f"Updated anime: {reloaded_anime}")


def test_delete(anime_storage: storage.AnimeInfoStorage) -> None:
    anime_storage.delete(mal_id=ONE_PIECE_ID)
    deleted_anime = anime_storage.load(mal_id=ONE_PIECE_ID)
    assert deleted_anime is None
    logging.info(f"Anime with ID {ONE_PIECE_ID} successfully deleted.")


def test_crud_operations() -> None:
    logging.info(f"Initial items in storage: {len(storage.AnimeInfoStorage().get_all().keys())}")
    anime_storage = test_create()
    test_read(anime_storage)
    test_update(anime_storage)
    logging.info(f"Items in storage after update: {len(anime_storage.get_all().keys())}")
    test_delete(anime_storage)
    logging.info(f"Final items in storage: {anime_storage.get_all()}")


if __name__ == "__main__":
    test_crud_operations()
    logging.info("All CRUD operation tests passed successfully.")
