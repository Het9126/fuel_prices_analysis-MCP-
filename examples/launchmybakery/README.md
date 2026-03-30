# Global Fuel Price Analysis: Google remote MCP demo 

[![Google Cloud](https://img.shields.io/badge/Blog-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services)

This directory contains the data artifacts and infrastructure setup scripts for the **MCP support for BigQuery & Google Maps** demo, focused on analyzing global fuel prices.

## Demo Overview

This scenario demonstrates an AI Agent's ability to orchestrate enterprise data (BigQuery) and real-world geospatial context (Google Maps) to analyze energy markets: 

> **"What are the trends in global fuel prices and how do they compare across regions?"**

The agent autonomously queries BigQuery to find price trends and uses Google Maps to provide real-world context for fuel distribution and logistics. The demo relies on three key datasets:

1.  **Petrol Prices:** Global petrol prices, daily oil consumption, and market share by country.
2.  **Diesel Prices:** Historical monthly diesel prices across multiple countries and currencies.
3.  **LPG Prices:** Historical monthly LPG prices for residential and industrial use.

## Repository Structure

```text
launchmybakery/
├── data/                        # CSV files for BigQuery
│   ├── Petrol.csv
│   ├── Diesel.csv
│   └── LPG.csv
├── adk_agent/                   # AI Agent Application (ADK)
│   └── mcp_bakery_app/          # App directory
│       ├── agent.py             # Agent definition
│       └── tools.py             # Custom tools for the agent
├── setup/                       # Infrastructure setup scripts
│   ├── setup_bigquery.sh        # Script to provision BigQuery dataset and tables
│   └── setup_env.sh             # Script to set up environment variables
├── cleanup/                     # Infrastructure clean up environment
│   ├── cleanup_env.sh           # Script to remove resources in environment
└── README.md                    # This documentation
```

## Deployment Guide

### 1. Authenticate with Google Cloud
```bash
gcloud config set project [YOUR-PROJECT-ID]
gcloud auth application-default login
```

### 2. Configure Environment
```bash
chmod +x setup/setup_env.sh
./setup/setup_env.sh
```

### 3. Provision BigQuery
```bash
chmod +x ./setup/setup_bigquery.sh
./setup/setup_bigquery.sh
```

### 4. Install ADK and Run Agent
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install google-adk==1.28.0
cd adk_agent/
adk web --allow_origins 'regex:https://.*\.cloudshell\.dev'
```

## Sample Questions

*   "Which country has the highest petrol price per liter in USD, and what is their daily oil consumption?"
*   "How has the price of Diesel in Argentina changed between 2023 and 2025?"
*   "Compare the LPG prices in Angola and Bangladesh for the last available month."
*   "Find the 5 closest gas stations in Los Angeles and tell me if they are likely to have competitive pricing based on global trends."
