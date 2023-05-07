"""Fetch data from the Times Newswire API.

The Times Newswire API provides an up-to-the-minute stream of published articles.
ref: https://developer.nytimes.com/docs/timeswire-product/1/overview
"""

import datetime as dt
import json
import os

import requests


class ApiNames:
    # Define all URLs that are needed
    BASE_URL = "https://api.nytimes.com/svc"

    # endpoint Archive
    BASE_ARCHIVE = BASE_URL + "/archive/v1"
    # endpoint Article Search
    BASE_ARTICLE_SEARCH = BASE_URL + "/search/v2/articlesearch.json"
    # endpoint Most Popular
    BASE_POPULAR = BASE_URL + "/mostpopular/v2"
    BASE_POPULAR_EMAILED = BASE_POPULAR + "/emailed"
    BASE_POPULAR_SHARED = BASE_POPULAR + "/shared"
    BASE_POPULAR_VIEWED = BASE_POPULAR + "/viewed"
    # endpoint Top Stories
    BASE_TOP_STORIES = BASE_URL + "/topstories/v2"
    # endpoint Times Wire
    BASE_WIRE = BASE_URL + "/news/v3/content"
    BASE_WIRE_LATEST = BASE_WIRE + ".json"
    BASE_WIRE_SECTION_LIST = BASE_WIRE + "/section-list.json"

    # endpoint Semantic
    BASE_SEMANTIC = BASE_URL + "/semantic/v2/concept"
    BASE_SEMANTIC_NAME = BASE_SEMANTIC + "/name"
    BASE_SEMANTIC_SEARCH = BASE_SEMANTIC + "/search.json"
    BASE_SEMANTIC_TAGS = BASE_SEMANTIC + "/suggest"  # replace Times Tags API
    # endpoint Time Tags
    BASE_TAGS = BASE_URL + "/suggest/v1/timestags"  # deprecated

    # endpoint Books
    BASE_BOOKS = BASE_URL + "/books/v3"
    BASE_BOOKS_LIST = BASE_BOOKS + "/lists"
    BASE_BOOKS_LIST_HISTORY = BASE_BOOKS_LIST + "/best-sellers/history.json"
    BASE_BOOKS_LIST_NAMES = BASE_BOOKS_LIST + "/names.json"
    BASE_BOOKS_LIST_OVERVIEW_FULL = BASE_BOOKS_LIST + "/full-overview.json"
    BASE_BOOKS_LIST_OVERVIEW_TOP5 = BASE_BOOKS_LIST + "/overview.json"
    BASE_BOOKS_LIST_LATEST = BASE_BOOKS_LIST + ".json"
    BASE_BOOKS_REVIEWS = BASE_BOOKS + "/reviews.json"
    # endpoint Movie Reviews
    BASE_MOVIE = BASE_URL + "/movies/v2"
    BASE_MOVIE_CRITICS = BASE_MOVIE + "/critics"
    BASE_MOVIE_REVIEWS = BASE_MOVIE + "/reviews"
    BASE_MOVIE_REVIEWS_SEARCH = BASE_MOVIE_REVIEWS + "/search.json"


class ApiNyTimes:
    """Instanciate a connection to the API of the NY Times.

    Attributes:
        API_KEY (str): Credentials required to access the API.
        PATH_STORAGE (str): Path to the storage directory.
        URI (str): Path to the API.
    """

    def __init__(
        self,
        path_storage: str | None,
        uri: str | None,
    ) -> None:
        self.API_KEY = os.environ["NY_API_KEY"]
        self.PATH_STORAGE = (
            path_storage if path_storage is not None else "../../data/raw/"
        )
        self.URI = uri

    def _get_data(
        self,
        url: str,
        payload: dict[str, str] | None,
    ) -> dict[str, str]:
        """GET request to an endpoint of the API.

        Args:
            url (str): Url path to the endpoint, including path parameters.
            payload (dict[str, str] | None): Query parameters of the request.

        Returns:
            dict[str, str]: Response as a JSON.
        """

        params = {"api-key": self.API_KEY}
        if payload:
            params.update(payload)
        response = requests.get(url=url, params=params, timeout=(10, 30))
        # print(response.status_code)
        return response.json()

    def _save_data(
        self,
        data: dict[str, str],
        filename: str,
    ) -> None:
        """Save fetched data in a new file located in the storage directory.

        Args:
            data (dict[str, str]): Data fetched from the request to the API.
            filename (str): Filename for the data saved.
        """

        path_file = self.PATH_STORAGE + filename
        with open(path_file, "w") as file:
            json.dump(data, file)


