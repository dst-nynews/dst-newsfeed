""" Instanciate the connection to the DB."""

import os

from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB setup: Async connection with Motor client
# Connection to the cluster
mongo_host = os.getenv("MONGO_CLIENT_HOST")  # Cloud Atlas connection
# mongo_host = os.getenv("MONGO_LOCAL_HOST")  # Local MongoDB connection
mongodb_client = AsyncIOMotorClient(mongo_host)

# Connection to the DB
mongodb = mongodb_client["NYTimes"]
# db_name = os.getenv("MONGO_DB_NAME")
# mongodb = mongodb_client[db_name]
