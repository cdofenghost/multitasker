from sqlalchemy.orm import Session

from ..models.task import Task
from ..schemas.task import TaskCreateSchema, TaskUpdateSchema

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()

        return task

    def find_task(self, id: int) -> Task | None:
        return self.db.query(Task).get(id)
    
    def get_tasks(self) -> list[Task]:
        pass
    
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


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def __to_task(self, task_data: TaskCreateSchema) -> Task:
        return Task(name=task_data.name, 
                    description=task_data.description,
                    author_id=task_data.author_id,
                    project_id=task_data.project_id,
                    performer_id=task_data.performer_id,
                    deadline=task_data.deadline,
                    priority=task_data.priority,)

    def add_task(self, task_data: TaskCreateSchema) -> Task | None:
        task = self.__to_task(task_data)

        return self.task_repository.add_task(task)

    def get_task(self, task_id: int) -> Task:
        pass
    
    def remove_task(self, task_id: int) -> Task | None:
        return self.task_repository.remove_task(task_id)

    def update_task(self, task_id: int, task_data: TaskUpdateSchema) -> Task | None:
        task = self.task_repository.find_task(task_id)

        if task is None:
            return None
        
        task.performer_id=task_data.performer_id
        task.name=task_data.name, 
        task.description=task_data.description,
        task.performer_id=task_data.performer_id,
        task.deadline=task_data.deadline,
        task.priority=task_data.priority,
        
        return self.task_repository.update_task(task)
