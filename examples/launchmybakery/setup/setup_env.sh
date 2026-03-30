#!/bin/bash

# Get Google Cloud Project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
DATASET_ID="fuel_prices_analysis" # Standardized dataset ID

if [ -z "$PROJECT_ID" ]; then
    echo "Error: Could not determine Google Cloud Project ID."
    echo "Please run 'gcloud config set project <PROJECT_ID>' first."
    exit 1
fi

echo "Found Project ID: $PROJECT_ID"

# Enable necessary APIs
echo "Enabling Google Cloud APIs..."
gcloud services enable \
    aiplatform.googleapis.com \
    apikeys.googleapis.com \
    bigquery.googleapis.com \
    maps-backend.googleapis.com \
    --project=$PROJECT_ID

# Create API Key for Maps
echo "Creating Google Maps Platform API Key..."
API_KEY_NAME="fuel-demo-key-$(date +%s)"
API_KEY=$(gcloud alpha services api-keys create --display-name="$API_KEY_NAME" \
    --api-target=service=maps-backend.googleapis.com \
    --format="value(keyString)")

if [ -z "$API_KEY" ]; then
    echo "Could not automate API key creation."
    read -p "Please enter your Google Maps API Key manually: " API_KEY
fi

# Create .env file in the launchmybakery directory
ENV_FILE=".env" 

cat <<EOF > "$ENV_FILE"
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1

# BigQuery Configuration
BIGQUERY_DATASET_ID=$DATASET_ID

# Maps Configuration
MAPS_API_KEY=$API_KEY
EOF

echo "----------------------------------------------------------------"
echo "Successfully updated $ENV_FILE"
echo "Project: $PROJECT_ID"
echo "Dataset: $DATASET_ID"
echo "----------------------------------------------------------------"