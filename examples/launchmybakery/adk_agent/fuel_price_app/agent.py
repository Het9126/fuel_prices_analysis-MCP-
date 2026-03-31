import os
import dotenv
from fuel_price_app import tools
from google.adk.agents import LlmAgent

dotenv.load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'project_not_set')

maps_toolset = tools.get_maps_mcp_toolset()
bigquery_toolset = tools.get_bigquery_mcp_toolset()

# Ensure we only pass valid toolsets
active_toolsets = [t for t in [maps_toolset, bigquery_toolset] if t is not None]

root_agent = LlmAgent(
    model='gemini-1.5-pro', # Switching to the stable model for better tool calling
    name='fuel_price_agent',
    instruction=f"""
                Help the user answer questions about global fuel prices (Petrol, Diesel, LPG) by strategically combining insights from two sources:
                
                1.  **BigQuery toolset:** Access fuel price data in the 'fuel_prices_analysis' dataset within project '{PROJECT_ID}'. 
                    - Table 'petrol_prices': Global petrol prices with consumption and world share.
                    - Table 'diesel_prices': Historical diesel prices (monthly) for various countries.
                    - Table 'lpg_prices': Historical LPG prices (monthly) for various countries.
                    
                    **IMPORTANT:** 
                    - Always use fully qualified table names: `{PROJECT_ID}.fuel_prices_analysis.petrol_prices`, `{PROJECT_ID}.fuel_prices_analysis.diesel_prices`, or `{PROJECT_ID}.fuel_prices_analysis.lpg_prices`.
                    - Use the `list_tables` and `get_table_schema` (or `describe_table`) tools to understand the exact column names before querying.
                    - The `diesel_prices` and `lpg_prices` tables have many columns named after months/years (e.g., 'Dec_15', 'Jan_16').
                    - Run all query jobs from project id: {PROJECT_ID}. 

                2.  **Maps Toolset:** Use this for real-world location analysis, finding gas stations, or calculating routes related to fuel logistics.
                    Include a hyperlink to an interactive map in your response where appropriate.
            """,
    tools=active_toolsets
)

