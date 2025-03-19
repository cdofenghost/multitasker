from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .categories import CategoryRepository, CategoryService
from ..database import get_db
from ..schemas.category import CategoryCreateSchema, CategoryUpdateSchema

router = APIRouter(prefix="/categories")

# user_codes = {
#     # "user_email": "code"
# }

def get_category_repository(db: Session = Depends(get_db)):
    return CategoryRepository(db)

def get_category_service(user_repository: CategoryRepository = Depends(get_category_repository)):
    return CategoryService(user_repository)


@router.post("/add",
             tags=["Categories"])
async def add_category(category_data: CategoryCreateSchema, 
                       service: CategoryService = Depends(get_category_service)):
    category = service.add_category(category_data)

    return {"id": category.id, "name": category.name, "color": category.color}


@router.put("/update", 
            tags=["Categories"])
async def update_category(category_id: int, 
                          category_data: CategoryUpdateSchema, 
                          service: CategoryService = Depends(get_category_service)):
    category = service.update_category(category_id, category_data)

    if category is None:
        raise HTTPException(status_code=404, detail="Не удалось обновить категорию - такой категории нет/уже удалена")

    return {"id": category.id, "name": category.name, "color": category.color}


@router.delete("/delete",
             tags=["Categories"])
async def delete_category(category_id: int, 
                          service: CategoryService = Depends(get_category_service)):
    category = service.remove_category(category_id)

    if category is None:
        raise HTTPException(status_code=404, detail="Не удалось удалить категорию - такой категории нет/уже удалена")
    
    return {"message": f"Категория '{category.name}' была удалена"}
