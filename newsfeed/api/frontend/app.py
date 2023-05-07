import datetime as dt

import streamlit as st

# Local imports
from .helpers import get_popular, make_clickable_article_title

# Page metadata
st.set_page_config(
    page_title="NyNews",
    page_icon="🗞️",
    layout="centered",
    menu_items={"About": "Comment is free 😈 🔮  \n_but facts are sacred_ 😇 🧮"},
)


# Page title
st.title("NyNews 🗽")
st.header("Liste des 20 articles les plus populaires ❤️‍🔥")
st.divider()


# Input form
with st.form("popular_form"):
    metric_form = st.selectbox("Quel filtre ?", ("emailed", "shared", "viewed"))
    _yesterday = dt.date.today() - dt.timedelta(days=1)
    date_form = st.date_input(
        "Quel jour ?",
        value=_yesterday,
        min_value=dt.date(2023, 4, 11),
        max_value=_yesterday,
    )
    # Button to request data from the backend
    submit_btn = st.form_submit_button("Consultez", type="primary")


# Output display
if submit_btn:
    pop_id = f"{metric_form}1d{date_form.month}{date_form.day}"
    response = get_popular(pop_id)
    if response["code"] != 200:
        # Error message (bad input)
        st.markdown(
            "🙈 Désolé, nous n'avons pas pu récupérer la liste des articles **pour cette journée**. 🕳️"
        )
    else:
        # Display each article after reformating it as an hyperlink
        pop_list = response["data"][0]["Articles"]
        for a in pop_list:
            st.markdown(make_clickable_article_title(a["title"], a["url"]))
