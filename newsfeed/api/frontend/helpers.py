""" Helper functions connecting frontend (Streamlit) and backend (FastAPI).
"""

from typing import Dict

import requests
import streamlit as st


class APINames:
    API_BASE = "http://localhost:8000"
    API_ROOT = API_BASE + "/"
    API_POPULAR = API_BASE + "/popular"


def make_clickable_article_title(title: str, url: str) -> str:
    """
    HTML hyperlink to article page
    :param id: article id as string
    :param title: title of article as string
    :return: html <a> with href attribute to make hyperlink
    """
    return f"[{title}]({url})"


@st.cache_data
def _get_json_data(endpoint) -> Dict:
    """Gets relevant JSON data from given FastAPI endpoint."""
    response = requests.get(endpoint)
    response.raise_for_status()
    return response.json()


@st.cache_data
def get_popular_list() -> Dict:
    return _get_json_data(APINames.API_POPULAR)


@st.cache_data
def get_popular(popular_id) -> Dict:
    return _get_json_data(f"{APINames.API_POPULAR}/{popular_id}")
