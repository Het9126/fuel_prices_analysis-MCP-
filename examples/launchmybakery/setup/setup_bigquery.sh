#!/bin/bash

# --- Configuration ---
PROJECT_ID=$(gcloud config get-value project)
DATASET_NAME="fuel_prices_analysis"
LOCATION="US"

# Generate bucket name if not provided as an argument
if [ -z "$1" ]; then
    BUCKET_NAME="gs://fuel-data-storage-$PROJECT_ID"
    echo "No bucket provided. Using default: $BUCKET_NAME"
else
    BUCKET_NAME=$1
fi

echo "----------------------------------------------------------------"
echo "Fuel Data Project Setup"
echo "Project: $PROJECT_ID | Dataset: $DATASET_NAME"
echo "----------------------------------------------------------------"

# 1. Create Google Cloud Storage Bucket
echo "[1/4] Checking Cloud Storage Bucket..."
if gcloud storage buckets describe $BUCKET_NAME >/dev/null 2>&1; then
    echo "      Bucket already exists."
else
    echo "      Creating bucket $BUCKET_NAME..."
    gcloud storage buckets create $BUCKET_NAME --location=$LOCATION
fi

# 2. Upload CSV files to the Bucket
echo "[2/4] Uploading CSV files to $BUCKET_NAME..."
# Note: Ensure your CSV files are in the data/ directory
gcloud storage cp data/Diesel.csv data/LPG.csv data/Petrol.csv $BUCKET_NAME/

# 3. Create BigQuery Dataset
echo "[3/4] Creating BigQuery Dataset..."
if bq show "$PROJECT_ID:$DATASET_NAME" >/dev/null 2>&1; then
    echo "      Dataset already exists."
else    
    bq mk --location=$LOCATION --dataset "$PROJECT_ID:$DATASET_NAME"
fi

# 4. Create Tables
echo "[4/4] Creating BigQuery Tables..."

# --- TABLE 1: petrol_prices ---
# This uses a defined schema to handle specific column names and types
echo "      - Creating table: petrol_prices"
bq query --use_legacy_sql=false \
"CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.petrol_prices\` (
    rank INT64,
    country STRING,
    daily_oil_consumption_barrels INT64,
    world_share STRING,
    yearly_gallons_per_capita FLOAT64,
    price_per_gallon_usd FLOAT64,
    price_per_liter_usd FLOAT64,
    price_per_liter_pkr FLOAT64
);"

bq load --source_format=CSV --skip_leading_rows=1 --replace \
    "$PROJECT_ID:$DATASET_NAME.petrol_prices" "$BUCKET_NAME/Petrol.csv"

# --- TABLE 2: diesel_prices (Autodetect) ---
# Since Diesel.csv has 100+ date columns, we use --autodetect to create the schema automatically
echo "      - Creating table: diesel_prices (Autodetecting 100+ columns)"
bq load --source_format=CSV --autodetect --replace \
    "$PROJECT_ID:$DATASET_NAME.diesel_prices" "$BUCKET_NAME/Diesel.csv"

# --- TABLE 3: lpg_prices (Autodetect) ---
echo "      - Creating table: lpg_prices (Autodetecting 100+ columns)"
bq load --source_format=CSV --autodetect --replace \
    "$PROJECT_ID:$DATASET_NAME.lpg_prices" "$BUCKET_NAME/LPG.csv"

echo "----------------------------------------------------------------"
echo "Setup Complete! Your tables are ready in BigQuery."
echo "----------------------------------------------------------------"
