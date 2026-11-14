from datetime import UTC,datetime
from uuid import uuid4
from typing import Protocol
from pymongo.collection import Collection
class PlannerRepository(Protocol):
 def create(self,owner_id:str,data:dict)->dict:...
 def list_for_owner(self,owner_id:str)->list[dict]:...
class InMemoryPlannerRepository:
 def __init__(self):self.records=[]
 def create(self,owner_id,data):
  record={"_id":str(uuid4()),"owner_id":owner_id,**data,"created_at":datetime.now(UTC)};self.records.append(record);return record.copy()
 def list_for_owner(self,owner_id):return [x.copy() for x in self.records if x["owner_id"]==owner_id]
class MongoPlannerRepository:
 def __init__(self,c:Collection):self.c=c;self.c.create_index([("owner_id",1),("planned_at",1)])
 def create(self,owner_id,data):
  r={"_id":str(uuid4()),"owner_id":owner_id,**data,"created_at":datetime.now(UTC)};self.c.insert_one(r);return r
 def list_for_owner(self,owner_id):return list(self.c.find({"owner_id":owner_id}).sort("planned_at",1))
