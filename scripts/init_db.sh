#!/bin/bash

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"gen-lang-client-0437257621"}
DATABASE_ID=${FIRESTORE_DATABASE:-"hiveinvestor"}

echo "Initializing Firestore for Project: $PROJECT_ID, Database: $DATABASE_ID"

TOKEN=$(gcloud auth print-access-token)

for window in "1d" "7d" "30d" "90d"; do
    echo "Creating leaderboard/$window..."
    curl -s -X POST -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        "https://firestore.googleapis.com/v1/projects/$PROJECT_ID/databases/$DATABASE_ID/documents/leaderboards?documentId=$window" \
        -d "{\"fields\": {\"id\": {\"stringValue\": \"$window\"}, \"entries\": {\"arrayValue\": {\"values\": []}}}}" \
        | grep -v "ALREADY_EXISTS" # Suppress error if exists, or handle it
    echo ""
done

echo "Database initialization complete."
