"""Fetch data from the Times Newswire API.

The Times Newswire API provides an up-to-the-minute stream of published articles.
ref: https://developer.nytimes.com/docs/timeswire-product/1/overview

Args:
    apikey (str): Credentials.
    endpoint (str): Endpoint to call.
    source (str | None): Filter results, in [all, nyt, inyt].
    section (str | None): Filter results, in [arts, business, ...].

Returns:
    sections (dict[str, str]): List of Sections (length of result: +- 50).
    articles (dict[str, str]): List of Articles (length of result: 500), from the most recently published.
"""

import json
import os
from datetime import datetime
from urllib.parse import urljoin

import requests


class ExtractApiNewsWire:
    def __init__(self, repo_path: str | None) -> None:
        """Instanciate a connection to fetch data from an API of the NY Times.

        Args:
            repo_path (str | None): Path to storage directory.
        """

        # Set paths and credentials
        self.API_KEY = os.environ["NY_API_KEY"]
        self.BASE_URL = os.getenv("BASE_URL", "https://api.nytimes.com/")
        self.repo_path = repo_path
        # data_source = os.environ.get("DATA_SOURCE")  # if a default value is ok
        # data_source = os.environ["DATA_SOURCE"]      # to fail when the conf is missing

    def get_data(
        self, endpoint: str | None, source: str | None, section: str | None
    ) -> dict[str, str]:
        """GET request to an endpoint of the API.

        Args:
            endpoint (str): Endpoint to call.
            source (str | None): Filter results, in [all, nyt, inyt].
            section (str | None): Filter results, in [arts, business, ...].

        Returns:
            dict[str, str]: Response as a JSON.
        """

        # url_path_section_list = "/svc/news/v3/content/section-list.json"
        # url_path_content = f"/svc/news/v3/content/{source}/{section}.json"
        url_path = (
            "/svc/news/v3/content/section-list.json"
            if endpoint
            else f"/svc/news/v3/content/{source}/{section}.json"
        )

        url = urljoin(self.BASE_URL, url_path)
        params = {"api-key": self.API_KEY}

        response = requests.get(url, params=params)
        # print(response.status_code)

        return response.json()

    def save_data(
        self,
        endpoint: str | None,
        source: str | None,
        section: str | None,
        data: dict[str, str],
    ) -> None:
        """Save response in a JSON file.

        Args:
            endpoint (str): Endpoint to call.
            source (str | None): Filter results, in [all, nyt, inyt].
            section (str | None): Filter results, in [arts, business, ...].
            data (dict[str, str]): Response as a JSON.
        """

        _now = datetime.now()
        _timestamp = _now.strftime("%y_%m_%d-%H_%M_%S")
        filename = (
            f"newswire-{_timestamp}"
            + (f"-{endpoint}" if endpoint else "")
            + (f"-{source}" if source else "")
            + (f"-{section}" if section else "")
            + ".json"
        )

        if self.repo_path:
            filepath = self.repo_path + filename
        else:
            filepath = f"../../assets/data/raw/{filename}"

        with open(filepath, "w") as file:
            json.dump(data, file)
        # return data, filename


# if __name__ == "__main__":
#     # Fetch articles (params: endpoint, period, repo_path).

#     import sys

#     endpoint = sys.argv[1]
#     period = int(sys.argv[2])

#     try:
#         api_most_popular = ApiMostPopular(repo_path=sys.argv[3])
#     except IndexError:
#         api_most_popular = ApiMostPopular()

#     query = api_most_popular.get_data(endpoint, period)

#     if query:
#         raw_data_most_popular = api_most_popular.save_data(query, endpoint, period)
#         print("\nArticles récupérés.\n")
#         to_treat = raw_data_most_popular[0]
#         name = raw_data_most_popular[1]

#     # file = "../data/raw_data/most_popular/most_popular_emailed_1d_4_25.json"
#     # to_treat = api_most_popular.import_json(file)
#     # name = api_most_popular.file_name(file)
#     print(name)
#     to_stock = api_most_popular.clean_data(to_treat, name)
#     print(to_stock)
#     api_most_popular.save_clean_data(to_stock, endpoint, period)
