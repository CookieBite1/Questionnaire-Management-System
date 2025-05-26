from app import mongo
import json
import os
from app import mongo
import json

from flask import current_app, g
from pymongo import MongoClient

def clean_document(doc):
    """Removes $oid if exists in _id."""
    if "_id" in doc and isinstance(doc["_id"], dict) and "$oid" in doc["_id"]:
        doc["_id"] = doc["_id"]["$oid"] 
    return doc

def load_collection(file_path, collection_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if isinstance(data, dict):
            data = [data]

        # Clean all documents
        cleaned_data = [clean_document(doc) for doc in data]

        mongo.db[collection_name].drop()  # Drop old collection 
        mongo.db[collection_name].insert_many(cleaned_data)
        print(f"✅ Dropped and loaded {len(cleaned_data)} documents into '{collection_name}' collection.")

def get_db():
    if "db" not in g:
        client = MongoClient(current_app.config["MONGO_URI"])
        g.db_client = client
        g.db = client["UniQ"]  # Το όνομα της βάσης
    return g.db

def close_db(e=None):
    db_client = g.pop("db_client", None)
    if db_client is not None:
        db_client.close()
