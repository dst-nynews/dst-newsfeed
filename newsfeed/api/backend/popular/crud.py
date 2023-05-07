""" CRUD operations for this endpoint.

Wrap in Python functions the CRUD operations interacting with the DB.
"""

# Local imports
from .database import mongodb

# Connection to the collection related to this endpoint
# popular_collection = mongodb.get_collection("SearchMostPopular")
popular_collection = mongodb.get_collection("Populars")  # for tests


# Helper function for parsing the results from a database query into a Python dict.
def popular_helper(popular) -> dict[str, str]:
    return {
        "id": str(popular["_id"]),
        "most_popular_type": popular["most_popular_type"],
        "search_period": popular["search_period"],
        "search_month": popular["search_month"],
        "search_day": popular["search_day"],
        "created_at": popular["created_at"],
        "Articles": popular["Articles"],
    }


# Retrieve all group of popular articles present in the database.
async def read_popular_index() -> list[dict]:
    populars = []
    async for popular in popular_collection.find():
        populars.append(popular_helper(popular))
    return populars


# Retrieve a group of popular articles with a matching ID.
async def read_popular(id: str) -> dict | None:
    popular = await popular_collection.find_one({"_id": id})
    if popular:
        return popular_helper(popular)


# Add a new group of popular articles  into to the database.
async def create_popular(popular_data: dict) -> dict[str, str]:
    popular = await popular_collection.insert_one(popular_data)
    created_popular = await popular_collection.find_one({"_id": popular.inserted_id})
    return popular_helper(created_popular)


# Update a group of popular articles with a matching ID.
async def update_popular(id: str, data: dict) -> bool:
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    popular = await popular_collection.find_one({"_id": id})
    if popular:
        updated_popular = await popular_collection.update_one(
            {"_id": id}, {"$set": data}
        )
        if updated_popular:
            return True
        return False


# Delete a group of popular articles from the database.
async def delete_popular(id: str) -> bool:
    popular = await popular_collection.find_one({"_id": id})
    if popular:
        await popular_collection.delete_one({"_id": id})
        return True
