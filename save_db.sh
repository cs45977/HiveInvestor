#!/bin/bash

# Script to manually save Firestore data to disk
# This sends a POST request to the Firestore Emulator Hub running inside the Vagrant VM.

echo "💾 Triggering Firestore data export..."

vagrant ssh -c "curl -s -X POST http://localhost:4400/emulators/export -d '{\"path\":\"/vagrant/backend/firebase-data\"}'"

echo ""
echo "✅ Data export request sent."
