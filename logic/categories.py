from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ..models.category import Category
from ..schemas.category import CategoryCreateSchema, CategoryUpdateSchema, CategorySchema


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_category(self, schema: CategorySchema) -> Category:
        return Category(**schema.model_dump())
    
    def add_category(self, user_id: int, category_schema: CategoryCreateSchema) -> CategorySchema:
        category = self.__to_category(category_schema)
        category.user_id = user_id

        self.db.add(category)
        self.db.commit()

        return CategorySchema(id=category.id, name=category.name, color=category.color, user_id=category.user_id)

    def find_category(self, category_id: int) -> CategorySchema:
        category = self.db.query(Category).filter(Category.id == category_id).first()

        if category is None:
            raise NoResultFound()
        
        return CategorySchema(id=category.id, name=category.name, color=category.color, user_id=category.user_id)
    
    def get_categories_by_user_id(self, user_id: int) -> list[CategorySchema]:
        return [CategorySchema(id=category.id, name=category.name, color=category.color, user_id=category.user_id)
                for category in self.db.query(Category).filter(Category.user_id == user_id)]

    def get_categories(self) -> list[CategorySchema]:
        return self.db.query(Category).all()
    
    def get_projects_count(self, category_id: int) -> int:
        from ..models.project import Project

        return len(list(self.db.query(Project).filter(Project.category_id == category_id)))
    
    def remove_category(self, category_id: int) -> CategorySchema | None:
        category = self.db.query(Category).filter(Category.id == category_id).first()

        if category is None:
            raise NoResultFound()
        
        self.db.query(Category).filter(Category.id == category_id).delete()
        self.db.commit()

        return CategorySchema(id=category.id, name=category.name, color=category.color, user_id=category.user_id)
    
    def update_category(self, category_id: int, category_schema: CategoryUpdateSchema) -> CategorySchema:
        category = self.db.query(Category).filter(Category.id == category_id).first()

        category.name = category_schema.name
        category.color = category_schema.color

        self.db.merge(category)
        self.db.commit()

        return CategorySchema(id=category.id, name=category.name, color=category.color, user_id=category.user_id)


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def add_category(self, user_id: int, category_data: CategoryCreateSchema) -> CategorySchema:
        return self.category_repository.add_category(user_id, category_data)

    def get_category(self, id: int) -> CategorySchema:
        return self.category_repository.find_category(id)
    
    def get_categories_by_user_id(self, user_id: int) -> list[CategorySchema]:
        return self.category_repository.get_categories_by_user_id(user_id)

    def get_projects_count(self, category_id: int) -> int:
        return self.category_repository.get_projects_count(category_id)
    
    def remove_category(self, id: int) -> CategorySchema:
        return self.category_repository.remove_category(id)

    def update_category(self, category_id: int, category_data: CategoryUpdateSchema) -> CategorySchema:
        category = self.category_repository.update_category(category_id, category_data)
        return category

    def check_category_id(self, user_id: int, category_id: int) -> bool:
        categories = self.get_categories_by_user_id(user_id)

        for category in categories:
            print(f"{user_id=}, {category_id=}, {category.id=}")
            if category_id == category.id:
                return True
            
        return False