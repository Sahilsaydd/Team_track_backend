from pydantic import BaseModel, Field ,field_validator
from typing import List, Optional



class GroupMemberSchema(BaseModel):
    user_id: int = Field(
        ...,
        example=1
    )

    role_in_group: str = Field(
        ...,
        example="Member"
    )

    note: Optional[str] = Field(
        None,
        example="Backend Team Member"
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


class UpdateGroupSchema(BaseModel):
    name:str = Field(...,min_length=3,max_length=100,description="Group Name")
    description:str = Field(..., min_length=5 , max_length=500 ,description="Group Description")
    profile_pic:str | None =None
    is_active:bool 
    @field_validator("name")
    @classmethod
    def validate_name(cls ,value:str):
        value = value.strip()

        if not value:
            raise ValueError("Group Name Cannot Be Empty")
        
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls ,value:str):
        value = value.strip()
        if not value:
            raise ValueError("Group Description  Cannot Be Empty")

        return value
    