from sqlalchemy.orm import Session

from ..models.subtask import Subtask
from ..schemas.subtask import SubtaskCreateSchema, SubtaskUpdateSchema


class SubtaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_subtask(self, subtask: Subtask) -> Subtask:
        self.db.add(subtask)
        self.db.commit()

        return subtask

    def find_subtask(self, id: int) -> Subtask | None:
        return self.db.query(Subtask).get(id)
    
    def get_subtasks(self) -> list[Subtask]:
        pass
    
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


class SubtaskService:
    def __init__(self, subtask_repository: SubtaskRepository):
        self.subtask_repository = subtask_repository

    def __to_subtask(self, subtask_data: SubtaskCreateSchema) -> Subtask:
        return Subtask(name=subtask_data.name, 
                    description=subtask_data.description,
                    author_id=subtask_data.author_id,
                    task_id=subtask_data.task_id,
                    performer_id=subtask_data.performer_id,
                    deadline=subtask_data.deadline,
                    priority=subtask_data.priority,)

    def add_subtask(self, subtask_data: SubtaskCreateSchema) -> Subtask | None:
        subtask = self.__to_subtask(subtask_data)

        return self.subtask_repository.add_subtask(subtask)

    def get_subtask(self, subtask_id: int) -> Subtask:
        pass
    
    def remove_subtask(self, subtask_id: int) -> Subtask | None:
        return self.subtask_repository.remove_subtask(subtask_id)

    def update_subtask(self, subtask_id: int, subtask_data: SubtaskUpdateSchema) -> Subtask | None:
        subtask = self.subtask_repository.find_subtask(subtask_id)

        if subtask is None:
            return None
        
        subtask.name=subtask_data.name, 
        subtask.description=subtask_data.description,
        subtask.performer_id=subtask_data.performer_id,
        subtask.deadline=subtask_data.deadline,
        subtask.priority=subtask_data.priority,
        
        return self.subtask_repository.update_subtask(subtask)