class MostPopular(ApiNyTimes):
    """Instanciate a connection to fetch data from an endpoint of the API NY Times.

    Attributes:
        endpoints (list[str]): List of possible endpoints for this API.
    """

    def __init__(self) -> None:
        self.URI = ApiNames.BASE_POPULAR
        self.endpoints = {
            "emailed": ApiNames.BASE_POPULAR_EMAILED,
            "shared": ApiNames.BASE_POPULAR_SHARED,
            "viewed": ApiNames.BASE_POPULAR_VIEWED,
        }

    def get_content(self, endpoint: str, period: int) -> dict[str, str]:
        """GET request to an endpoint of the API.

        Args:
            endpoint (str): The endpoint to call,
                            in ["emailed", "shared", "viewed"].
            period (int): The period of days, in [1, 7, 30].

        Returns:
            dict[str, str]: Response as a JSON.
        """

        url = endpoint + f"/{period}.json"
        return self._get_data(url)

    def get_emailed(self, period: int) -> dict[str, str]:
        url = self.endpoints["emailed"] + f"/{period}.json"
        return self._get_data(url)

    def get_shared(self, period: int) -> dict[str, str]:
        url = self.endpoints["shared"] + f"/{period}.json"
        return self._get_data(url)

    def get_viewed(self, period: int) -> dict[str, str]:
        url = self.endpoints["viewed"] + f"/{period}.json"
        return self._get_data(url)

    def save_content(self, data: dict[str, str], endpoint: str, period: int) -> None:
        _today = dt.date.today()
        filename = f"most_popular_{endpoint}_{period}d_{_today.month}_{_today.day}.json"
        return self._save_data(data=data, filename=filename)


class TimesWire(ApiNyTimes):
    """Instanciate a connection to fetch data from an endpoint of the API NY Times.

    Attributes:
        endpoints (list[str]): List of possible endpoints for this API.
        sections (dict[str, str]): All possible sections for the content.
    """

    def __init__(self) -> None:
        self.URI = ApiNames.BASE_WIRE
        self.endpoints = {
            "content": ApiNames.BASE_WIRE,
            "latest": ApiNames.BASE_WIRE_LATEST,
            "section_list": ApiNames.BASE_WIRE_SECTION_LIST,
        }
        self.sections = self.get_section_list()

    def get_content(
        self,
        source: str = "all",
        section: str = "all",
    ) -> dict[str, str]:
        """GET request to an endpoint of the API.

        Args:
            source (str, optional): Filter results from [all, nyt, inyt]. Defaults to "all".
            section (str, optional): Filter results from [arts, business, ...]. Defaults to "all".

        Returns:
            dict[str, str]: Response as a JSON.
        """

        url = self.endpoints["content"] + f"/{source}/{section}.json"
        return self._get_data(url)

    def get_latest(self):
        # TODO
        pass

    def get_section_list(self) -> dict[str, str]:
        url = self.endpoints["section_list"]
        return self._get_data(url)

    def save_articles(
        self,
        data: dict[str, str],
        source: str = "all",
        section: str = "all",
    ) -> None:
        """Save fetched data in a new file located in the storage directory.

        Args:
            data (dict[str, str]): Data fetched from the request to the API.
            source (str, optional): Filter results from [all, nyt, inyt]. Defaults to "all".
            section (str, optional): Filter results from [arts, business, ...]. Defaults to "all".
        """

        _timestamp = dt.datetime.now().strftime("%y_%m_%d-%H_%M_%S")
        filename = f"newswire-{_timestamp}-{source}_{section}.json"
        return self._save_data(data, filename)

    def save_latest(self):
        # TODO
        pass

    def save_section_list(self, data: dict[str, str]) -> None:
        filename = "newswire-sections.json"
        return self._save_data(data, filename)


# class Archive(ApiNyTimes):
#     # TODO
#     pass


# class ArticleSearch(ApiNyTimes):
#     # TODO
#     pass


# class Books(ApiNyTimes):
#     # TODO
#     pass


# class MovieReviews(ApiNyTimes):
#     # TODO
#     pass


# class Semantic(ApiNyTimes):
#     # TODO
#     pass


# class TopStories(ApiNyTimes):
#     # TODO
#     pass
