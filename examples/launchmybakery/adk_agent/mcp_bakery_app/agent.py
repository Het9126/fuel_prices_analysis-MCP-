import os
import dotenv
from mcp_bakery_app import tools
from google.adk.agents import LlmAgent

dotenv.load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'project_not_set')

maps_toolset = tools.get_maps_mcp_toolset()
bigquery_toolset = tools.get_bigquery_mcp_toolset()

root_agent = LlmAgent(
    model='gemini-3.1-pro-preview',
    name='root_agent',
    instruction=f"""
                Help the user answer questions about global fuel prices (Petrol, Diesel, LPG) by strategically combining insights from two sources:
                
                1.  **BigQuery toolset:** Access fuel price data in the 'fuel_prices_analysis' dataset. 
                    - Table 'petrol_prices': Global petrol prices with consumption and world share.
                    - Table 'diesel_prices': Historical diesel prices (monthly) for various countries.
                    - Table 'lpg_prices': Historical LPG prices (monthly) for various countries.
                    Run all query jobs from project id: {PROJECT_ID}. 

                2.  **Maps Toolset:** Use this for real-world location analysis, finding gas stations, or calculating routes related to fuel logistics.
                    Include a hyperlink to an interactive map in your response where appropriate.
            """,
    tools=[maps_toolset, bigquery_toolset]
)

