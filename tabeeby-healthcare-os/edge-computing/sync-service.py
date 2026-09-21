"""
TABEEBY Edge Sync Service
Syncs data between edge nodes and central cloud
"""
import asyncio
import aiohttp
import json
from datetime import datetime

class EdgeSyncService:
    def __init__(self, central_url, sync_interval=300):
        self.central_url = central_url
        self.sync_interval = sync_interval
        self.local_queue = []

    async def sync_loop(self):
        while True:
            try:
                await self._sync_batch()
                await asyncio.sleep(self.sync_interval)
            except Exception as e:
                print(f"[Edge Sync] Error: {e}. Retrying in 60s...")
                await asyncio.sleep(60)

    async def _sync_batch(self):
        if not self.local_queue:
            return

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.central_url}/api/v1/edge/sync",
                json={"batch": self.local_queue}
            ) as resp:
                if resp.status == 200:
                    self.local_queue = []
                    print(f"[Edge Sync] {len(self.local_queue)} records synced")

    def queue_data(self, data):
        self.local_queue.append({
            **data,
            "timestamp": datetime.utcnow().isoformat(),
            "edge_node_id": "edge-001"
        })

if __name__ == "__main__":
    service = EdgeSyncService("https://api.tabeeby.health")
    asyncio.run(service.sync_loop())
