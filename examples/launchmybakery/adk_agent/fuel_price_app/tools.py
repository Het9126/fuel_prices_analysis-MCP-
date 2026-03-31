import os
import dotenv
import google.auth
import google.auth.transport.requests
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams 

# Load environment variables at the top level
dotenv.load_dotenv()

MAPS_MCP_URL = "https://mapstools.googleapis.com/mcp" 
BIGQUERY_MCP_URL = "https://bigquery.googleapis.com/mcp" 

def get_maps_mcp_toolset():
    maps_api_key = os.getenv('MAPS_API_KEY', 'no_api_found')
    
    tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=MAPS_MCP_URL,
            headers={    
                "X-Goog-Api-Key": maps_api_key
            },
            timeout=60.0,          
            sse_read_timeout=300.0
        )
    )
    print("Maps MCP Toolset configured.")
    return tools


def get_bigquery_mcp_toolset():   
    print("Configuring BigQuery MCP Toolset...")
    try:
        # Use a broader scope and explicit project ID
        credentials, project_id = google.auth.default(
                scopes=["https://www.googleapis.com/auth/bigquery", "https://www.googleapis.com/auth/cloud-platform"]
        )

        # In Cloud Run, the environment variable is more reliable
        env_project = os.getenv('GOOGLE_CLOUD_PROJECT')
        final_project = env_project if env_project else project_id
        print(f"Using Project ID for BigQuery: {final_project}")

        # Explicitly refresh the token
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
            
        HEADERS_WITH_OAUTH = {
            "Authorization": f"Bearer {credentials.token}",
            "x-goog-user-project": final_project
        }

        tools = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=BIGQUERY_MCP_URL,
                headers=HEADERS_WITH_OAUTH,
                timeout=120.0,          # 2 minutes to wait for BigQuery
                sse_read_timeout=600.0  # 10 minutes for long data streams
            )
        )
        print("BigQuery MCP Toolset successfully initialized.")
        return tools
    except Exception as e:
        print(f"CRITICAL ERROR in get_bigquery_mcp_toolset: {e}")
        return None