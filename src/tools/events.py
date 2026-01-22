from mcp.server.fastmcp import FastMCP
from src.service import Kubernetes

def register_event_tools(mcp: FastMCP, k8s: Kubernetes):
    @mcp.tool()
    async def cluster_events(namespace: str = "default") -> str:
        """List all pods in a namespace with their current status."""
        try:
            pods = await k8s.get_pods(namespace)
            output = [f"{p.metadata.name} | {p.status.phase}" for p in pods.items]
            return "\n".join(output)
        except Exception as e:
            return f"Error: {str(e)}"
