from sqlalchemy.orm import Session

from ..models.category import Category
from ..schemas.category import Category as CategorySchema


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_category(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()

        return category

    def find_category(self, id: int) -> Category | None:
        return self.db.query(Category).get(id)
    
    def get_categories(self) -> list[Category]:
        return self.db.query(Category).all()
    
    def remove_category(self, id: int) -> Category | None:
        category = self.db.query(Category).get(id)

        if category is None:
            return None
        
        self.db.query(Category).filter(Category.id == id).delete()
        self.db.commit()

        return category
    
    def update_category(self, category: Category) -> Category:
        self.db.merge(category)
        self.db.commit()

        return category


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def __to_category(self, user_id: int, category_data: CategorySchema) -> Category:
        return Category(name=category_data.name, 
                        color=category_data.color, 
                        description=category_data.description,
                        user_id=user_id)

    def add_category(self, user_id: int, category_data: CategorySchema) -> Category | None:
        category = self.__to_category(user_id, category_data)

        return self.category_repository.add_category(category)

    def get_category(self, id: int) -> Category:
        return self.category_repository.find_category(id)
    
    def remove_category(self, id: int) -> Category:
        return self.category_repository.remove_category(id)

    def update_category(self, id: int, category_data: CategorySchema) -> Category | None:
        category = self.category_repository.find_category(id)

        category.name = category_data.name
        category.color = category_data.color
        category.description = category_data.description

        self.category_repository.update_category(category)

        return category
