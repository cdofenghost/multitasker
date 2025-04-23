from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .users import UserSchema
from .categories import CategoryRepository, CategoryService
from ..database import get_db
from ..schemas.category import CategoryCreateSchema, CategoryUpdateSchema, CategorySchema
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

@router.post("/", response_model=CategorySchema, status_code=201)
async def add_category(category_data: CategoryCreateSchema, 
                       service: ServiceDependency,
                       user: UserDependency):
    category = service.add_category(user.id, category_data)

    return category


@router.put("/", response_model=CategorySchema)
async def update_category(category_id: int, 
                          category_data: CategoryUpdateSchema, 
                          service: ServiceDependency,
                          user: UserDependency):
    try:
        category = service.update_category(category_id, category_data)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Не удалось обновить категорию - такой категории нет/уже удалена")

    return category


@router.get("/all", response_model=list[CategorySchema])
async def get_all_user_categories(service: ServiceDependency,
                                  user: UserDependency):
    categories = service.get_categories_by_user_id(user.id)

    return categories


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(category_id: int,
                       service: ServiceDependency,
                       user: UserDependency):
    try:
        category = service.get_category(category_id)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Категория с таким ID не была найдена")
    
    return category


@router.get("/count/projects", response_model=int)
async def get_projects_count(category_id: int,
                          service: ServiceDependency,
                          user: UserDependency):
    return service.get_projects_count(category_id)


@router.delete("/", status_code=204)
async def delete_category(category_id: int, 
                          service: ServiceDependency,
                          user: UserDependency,
                          response: Response):
    if not service.check_category_id(user.id, category_id):
        raise HTTPException(status_code=403, detail="Неправомерное удаление данных")
    
    try:
        category = service.remove_category(category_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Запрашиваемый на удаление пользователь не найден/уже удален")