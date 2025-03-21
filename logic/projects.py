from sqlalchemy.orm import Session

from ..models.project import Project
from ..models.category import Category
from ..schemas.project import ProjectCreateSchema, ProjectUpdateSchema


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_project(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()

        return project

    def find_project(self, project_id: int) -> Project | None:
        return self.db.query(Project).get(project_id)
    
    def get_projects_by_category_id(self, category_id: int) -> list[Project]:
        return list(self.db.query(Project).filter(Project.category_id == category_id))
    
    def remove_project(self, project_id: int) -> Project | None:
        project = self.find_project(project_id)

        if project is None:
            return None
        
        self.db.query(Project).filter(Project.id == project_id).delete()
        self.db.commit()

        return project
    
    def update_project(self, project: Project) -> Project:
        self.db.merge(project)
        self.db.commit()

        return project

    def check_category_ownership(self, user_id: int, category_id: int) -> bool:    
        category = self.db.query(Category).filter(Category.id == category_id,
                                                  Category.user_id == user_id).first()
        
        return False if category is None else True

    def check_project_ownership(self, user_id: int, project_id: int) -> bool:
        project = self.db.query(Project).filter(Project.id == project_id).first()

        if project is None:
            return False
        
        category = self.db.query(Category).filter(Category.id == project.category_id,
                                                  Category.user_id == user_id).first()
        
        return False if category is None else True

class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def __to_project(self, category_id: int, project_data: ProjectCreateSchema) -> Project:
        return Project(name=project_data.name, 
                       description=project_data.description, 
                       icon=project_data.icon,
                       category_id=category_id)

    def add_project(self, user_id: int, category_id: int, project_data: ProjectCreateSchema) -> Project | None:
        user_is_owner = self.check_category_ownership(user_id, category_id)

        if not user_is_owner:
            return None
        
        project = self.__to_project(category_id, project_data)

        return self.project_repository.add_project(project)

    def get_project(self, user_id: int, project_id: int) -> Project | None:
        project = self.project_repository.find_project(project_id)

        if project is None:
            return None
        
        user_is_owner = self.check_category_ownership(project.category_id, user_id)

        if not user_is_owner:
            return None
        
        return project
    
    def get_projects_by_category_id(self, user_id: int, category_id: int) -> list[Project] | None:
        user_is_owner = self.check_category_ownership(user_id, category_id)
        
        if not user_is_owner:
            return None
        
        return self.project_repository.get_projects_by_category_id(category_id)
    
    def remove_project(self, user_id: int, project_id: int) -> Project | None:
        project = self.get_project(user_id, project_id)

        if project is None:
            return None
        
        return self.project_repository.remove_project(project_id)

    def update_project(self, user_id: int, project_id: int, project_data: ProjectUpdateSchema) -> Project | None:
        project = self.get_project(user_id, project_id)

        if project is None:
            return None
        
        project.name = project_data.name
        project.description = project_data.description
        project.icon = project_data.icon
        
        return self.project_repository.update_project(project)

    def check_category_ownership(self, user_id: int, category_id: int) -> bool:
        return self.project_repository.check_category_ownership(user_id, category_id)
    
    def check_project_ownership(self, user_id: int, project_id: int) -> bool:
        return self.project_repository.check_project_ownership(user_id, project_id)