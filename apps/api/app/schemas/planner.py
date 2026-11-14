from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
Status=Literal["idea","draft","ready","scheduled","published","archived"]
class PlanRequest(BaseModel): title:str=Field(min_length=1,max_length=160); planned_at:datetime|None=None; status:Status="idea"
class PlanResponse(PlanRequest): id:str; created_at:datetime
