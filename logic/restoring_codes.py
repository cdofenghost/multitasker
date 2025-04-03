from sqlalchemy.orm import Session

from ..models.restoring_codes import RestoringCode
from ..schemas.restoring_codes import (
    RestoringCodeCreateSchema, 
    RestoringCodeRevokeSchema, 
    RestoringCodeUpdateSchema,
    RestoringCodeSchema,
)

class RestoringCodeRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_code_model(self, code_schema: RestoringCodeCreateSchema) -> RestoringCode:
        return RestoringCode(user_email=code_schema.user_email, code=code_schema.code)
    
    def add_code(self, code_schema: RestoringCodeCreateSchema) -> RestoringCodeSchema:
        code = self.__to_code_model(code_schema)

        self.db.add(code)
        self.db.commit()

        return RestoringCodeSchema(code_id=code.id, user_email=code.user_email, code=code.code)

    def find_code(self, code_id: int) -> RestoringCodeSchema | None:
        code = self.db.query(RestoringCode).filter(RestoringCode.id == code_id).first()

        return RestoringCodeSchema(code_id=code.id, user_email=code.user_email, code=code.code)
    
    def find_code_by_email(self, user_email: str) -> RestoringCodeSchema | None:
        return self.db.query(RestoringCode).filter(RestoringCode.user_email == user_email).first()
    
    def revoke_code(self, code_schema: RestoringCodeRevokeSchema) -> RestoringCodeSchema:
        code = self.find_code_by_email(code_schema.user_email)

        if code is None:
            return None
        
        code.code = None

        self.db.merge(code)
        self.db.commit()

        return RestoringCodeSchema(code_id=code.code_id, user_email=code.user_email, code=code.code)
    
    def get_codes(self) -> list[RestoringCode]:
        pass

    # def get_task_subtasks(self, task_id: int) -> list[RestoringCode]:
    #     return list(self.db.query(RestoringCode).filter(RestoringCode.task_id == task_id))
    
    # def get_allocated_subtasks(self, user_id: int) -> list[RestoringCode]:
    #     subtasks = self.db.query(RestoringCode).filter(RestoringCode.performer_id == user_id)
    #     return list(subtasks)
    
    def remove_code(self, code_id: int) -> RestoringCodeSchema | None:
        code = self.find_code(code_id)

        if code is None:
            return None
        
        self.db.query(RestoringCode).filter(code.id == code_id).delete()
        self.db.commit()

        return RestoringCodeSchema(code_id=code.id, user_email=code.user_email, code=code.code)
    
    def update_code(self, code_schema: RestoringCodeSchema) -> RestoringCodeSchema:
        code = self.__to_code_model(code_schema)

        self.db.merge(code)
        self.db.commit()

        return code_schema
    

class RestoringCodeService:
    def __init__(self, code_repository: RestoringCodeRepository):
        self.code_repository = code_repository

    def add_code(self, code_data: RestoringCodeCreateSchema) -> RestoringCodeSchema | None:        
        return self.code_repository.add_code(code_data)

    def get_code_by_email(self, user_email: str) -> RestoringCodeSchema | None:
        code = self.code_repository.find_code_by_email(user_email)

        if code is None:
            return None
        
        return code
    
    def remove_code(self, code_data: RestoringCodeSchema) -> RestoringCodeSchema | None:
        code = self.get_code_by_email(code_data.user_email)

        if code is None:
            return None
        
        return self.code_repository.remove_code(code.id)

    def update_subtask(self, code_data: RestoringCodeUpdateSchema) -> RestoringCodeSchema | None:
        code = self.get_code_by_email(code_data.user_email)

        return self.code_repository.update_code(code_data)