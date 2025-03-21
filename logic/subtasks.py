from sqlalchemy.orm import Session

from ..models.task import Task
from ..models.project import Project
from ..models.category import Category
from ..models.subtask import Subtask
from ..schemas.subtask import SubtaskCreateSchema, SubtaskUpdateSchema

class SubtaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_subtask(self, task: Subtask) -> Subtask:
        self.db.add(task)
        self.db.commit()

        return task

    def find_subtask(self, subtask_id: int) -> Subtask | None:
        return self.db.query(Subtask).filter(Subtask.id == subtask_id).first()
    
    def get_tasks(self) -> list[Subtask]:
        pass

    def get_task_subtasks(self, task_id: int) -> list[Subtask]:
        return list(self.db.query(Subtask).filter(Subtask.task_id == task_id))
    
    def remove_subtask(self, id: int) -> Subtask | None:
        subtask = self.find_subtask(id)

        if subtask is None:
            return None
        
        self.db.query(Subtask).filter(subtask.id == id).delete()
        self.db.commit()

        return subtask
    
    def update_subtask(self, subtask: Subtask) -> Subtask:
        self.db.merge(subtask)
        self.db.commit()

        return subtask

    def check_subtask_ownership(self, user_id: int, subtask_id: int) -> bool:
        subtask = self.db.query(Subtask).filter(Subtask.id == subtask_id).first()

        if subtask is None:
            return False
        
        task = self.db.query(Task).filter(Task.id == subtask.task_id).first()

        if task is None:
            return False
        
        project = self.db.query(Project).filter(Project.id == task.project_id).first()

        if project is None:
            return False
        
        category = self.db.query(Category).filter(Category.id == project.category_id,
                                                  Category.user_id == user_id).first()
        
        return False if category is None else True

    def check_task_ownership(self, user_id: int, task_id: int) -> bool:
        task = self.db.query(Task).filter(Task.id == task_id).first()

        if task is None:
            return False
        
        project = self.db.query(Project).filter(Project.id == task.project_id).first()

        if project is None:
            return False
        
        category = self.db.query(Category).filter(Category.id == project.category_id,
                                                  Category.user_id == user_id).first()
        
        return False if category is None else True
    

class SubtaskService:
    def __init__(self, subtask_repository: SubtaskRepository):
        self.subtask_repository = subtask_repository

    def __to_subtask(self, task_id: int, task_data: SubtaskCreateSchema) -> Subtask:
        return Subtask(name=task_data.name, 
                    description=task_data.description,
                    author_id=task_data.author_id,
                    task_id=task_id,
                    performer_id=task_data.performer_id,
                    deadline=task_data.deadline,
                    priority=task_data.priority,)

    def add_subtask(self, user_id: int, task_id: int, subtask_data: SubtaskCreateSchema) -> Subtask | None:
        user_is_owner = self.check_task_ownership(user_id, task_id)

        if not user_is_owner:
            return None
        
        subtask = self.__to_subtask(task_id, subtask_data)

        return self.subtask_repository.add_subtask(subtask)

    def get_subtask(self, user_id: int, task_id: int) -> Subtask:
        subtask = self.subtask_repository.find_subtask(task_id)

        if subtask is None:
            return None
        
        user_is_owner = self.check_task_ownership(user_id, subtask.task_id)

        if not user_is_owner:
            return None
        
        return subtask
    
    def get_task_subtasks(self, user_id: int, task_id: int) -> list[Subtask]:
        user_is_owner = self.check_task_ownership(user_id, task_id)
        
        if not user_is_owner:
            return None
        
        return self.subtask_repository.get_task_subtasks(task_id)
    
    def remove_subtask(self, user_id: int, subtask_id: int) -> Subtask | None:
        subtask = self.get_subtask(user_id, subtask_id)

        if subtask is None:
            return None
        
        return self.subtask_repository.remove_subtask(subtask_id)

    def update_subtask(self, user_id: int, subtask_id: int, subtask_data: SubtaskUpdateSchema) -> Subtask | None:
        subtask = self.get_subtask(user_id, subtask_id)

        if subtask is None:
            return None
        
        subtask.performer_id=subtask_data.performer_id
        subtask.name=subtask_data.name, 
        subtask.description=subtask_data.description,
        subtask.performer_id=subtask_data.performer_id,
        subtask.deadline=subtask_data.deadline,
        subtask.priority=subtask_data.priority,
        
        return self.subtask_repository.update_subtask(subtask)

    def check_subtask_ownership(self, user_id: int, subtask_id: int) -> bool:
        return self.subtask_repository.check_subtask_ownership(user_id, subtask_id)
    
    def check_task_ownership(self, user_id: int, task_id: int) -> bool:
        return self.subtask_repository.check_task_ownership(user_id, task_id)