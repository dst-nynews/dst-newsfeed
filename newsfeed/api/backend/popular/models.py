""" Models to define the data objects for this endpoint."""

from pydantic import BaseModel, Field, HttpUrl


class PopularArticleModel(BaseModel):
    id: str = Field(..., alias="_id")
    url: HttpUrl = Field(...)
    title: str = Field(...)
    pusblished_date: str = Field(...)
    byline: str = Field(...)
    section: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "nyt://article/5afe40ea-07c7-5c80-842b-f3385c9fb4e5",
                "url": "https://www.nytimes.com/2023/04/05/style/emily-name-popularity.html",
                "title": "It’s Time to Address the Emily in the Room",
                "pusblished_date": "2023-04-05",
                "byline": "By Emilia Petrarca",
                "section": "Style",
            }
        }


# Build ids for an instance of PopularModel (it's a composite from its attributes).
def concat_id(pop_type: str, pop_period: str, pop_month: str, pop_day: str):
    return f"{pop_type}{pop_period}{pop_month}{pop_day}"


class PopularModel(BaseModel):
    most_popular_type: str = Field(...)
    search_period: str = Field(...)
    search_month: str = Field(...)
    search_day: str = Field(...)
    created_at: str = Field(...)
    Articles: list[PopularArticleModel] | None
    id: str = Field(
        default_factory=concat_id(
            most_popular_type, search_period, search_month, search_day
        ),
        alias="_id",
    )

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "emailed7d47",
                "most_popular_type": "emailed",
                "search_period": "7d",
                "search_month": "4",
                "search_day": "7",
                "created_at": "07/04/2023 13:48:22",
                "Articles": [
                    {
                        "_id": "nyt://article/5afe40ea-07c7-5c80-842b-f3385c9fb4e5",
                        "url": "https://www.nytimes.com/2023/04/05/style/emily-name-popularity.html",
                        "title": "It’s Time to Address the Emily in the Room",
                        "pusblished_date": "2023-04-05",
                        "byline": "By Emilia Petrarca",
                        "section": "Style",
                    },
                    {
                        "_id": "nyt://article/dcf4b9da-42ad-5f46-b9a8-c60c699c3d0a",
                        "url": "https://www.nytimes.com/2023/04/01/world/europe/finland-happiness-optimism.html",
                        "title": "The Finnish Secret to Happiness? Knowing When You Have Enough.",
                        "pusblished_date": "2023-04-01",
                        "byline": "By Penelope Colston and Jake Michaels",
                        "section": "World",
                    },
                ],
            }
        }


class UpdatePopularModel(BaseModel):
    most_popular_type: str | None
    search_period: str | None
    search_month: str | None
    search_day: str | None
    created_at: str | None
    Articles: list[PopularArticleModel] | None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "most_popular_type": "emailed",
                "search_period": "7d",
                "search_month": "4",
                "search_day": "7",
                "created_at": "07/04/2023 13:48:22",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message,
    }
