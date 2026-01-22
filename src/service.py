from kubernetes_asyncio import client, config
from kubernetes_asyncio.client.rest import ApiException

class Kubernetes:
    def __init__(self):
        self._initialized = False

    async def initialize(self):
        if not self._initialized:
            try:
                await config.load_kube_config()
            except:
                await config.load_incluster_config()
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
        try:
            await self.initialize()
            async with client.ApiClient() as api:
                v1 = client.CoreV1Api(api)
                
                kwargs = {
                    "name": pod_name,
                    "namespace": namespace,
                    "tail_lines": tail_lines,
                    "previous": previous
                }
                if container:
                    kwargs["container"] = container

                # Use read_namespaced_pod_log for the raw log string
                logs = await v1.read_namespaced_pod_log(**kwargs)
                return logs
        except ApiException as e:
            return f"Kubernetes API Error: {e.status} {e.reason} - {e.body}"
        except Exception as e:
            return f"Error reading logs: {str(e)}"
