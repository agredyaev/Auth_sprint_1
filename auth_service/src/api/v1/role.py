# from fastapi import APIRouter, HTTPException, status
# from uuid import UUID
# from typing import List
# from auth_service.src.schemas.role import RoleCreate, RoleUpdate, RoleOut, UserRoleOut
# from auth_service.src.services import get_role_management_service
#
# role_router = APIRouter()
#
#
# @role_router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
# async def create_role(role: RoleCreate):
#     return await get_role_management_service.create_role(role)
#
#
# @role_router.get("/{role_id}", response_model=RoleOut)
# async def get_role(role_id: UUID):
#     role = await get_role_management_service.get_role(role_id)
#     if not role:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
#     return role
#
#
# @role_router.get("/", response_model=List[RoleOut])
# async def get_all_roles():
#     return await get_role_management_service.get_all_roles()
#
#
# @role_router.put("/{role_id}", response_model=RoleOut)
# async def update_role(role_id: UUID, role: RoleUpdate):
#     return await get_role_management_service.update_role(role_id, role)
#
#
# @role_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_role(role_id: UUID):
#     await get_role_management_service.delete_role(role_id)
#     return {"message": "Role deleted"}
#
#
# @role_router.post("/{role_id}/assign/{user_id}", response_model=UserRoleOut)
# async def assign_role_to_user(role_id: UUID, user_id: UUID):
#     return await get_role_management_service.assign_role_to_user(user_id, role_id)
#
#
# @role_router.delete("/{role_id}/remove/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def remove_role_from_user(role_id: UUID, user_id: UUID):
#     await get_role_management_service.remove_role_from_user(user_id, role_id)
#     return {"message": "Role removed from user"}
#
#
# @role_router.get("/check/{user_id}/{role_name}", response_model=bool)
# async def check_user_role(user_id: UUID, role_name: str):
#     return await get_role_management_service.check_user_role(user_id, role_name)
