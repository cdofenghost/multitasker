from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ..models.attachment import Attachment
from ..schemas.attachment import AttachmentSchema, AttachmentCreateSchema, AttachmentUpdateSchema


class AttachmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_attachment(self, attachment_schema: AttachmentCreateSchema) -> AttachmentSchema:
        attachment = Attachment(**attachment_schema.model_dump())

        self.db.add(attachment)
        self.db.commit()

        return AttachmentSchema(id=attachment.id, user_id=attachment.user_id, path=attachment.path)

    def find_attachment(self, id: int) -> AttachmentSchema:
        attachment = self.db.query(Attachment).get(id)

        if attachment is None:
            raise NoResultFound()
        
        return AttachmentSchema(id=attachment.id, user_id=attachment.user_id, path=attachment.path)
    
    def get_user_attachments(self, user_id: int) -> list[AttachmentSchema]:
        user_attachments = list(self.db.query(Attachment).filter(Attachment.user_id == user_id))

        return [AttachmentSchema(id=attachment.id, user_id=attachment.user_id, path=attachment.path)
                for attachment in user_attachments]

    def get_attachments(self) -> list[AttachmentSchema]:
        attachments = list(self.db.query(Attachment).all())

        return [AttachmentSchema(id=attachment.id, user_id=attachment.user_id, path=attachment.path)
                for attachment in attachments]
    
    def remove_attachment(self, id: int) -> AttachmentSchema:
        attachment = self.db.query(Attachment).get(id)

        if attachment is None:
            raise NoResultFound()
        
        self.db.query(Attachment).filter(Attachment.id == id).delete()
        self.db.commit()

        return AttachmentSchema(id=attachment.id, user_id=attachment.user_id, path=attachment.path)
    
    # def update_attachment(self, attachment_id: int, attachment_schema: AttachmentUpdateSchema) -> Attachment:
    #     attachment = self.db.query(Attachment).filter(Attachment.id == attachment_id).first()

    #     attachment.user
    #     self.db.merge(attachment)
    #     self.db.commit()

    #     return category


class AttachmentService:
    def __init__(self, attachment_repository: AttachmentRepository):
        self.attachment_repository = attachment_repository

    def add_attachment(self, attachment_data: AttachmentCreateSchema) -> AttachmentSchema:
        return self.attachment_repository.add_attachment(attachment_data)

    def get_attachment(self, id: int) -> AttachmentSchema:
        return self.attachment_repository.find_attachment(id)
    
    def get_user_attachments(self, user_id: int) -> list[AttachmentSchema]:
        return self.attachment_repository.get_user_attachments(user_id)

    def remove_attachment(self, id: int) -> AttachmentSchema:
        return self.attachment_repository.remove_attachment(id)

    # def update_category(self, category_id: int, category_data: AttachmentUpdateSchema) -> Attachment | None:
    #     category = self.attachment_repository.find_category(category_id)

    #     if category is None:
    #         return None
        
    #     category.name = category_data.name
    #     category.color = category_data.color

    #     self.attachment_repository.update_category(category)

    #     return category

    # def check_category_id(self, user_id: int, category_id: int) -> bool:
    #     categories = self.get_categories_by_user_id(user_id)

    #     for category in categories:
    #         if category_id == category.id:
    #             return True
            
    #     return False