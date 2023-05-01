"""Fetch data from the Times Newswire API.

The Times Newswire API provides an up-to-the-minute stream of published articles.
ref: https://developer.nytimes.com/docs/timeswire-product/1/overview
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

import requests


class ExtractNewsWire:
    """Instanciate a connection to fetch data from the API Times Newswire of the NY Times.

    Attributes:
        API_KEY (str): Credentials required to access the API.
        URL_BASE (str): Path to the API.
        URL_CONTENT (str): Path to an endpoint.
        URL_SECTION (str): Path to an endpoint.
        STORAGE_PATH (str): Path to the storage directory.
        section_list (Dict[str, str]): All possible sections for the content.
    """

    def __init__(self, storage_path: Optional[str] = None) -> None:
        self.API_KEY = os.environ["NY_API_KEY"]
        self.URL_BASE = os.getenv("URL_BASE", "https://api.nytimes.com")
        self.URL_CONTENT = self.URL_BASE + "/svc/news/v3/content"
        self.URL_SECTION = self.URL_CONTENT + "/section-list.json"
        self.STORAGE_PATH = (
            storage_path if storage_path is not None else "../../assets/data/raw/"
        )
        self.section_list = self.fetch_section_list()

    def _fetch_data(self, url: str) -> Dict[str, str]:
        """GET request to an endpoint of the API.

        Args:
            url (str): Url path to the endpoint, including path parameters.

        Returns:
            Dict[str, str]: Response as a JSON.
        """

        params = {"api-key": self.API_KEY}
        response = requests.get(url, params=params)
        # print(response.status_code)
        return response.json()

    def fetch_articles(
        self,
        source: str = "all",
        section: str = "all",
    ) -> Dict[str, str]:
        """GET request to an endpoint of the API.

        Args:
            source (str, optional): Filter results from [all, nyt, inyt]. Defaults to "all".
            section (str, optional): Filter results from [arts, business, ...]. Defaults to "all".

        Returns:
            Dict[str, str]: Response as a JSON.
        """

        url = self.URL_CONTENT + f"/{source}/{section}.json"
        return self._fetch_data(url)

    def fetch_section_list(self) -> Dict[str, str]:
        """GET request to an endpoint of the API.

        Returns:
            Dict[str, str]: Response as a JSON.
        """

        response = self._fetch_data(self.URL_SECTION)
        return response

    def _save_data(
        self,
        data: Dict[str, str],
        file_name: str,
    ) -> None:
        """Save fetched data in a new file located in the storage directory.

        Args:
            data (Dict[str, str]): Data fetched from the request to the API.
            file_name (str): Filename for the data saved.
        """

        file_path = self.STORAGE_PATH + file_name
        with open(file_path, "w") as file:
            json.dump(data, file)

    def save_articles(
        self,
        data: Dict[str, str],
        source: str = "all",
        section: str = "all",
    ) -> None:
        """Save fetched data in a new file located in the storage directory.

        Args:
            data (Dict[str, str]): Data fetched from the request to the API.
            source (str, optional): Filter results from [all, nyt, inyt]. Defaults to "all".
            section (str, optional): Filter results from [arts, business, ...]. Defaults to "all".
        """

        _timestamp = datetime.now().strftime("%y_%m_%d-%H_%M_%S")
        file_name = f"newswire-{_timestamp}-{source}_{section}.json"
        return self._save_data(data, file_name)

    def save_section_list(self, data: Dict[str, str]) -> None:
        """Save fetched data in a new file located in the storage directory.

        Args:
            data (Dict[str, str]): Data fetched from the request to the API.
        """

        file_name = "newswire-sections.json"
        return self._save_data(data, file_name)
