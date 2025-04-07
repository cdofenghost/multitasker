from sqlalchemy.orm import Session

from ..models.project import Project
from ..models.category import Category
from ..models.task import Task
from ..schemas.task import TaskCreateSchema, TaskUpdateSchema
from .users import UserRepository, UserService

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()

        return task

    def find_task(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_tasks(self) -> list[Task]:
        pass

    def get_allocated_tasks(self, user_id: int) -> list[Task]:
        tasks = self.db.query(Task).filter(Task.performer_id == user_id)
        return list(tasks)
    
    def get_authored_tasks(self, user_id: int) -> list[Task]:
        tasks = self.db.query(Task).filter(Task.author_id == user_id)
        return list(tasks)

    def get_project_tasks(self, project_id: int) -> list[Task]:
        return list(self.db.query(Task).filter(Task.project_id == project_id))
    
    def remove_task(self, id: int) -> Task | None:
        task = self.find_task(id)

        if task is None:
            return None
        
        self.db.query(Task).filter(task.id == id).delete()
        self.db.commit()

        return task
    
    def update_task(self, task: Task) -> Task:
        self.db.merge(task)
        self.db.commit()

        return task

    def check_project_ownership(self, user_id: int, project_id: int) -> bool:
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
        task = self.db.query(Task).filter(Task.id == task_id).first()

        if task is None:
            return False
        
        project = self.db.query(Project).filter(Project.id == task.project_id)

        if project is None:
            return False
        
        

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def __to_task(self, user_id: int, project_id: int, task_data: TaskCreateSchema) -> Task:
        return Task(name=task_data.name, 
                    description=task_data.description,
                    author_id=user_id,
                    project_id=project_id,
                    performer_id=task_data.performer_id,
                    deadline=task_data.deadline,
                    priority=task_data.priority,)

    def add_task(self, user_id: int, project_id: int, task_data: TaskCreateSchema) -> Task | None:
        user_is_owner = self.check_project_ownership(user_id, project_id)

        if not user_is_owner:
            return None
        
        task = self.__to_task(user_id, project_id, task_data)

        return self.task_repository.add_task(task)

    def get_task(self, user_id: int, task_id: int) -> Task:
        task = self.task_repository.find_task(task_id)

        if task is None:
            return None
        
        user_is_owner = self.check_project_ownership(user_id, task.project_id)

        if not user_is_owner:
            return None
        
        return task
    
    def get_project_tasks(self, user_id: int, project_id: int) -> list[Task]:
        user_is_owner = self.check_project_ownership(user_id, project_id)
        
        if not user_is_owner:
            return None
        
        return self.task_repository.get_project_tasks(project_id)
    
    def remove_task(self, user_id: int, task_id: int) -> Task | None:
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

    def set_performer(self, task_id: int, performer_id: int) -> Task | dict:
        task = self.task_repository.find_task(task_id)
        
        if task is None:
            return {'error_code': 404, 'detail': 'Такой таски не существует!'}
        
        task.performer_id = performer_id
        
        return self.task_repository.update_task(task)
    
    def get_allocated_tasks(self, user_id: int):
        return self.task_repository.get_allocated_tasks(user_id)
    
    def get_authored_tasks(self, user_id: int):
        return self.task_repository.get_authored_tasks(user_id)