from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from .users import UserSchema
from .categories import CategoryRepository, CategoryService
from ..database import get_db
from ..schemas.category import CategoryCreateSchema, CategoryUpdateSchema
from .tokens import get_current_user

router = APIRouter(prefix="/category", tags=["Categories"])

# user_codes = {
#     # "user_email": "code"
# }

def get_category_repository(db: Session = Depends(get_db)):
    return CategoryRepository(db)

def get_category_service(user_repository: CategoryRepository = Depends(get_category_repository)):
    return CategoryService(user_repository)

ServiceDependency = Annotated[CategoryService, Depends(get_category_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]

@router.post("/")
async def add_category(category_data: CategoryCreateSchema, 
                       service: ServiceDependency,
                       user: UserDependency):
    category = service.add_category(user.id, category_data)

    return {"id": category.id, "name": category.name, "color": category.color}


@router.put("/")
async def update_category(category_id: int, 
                          category_data: CategoryUpdateSchema, 
                          service: ServiceDependency,
                          user: UserDependency):
    category = service.update_category(category_id, category_data)

    if category is None:
        raise HTTPException(status_code=404, detail="Не удалось обновить категорию - такой категории нет/уже удалена")

    return {"id": category.id, "name": category.name, "color": category.color}


@router.get("/all")
async def get_all_user_categories(service: ServiceDependency,
                                  user: UserDependency):
    categories = service.get_categories_by_user_id(user.id)

    return {"categories": categories}


@router.delete("/",
             tags=["Categories"])
async def delete_category(category_id: int, 
                          service: ServiceDependency,
                          user: UserDependency,
                          response: Response):
    if not service.check_category_id(user.id, category_id):
        raise HTTPException(status_code=403, detail="Неправомерное удаление данных")
    
    category = service.remove_category(category_id)

    if category is None:
        raise HTTPException(status_code=404, detail="Не удалось удалить категорию - такой категории нет/уже удалена")
    
    return {"message": f"Категория '{category.name}' была удалена"}
