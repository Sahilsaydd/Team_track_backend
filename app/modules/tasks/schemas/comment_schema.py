from pydantic import BaseModel

class TaskCommentSchema(BaseModel):
    id:int
    comment:str
    