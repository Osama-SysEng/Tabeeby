"""Repository for national-health"""
from typing import Optional, List
class BaseRepository:
    def __init__(self, db=None):
        self.db = db or {}
    def add(self, entity):
        eid = entity.get("id", f"item-{random.randint(1000, 9999)}")
        self.db[eid] = entity
        return eid
    def get(self, eid):
        return self.db.get(eid)
    def list_all(self):
        return list(self.db.values())
    def update(self, eid, data):
        if eid in self.db:
            self.db[eid].update(data)
            return self.db[eid]
        return None
    def delete(self, eid):
        if eid in self.db:
            del self.db[eid]
            return True
        return False
