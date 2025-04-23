from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime

from ..models.task import Task
from ..models.project import Project
from ..models.category import Category
from ..models.subtask import Subtask
from ..schemas.subtask import SubtaskCreateSchema, SubtaskUpdateSchema, SubtaskSchema

class SubtaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_subtask(self, task_id: int, user_id: int, schema: SubtaskCreateSchema) -> Subtask:
        return Subtask(name=schema.name,
                    description=schema.description,
                    performer_id=schema.performer_id,
                    author_id=user_id,
                    task_id=task_id,
                    deadline=schema.deadline,
                    date_created=datetime.now(),
                    date_updated=datetime.now(),
                    status=1,
                    priority=schema.priority)
    
    def __to_subtask_schema(self, task: Subtask) -> SubtaskSchema:
        return SubtaskSchema(id=task.id,
                            name=task.name,
                            author_id=task.author_id,
                            performer_id=task.performer_id,
                            task_id=task.task_id,
                            deadline=task.deadline,
                            date_created=task.date_created,
                            date_updated=task.date_updated,
                            priority=task.priority,
                            status=task.status,
                            description=task.description)
    
    def add_subtask(self, task_id: int, user_id: int, subtask_schema: SubtaskCreateSchema) -> SubtaskSchema:
        subtask = self.__to_subtask(task_id=task_id, user_id=user_id, schema=subtask_schema)

        self.db.add(subtask)
        self.db.commit()

        return self.__to_subtask_schema(subtask)

    def find_subtask(self, subtask_id: int) -> SubtaskSchema:
        subtask = self.db.query(Subtask).filter(Subtask.id == subtask_id).first()

        if subtask is None:
            raise NoResultFound()
        
        return self.__to_subtask_schema(subtask)
    
    def get_subtasks(self) -> list[SubtaskSchema]:
        return [self.__to_subtask_schema(subtask)
                for subtask in self.db.query(Subtask).all()]
    
    def get_allocated_subtasks(self, user_id: int) -> list[SubtaskSchema]:
        return [self.__to_subtask_schema(subtask)
                for subtask in self.db.query(Subtask).filter(Subtask.performer_id == user_id)]
    
    def get_authored_subtasks(self, user_id: int) -> list[SubtaskSchema]:
        return [self.__to_subtask_schema(subtask)
                for subtask in self.db.query(Subtask).filter(Subtask.author_id == user_id)]

    def get_task_subtasks(self, task_id: int) -> list[SubtaskSchema]:
        return [self.__to_subtask_schema(subtask) 
                for subtask in self.db.query(Subtask).filter(Subtask.task_id == task_id)]
    
    def remove_subtask(self, id: int) -> SubtaskSchema:
        subtask = self.find_subtask(id)
        
        self.db.query(Subtask).filter(subtask.id == id).delete()
        self.db.commit()

        return self.__to_subtask_schema(subtask)
    
    def update_subtask(self, subtask_id: int, subtask_data: SubtaskUpdateSchema) -> SubtaskSchema:
        subtask = self.find_subtask(subtask_id)

        subtask.performer_id=subtask_data.performer_id
        subtask.name=subtask_data.name
        subtask.description=subtask_data.description
        subtask.deadline=subtask_data.deadline
        subtask.priority=subtask_data.priority
        subtask.status=subtask_data.status
        subtask.date_updated = datetime.now()

        sub = Subtask(name=subtask.name,
                    description=subtask.description,
                    performer_id=subtask.performer_id,
                    author_id=subtask.author_id,
                    task_id=subtask.task_id,
                    deadline=subtask.deadline,
                    date_created=subtask.date_created,
                    date_updated=datetime.now(),
                    status=subtask.status,
                    priority=subtask.priority)
        self.db.merge(sub)
        self.db.commit()

        return self.__to_subtask_schema(sub)

    def check_subtask_ownership(self, user_id: int, task_id: int) -> bool:
        subtask_author = self.db.query(Task).filter(Task.id == task_id,
                                                    Task.author_id == user_id).first()
        
        # project = self.db.query(Project).filter(Project.id == task.project_id).first()

        # if project is None:
        #     return False
        
        # category = self.db.query(Category).filter(Category.id == project.category_id,
        #                                           Category.user_id == user_id).first()
        
        return False if subtask_author is None else True

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

    def add_subtask(self, user_id: int, task_id: int, subtask_data: SubtaskCreateSchema) -> SubtaskSchema:
        user_is_owner = self.check_task_ownership(user_id, task_id)

        if subtask_data.performer_id == -1:
            subtask_data.performer_id = user_id
            
        if not user_is_owner:
            raise PermissionError()

        return self.subtask_repository.add_subtask(task_id=task_id, user_id=user_id, subtask_schema=subtask_data)

    def get_subtask(self, user_id: int, task_id: int) -> SubtaskSchema:
        subtask = self.subtask_repository.find_subtask(task_id)
        
        user_is_owner = self.check_task_ownership(user_id, subtask.task_id)

        if not user_is_owner:
            raise PermissionError()
        
        return subtask
    
    def get_task_subtasks(self, user_id: int, task_id: int) -> list[SubtaskSchema]:
        user_is_owner = self.check_task_ownership(user_id, task_id)
        
        if not user_is_owner:
            raise PermissionError()
        
        return self.subtask_repository.get_task_subtasks(task_id)
    
    def remove_subtask(self, user_id: int, subtask_id: int) -> SubtaskSchema:
        return self.subtask_repository.remove_subtask(subtask_id)

    def update_subtask(self, user_id: int, subtask_id: int, subtask_data: SubtaskUpdateSchema) -> SubtaskSchema:
        return self.subtask_repository.update_subtask(subtask_id, subtask_data)

    def check_subtask_ownership(self, user_id: int, subtask_id: int) -> bool:
        return self.subtask_repository.check_subtask_ownership(user_id, subtask_id)
    
    def check_task_ownership(self, user_id: int, task_id: int) -> bool:
        return self.subtask_repository.check_task_ownership(user_id, task_id)
    
    def set_performer(self, task_id: int, performer_id: int) -> Task | dict:
        task = self.subtask_repository.find_subtask(task_id)
        
        task.performer_id = performer_id
        
        return self.subtask_repository.update_subtask(task)
    
    def get_allocated_subtasks(self, user_id: int):
        return self.subtask_repository.get_allocated_subtasks(user_id)

    def get_authored_subtasks(self, user_id: int):
        return self.subtask_repository.get_authored_subtasks(user_id)