import sys
import os

# Add the project root (parent directory) to sys.path
# This allows 'from src...' imports to work when running the script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp.server.fastmcp import FastMCP
from src.service import Kubernetes
from src.tools.logs import register_log_tools
from src.tools.pods import register_pod_tools
from src.tools.events import register_event_tools
from src.utils.logger import setup_logging

# Initialize Logging
setup_logging(level="DEBUG")

mcp = FastMCP("K8s-Contextualist")
k8s_service = Kubernetes()

# Register the tools
register_log_tools(mcp, k8s_service)
register_pod_tools(mcp, k8s_service)
register_event_tools(mcp, k8s_service)

if __name__ == "__main__":
    mcp.run()
