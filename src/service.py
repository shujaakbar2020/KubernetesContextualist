from kubernetes_asyncio import client, config
from kubernetes_asyncio.client.rest import ApiException

class K8sService:
    def __init__(self):
        self._initialized = False

    async def initialize(self):
        if not self._initialized:
            try:
                await config.load_kube_config()
            except:
                config.load_incluster_config()
            self._initialized = True

    async def get_pods(self, namespace: str):
        await self.initialize()
        async with client.ApiClient() as api:
            v1 = client.CoreV1Api(api)
            return await v1.list_namespaced_pod(namespace)

async def read_logs(
        self, 
        pod_name: str, 
        namespace: str, 
        tail_lines: int = 100, 
        container: str = None,
        previous: bool = False
    ) -> str:
        await self.initialize()
        async with client.ApiClient() as api:
            v1 = client.CoreV1Api(api)
            try:
                # Use read_namespaced_pod_log for the raw log string
                logs = await v1.read_namespaced_pod_log(
                    name=pod_name,
                    namespace=namespace,
                    container=container,
                    tail_lines=tail_lines,
                    previous=previous
                )
                return logs
            except Exception as e:
                return f"Error reading logs: {str(e)}"
