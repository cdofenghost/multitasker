from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime

from ..models.task import Task
from ..schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from .users import UserRepository, UserService

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_task(self, project_id: int, user_id: int, schema: TaskCreateSchema) -> Task:
        return Task(name=schema.name,
                    description=schema.description,
                    performer_id=schema.performer_id,
                    author_id=user_id,
                    project_id=project_id,
                    deadline=schema.deadline,
                    date_created=datetime.now(),
                    date_updated=datetime.now(),
                    status=1,
                    priority=schema.priority)

    def __to_task_schema(self, task: Task) -> TaskSchema:
        return TaskSchema(id=task.id,
                          name=task.name,
                          author_id=task.author_id,
                          performer_id=task.performer_id,
                          project_id=task.project_id,
                          deadline=task.deadline,
                          date_created=task.date_created,
                          date_updated=task.date_updated,
                          priority=task.priority,
                          status=task.status,
                          description=task.description)
    
    def add_task(self, project_id: int, user_id: int, task_schema: TaskCreateSchema) -> TaskSchema:
        task = self.__to_task(project_id=project_id, user_id=user_id, schema=task_schema)

        self.db.add(task)
        self.db.commit()

        return self.__to_task_schema(task)

    def find_task(self, task_id: int) -> TaskSchema:
        task = self.db.query(Task).filter(Task.id == task_id).first()

        if task is None:
            return NoResultFound()
        
        return self.__to_task_schema(task)
    
    def get_tasks(self) -> list[TaskSchema]:
        return [self.__to_task_schema(task)
                for task in self.db.query(Task).all()]

    def get_allocated_tasks(self, user_id: int) -> list[TaskSchema]:
        return [self.__to_task_schema(task)
                for task in self.db.query(Task).filter(Task.performer_id == user_id)]
    
    def get_authored_tasks(self, user_id: int) -> list[TaskSchema]:
        return [self.__to_task_schema(task)
                for task in self.db.query(Task).filter(Task.author_id == user_id)]

    def get_project_tasks(self, project_id: int) -> list[Task]:
        return [self.__to_task_schema(task) 
                for task in self.db.query(Task).filter(Task.project_id == project_id)]
    
    def remove_task(self, id: int) -> Task | None:
        task = self.find_task(id)
        
        self.db.query(Task).filter(task.id == id).delete()
        self.db.commit()

        return self.__to_task_schema(task)
    
    def update_task(self, task: TaskUpdateSchema) -> TaskSchema:
        
        self.db.merge(task)
        self.db.commit()

        return self.__to_task_schema(task)

    def check_project_ownership(self, user_id: int, project_id: int) -> bool:
        from ..models.project import Project
        from ..models.category import Category
        project = self.db.query(Project).filter(Project.id == project_id).first()

        if project is None:
            return False
        
        category = self.db.query(Category).filter(Category.id == project.category_id,
                                                  Category.user_id == user_id).first()
        
        print(f"Ownership: {False if category is None else True}")
        return False if category is None else True

    def check_task_ownership(self, user_id: int, task_id: int) -> bool:
        task_author = self.db.query(Task).filter(Task.id == task_id).first()
        
        # project = self.db.query(Project).filter(Project.id == task.project_id).first()

        # if project is None:
        #     return False
        
        # category = self.db.query(Category).filter(Category.id == project.category_id,
        #                                           Category.user_id == user_id).first()
        
        return False if task_author is None else True
    
    def is_user_in_project(self, user_id: int, task_id: int) -> bool:
        from ..models.project import Project
        task = self.db.query(Task).filter(Task.id == task_id).first()

        if task is None:
            return False
        
        project = self.db.query(Project).filter(Project.id == task.project_id)

        if project is None:
            return False
        
        

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def add_task(self, project_id: int, user_id: int, task_data: TaskCreateSchema) -> TaskSchema:
        user_is_owner = self.check_project_ownership(user_id, project_id)

        if task_data.performer_id == -1:
            task_data.performer_id = user_id
        
        if not user_is_owner:
            raise PermissionError()

        return self.task_repository.add_task(project_id=project_id, user_id=user_id, task_schema=task_data)

    def get_task(self, user_id: int, task_id: int) -> TaskSchema:
        task = self.task_repository.find_task(task_id)
        
        user_is_owner = self.check_project_ownership(user_id, task.project_id)

        if not user_is_owner:
            raise PermissionError()
        
        return task
    
    def get_project_tasks(self, user_id: int, project_id: int) -> list[TaskSchema]:
        user_is_owner = self.check_project_ownership(user_id, project_id)
        
        if not user_is_owner:
            return None
        
        return self.task_repository.get_project_tasks(project_id)
    
    def remove_task(self, user_id: int, task_id: int) -> TaskSchema:
        task = self.get_task(user_id, task_id)

        if task is None:
            return None
        
        return self.task_repository.remove_task(task_id)

    def update_task(self, user_id: int, task_id: int, task_data: TaskUpdateSchema) -> Task | None:
        task = self.get_task(user_id, task_id)

        if task is None:
            return None
        
        task.performer_id=task_data.performer_id
        task.name=task_data.name, 
        task.description=task_data.description,
        task.performer_id=task_data.performer_id,
        task.deadline=task_data.deadline,
        task.priority=task_data.priority,
        
        return self.task_repository.update_task(task)

    def check_project_ownership(self, user_id: int, project_id: int) -> bool:
        return self.task_repository.check_project_ownership(user_id, project_id)
    
    def check_task_ownership(self, user_id: int, task_id: int) -> bool:
        return self.task_repository.check_task_ownership(user_id, task_id)

    def set_performer(self, task_id: int, performer_id: int) -> TaskSchema:
        task = self.task_repository.find_task(task_id)
        
        task.performer_id = performer_id
        
        return self.task_repository.update_task(task)
    
    def get_allocated_tasks(self, user_id: int) -> list[TaskSchema]:
        return self.task_repository.get_allocated_tasks(user_id)
    
    def get_authored_tasks(self, user_id: int) -> list[TaskSchema]:
        return self.task_repository.get_authored_tasks(user_id)