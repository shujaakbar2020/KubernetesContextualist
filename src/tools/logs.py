from mcp.server.fastmcp import FastMCP
from src.service import Kubernetes

def register_log_tools(mcp: FastMCP, k8s: Kubernetes):
    @mcp.tool()
    async def get_pod_logs(
        pod_name: str, 
        namespace: str = "default", 
        tail_lines: int = 100,
        container: str = None,
        previous: bool = False
    ) -> str:
        """
        Fetch logs from a specific Kubernetes pod.
        
        Args:
            pod_name: Name of the pod to fetch logs from.
            namespace: The namespace the pod is in.
            tail_lines: Number of recent log lines to retrieve (default 100).
            container: Name of the container (required if pod has multiple containers).
            previous: If True, gets logs from the previous instance of the container (useful for CrashLoopBackOff).
        """
        return await k8s.read_logs(
            pod_name=pod_name,
            namespace=namespace,
            tail_lines=tail_lines,
            container=container,
            previous=previous
        )
