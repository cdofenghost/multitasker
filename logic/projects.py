from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# from fastapi.exce

# Рейз 
from ..models.project import Project
from ..schemas.project import ProjectCreateSchema, ProjectUpdateSchema, ProjectSchema

# ExceptionHandler

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_project(self, schema: ProjectCreateSchema) -> ProjectSchema:
        return Project(name=schema.name, description=schema.description, icon="testapp/attachments/default-icon.jpg", category_id=schema.category_id)
    
    def add_project(self, project_schema: ProjectCreateSchema) -> ProjectSchema:
        project = self.__to_project(project_schema)

        self.db.add(project)
        self.db.commit()

        return ProjectSchema(id=project.id, name=project.name, description=project.description, icon=project.icon, category_id=project.category_id)

    def find_project(self, project_id: int) -> ProjectSchema:
        project = self.db.query(Project).filter(Project.id == project_id).first()

        if project is None:
            raise NoResultFound()
    
        return ProjectSchema(id=project.id, name=project.name, description=project.description, icon=project.icon, category_id=project.category_id)
    
    def get_projects_by_category_id(self, category_id: int) -> list[ProjectSchema]:
        return [ProjectSchema(id=project.id, name=project.name, description=project.description, icon=project.icon, category_id=project.category_id)
                for project in self.db.query(Project).filter(Project.category_id == category_id)]
    
    def get_tasks_count(self, project_id: int) -> int:
        from ..models.task import Task

        return len(list(self.db.query(Task).filter(Task.project_id == project_id)))
    
    def remove_project(self, project_id: int) -> ProjectSchema:
        project = self.find_project(project_id)
        
        self.db.query(Project).filter(Project.id == project_id).delete()
        self.db.commit()

        return ProjectSchema(id=project.id, name=project.name, description=project.description, icon=project.icon, category_id=project.category_id)
    
    def update_project(self, project_id: int, project_schema: ProjectUpdateSchema) -> ProjectSchema:
        project = self.find_project(project_id)
        
        project.name = project_schema.name
        project.description = project_schema.description

        self.db.merge(project)
        self.db.commit()

        return ProjectSchema(id=project.id, name=project.name, description=project.description, icon=project.icon, category_id=project.category_id)

    def check_category_ownership(self, user_id: int, category_id: int) -> bool:
        from ..models.category import Category

        category = self.db.query(Category).filter(Category.id == category_id,
                                                  Category.user_id == user_id).first()
        
        print(f"Ownership {False if category is None else True}, {user_id=}, {category_id=}")
        return False if category is None else True

    def check_project_ownership(self, user_id: int, project_id: int) -> bool:
        from ..models.category import Category

        project = self.find_project(project_id)
        
        category = self.db.query(Category).filter(Category.id == project.category_id,
                                                  Category.user_id == user_id).first()
        
        return False if category is None else True

class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    # def __get(self, id) -> Project:
    #     res = self.project_repository.get()
    #     if not res:
    #         raise NotImplementedError()
    #     return res

    def add_project(self, user_id: int, category_id: int, project_data: ProjectCreateSchema) -> ProjectSchema:
        user_is_owner = self.check_category_ownership(user_id, category_id)

        if not user_is_owner:
            raise PermissionError()

        return self.project_repository.add_project(project_data)

    def get_project(self, user_id: int, project_id: int) -> ProjectSchema:
        project = self.project_repository.find_project(project_id)
        
        user_is_owner = self.check_category_ownership(user_id, project.category_id)

        if not user_is_owner:
            raise PermissionError()
        
        return project
    
    def get_projects_by_category_id(self, user_id: int, category_id: int) -> list[ProjectSchema]:
        user_is_owner = self.check_category_ownership(user_id, category_id)
        
        if not user_is_owner:
            raise PermissionError()
        
        return self.project_repository.get_projects_by_category_id(category_id)
    
    def get_tasks_count(self, user_id: int, project_id: int) -> int:
        user_is_owner = self.check_project_ownership(user_id, project_id)
        
        return self.project_repository.get_tasks_count(project_id)
    
    def remove_project(self, user_id: int, project_id: int) -> ProjectSchema:
        project = self.get_project(user_id, project_id)
        
        return self.project_repository.remove_project(project_id)

    def update_project(self, user_id: int, project_id: int, project_data: ProjectUpdateSchema) -> ProjectSchema:
        return self.project_repository.update_project(project_id, project_data)

    def check_category_ownership(self, user_id: int, category_id: int) -> bool:
        return self.project_repository.check_category_ownership(user_id, category_id)
    
    def check_project_ownership(self, user_id: int, project_id: int) -> bool:
        return self.project_repository.check_project_ownership(user_id, project_id)