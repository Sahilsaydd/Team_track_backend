from pydantic import BaseModel, Field
from typing import List, Optional



class GroupMemberSchema(BaseModel):
    user_id: int = Field(
        ...,
        example=1
    )

    role_in_group: str = Field(
        ...,
        example="Lead"
    )

    note: Optional[str] = Field(
        None,
        example="Backend Team Leader"
    )



class CreateGroupSchema(BaseModel):

    name: str = Field(
        ...,
        example="Backend Team"
    )

    description: Optional[str] = Field(
        None,
        example="Handle Backend APIs"
    )

    profile_pic: Optional[str] = Field(
        None,
        example="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    )

    members: List[GroupMemberSchema]



class UpdateGroupSchema(BaseModel):

    name: Optional[str] = Field(
        None,
        example="Backend Team Updated"
    )

    description: Optional[str] = Field(
        None,
        example="Updated Backend Team"
    )

    profile_pic: Optional[str] = Field(
        None,
        example="uploads/groups/new-image.png"
    )

    is_active: Optional[bool] = Field(
        None,
        example=True
    )



class AddMemberSchema(BaseModel):

    group_id: int = Field(
        ...,
        example=1
    )

    members: List[GroupMemberSchema]



class ChangeLeaderSchema(BaseModel):

    group_id: int = Field(
        ...,
        example=1
    )

    new_leader_id: int = Field(
        ...,
        example=5
    )



class RemoveMemberSchema(BaseModel):

    group_id: int = Field(
        ...,
        example=1
    )

    user_id: int = Field(
        ...,
        example=4
    )
