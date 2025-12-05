import os
from google.cloud import firestore

def get_db():
    database = os.getenv("FIRESTORE_DATABASE")
    if database:
        return firestore.Client(database=database)
    return firestore.Client()
