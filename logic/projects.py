from sqlalchemy.orm import Session

from ..models.project import Project
from ..schemas.project import ProjectCreateSchema, ProjectUpdateSchema


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_project(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()

        return project

    def find_project(self, id: int) -> Project | None:
        return self.db.query(Project).get(id)
    
    def get_projects(self) -> list[Project]:
        pass
    
    def remove_project(self, id: int) -> Project | None:
        project = self.find_project(id)

        if project is None:
            return None
        
        self.db.query(Project).filter(Project.id == id).delete()
        self.db.commit()

        return project
    
    def update_project(self, project: Project) -> Project:
        self.db.merge(project)
        self.db.commit()

        return project


class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def __to_project(self, project_data: ProjectCreateSchema) -> Project:
        return Project(name=project_data.name, 
                       description=project_data.description, 
                       icon=project_data.icon,
                       category_id=project_data.category_id)

    def add_project(self, project_data: ProjectCreateSchema) -> Project:
        project = self.__to_project(project_data)

        return self.project_repository.add_project(project)

    def get_project(self, id: int) -> Project:
        pass
    
    def remove_project(self, id: int) -> Project | None:
        return self.project_repository.remove_project(id)

    def update_project(self, id: int, project_data: ProjectUpdateSchema) -> Project | None:
        project = self.project_repository.find_project(id)

        if project is None:
            return None
        
        project.name = project_data.name
        project.description = project_data.description
        project.icon = project_data.icon
        
        return self.project_repository.update_project(project)
