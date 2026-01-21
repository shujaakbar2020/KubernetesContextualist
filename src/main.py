from mcp.server.fastmcp import FastMCP
from src.service import K8sService
from src.tools.logs import register_log_tools
from src.tools.pods import register_pod_tools

# Initialize Logging
setup_logging(level="DEBUG")

mcp = FastMCP("K8s-Contextualist")
k8s_service = K8sService()

# Register the tools
register_log_tools(mcp, k8s_service)
register_pod_tools(mcp, k8s_service)

if __name__ == "__main__":
    mcp.run(transport="sse")
