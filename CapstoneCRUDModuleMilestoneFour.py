from pymongo import MongoClient


class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username, password):
        """
        Initialize connection to MongoDB using provided credentials.
        """
        HOST = "localhost"
        PORT = 27017
        DB = "aac"
        COL = "animals"

        try:
            self.client = MongoClient(
                f"mongodb://{username}:{password}@{HOST}:{PORT}/?authSource=aac"
            )

            self.database = self.client[DB]
            self.collection = self.database[COL]

            # Database Enhancement:
            # Create indexes for commonly queried fields
            self.collection.create_index("breed")
            self.collection.create_index("animal_type")
            self.collection.create_index("outcome_type")

        except Exception as e:
            print(f"Connection failed: {e}")

    # ----------------
    # CREATE
    # ----------------
    def create(self, data):

        if not isinstance(data, dict):
            raise TypeError(
                "Data must be a dictionary"
            )

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged

        except Exception as e:
            print(f"Insert failed: {e}")
            return False

    # ----------------
    # READ
    # ----------------
    def read(self, query=None, projection=None):

        if query is None:
            query = {}

        if not isinstance(query, dict):
            raise TypeError(
                "Query must be a dictionary"
            )

        try:

            cursor = self.collection.find(
                query,
                projection
            )

            return list(cursor)

        except Exception as e:
            print(f"Read operation failed: {e}")
            return []

    # ----------------
    # UPDATE
    # ----------------
    def update(self, query, new_values):

        if not query:
            raise ValueError(
                "Query cannot be empty"
            )

        if not new_values:
            raise ValueError(
                "Update values cannot be empty"
            )

        try:

            result = self.collection.update_many(
                query,
                new_values
            )

            return result.modified_count

        except Exception as e:
            print(f"Update failed: {e}")
            return 0

    # ----------------
    # DELETE
    # ----------------
    def delete(self, query):

        if not query:
            raise ValueError(
                "Delete query cannot be empty"
            )

        try:

            result = self.collection.delete_many(
                query
            )

            return result.deleted_count

        except Exception as e:
            print(f"Delete failed: {e}")
            return 0

    # ----------------
    # DATABASE ENHANCEMENTS
    # ----------------

    def search_by_breed(self, breed):

        return self.read(
            {
                "breed": {
                    "$regex": breed,
                    "$options": "i"
                }
            }
        )

    def search_by_outcome(self, outcome):

        return self.read(
            {
                "outcome_type": outcome
            }
        )

    def get_top_breeds(self, limit=10):

        pipeline = [

            {
                "$group": {
                    "_id": "$breed",
                    "count": {
                        "$sum": 1
                    }
                }
            },

            {
                "$sort": {
                    "count": -1
                }
            },

            {
                "$limit": limit
            }
        ]

        return list(
            self.collection.aggregate(
                pipeline
            )
        )