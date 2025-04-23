from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .users import UserRepository, UserService, UserSchema

from .tokens import get_current_user

from .subtasks import SubtaskRepository, SubtaskService
from ..database import get_db
from ..schemas.subtask import SubtaskCreateSchema, SubtaskUpdateSchema, SubtaskSchema

router = APIRouter(prefix="/subtask", tags=["Subtasks"])


def get_task_repository(db: Session = Depends(get_db)):
    return SubtaskRepository(db)

def get_task_service(user_repository: SubtaskRepository = Depends(get_task_repository)):
    return SubtaskService(user_repository)

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
ServiceDependency = Annotated[SubtaskService, Depends(get_task_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]


@router.post("/", status_code=201, response_model=SubtaskSchema)
async def add_subtask(task_id: int,
                      task_data: SubtaskCreateSchema, 
                      service: ServiceDependency,
                      user: UserDependency):
    try:
        subtask = service.add_subtask(user.id, task_id, task_data)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Вам не разрешено прикреплять подзадачу к этой задаче, потому что она вам не принадлежит")
    
    return subtask


@router.put("/", response_model=SubtaskSchema)
async def update_subtask(subtask_id: int, 
                         task_data: SubtaskUpdateSchema, 
                         service: ServiceDependency,
                         user: UserDependency):
    try:
        subtask = service.update_subtask(user.id, subtask_id, task_data)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Подзадачи с таким ID не было найдено")
    
    except PermissionError:
        raise HTTPException(status_code=403, detail=" Вам не разрешено изменять эту подзадачу, потому что она вам не принадлежит")
    
    return subtask


@router.delete("/", status_code=204, response_model=None)
async def delete_subtask(subtask_id: int, 
                         service: ServiceDependency,
                         user: UserDependency):
    try:
        service.remove_subtask(user.id, subtask_id)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Подзадачи с таким ID не было найдено")

@router.get("/", response_model=SubtaskSchema)
async def get_subtask(subtask_id: int,
                            service: ServiceDependency,
                            user: UserDependency,):
    
    try:
        subtask = service.get_subtask(user.id, subtask_id)
        
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Подзадачи с таким ID не было найдено")
    
    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение подзадач проекта.")

    return subtask

@router.get("/all", response_model=list[SubtaskSchema])
async def get_task_subtasks(task_id: int,
                            service: ServiceDependency,
                            user: UserDependency,
                            status: int | None = None,
                            priority: int | None = None,
                            author_id: int | None = None,
                            performer_id: int | None = None,):
    
    try:
        subtasks = service.get_task_subtasks(user.id, task_id)
    
    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение подзадач проекта.")

    if not status is None:
        subtasks = [subtask for subtask in subtasks if subtask.status == status]

    if not priority is None:
        subtasks = [subtask for subtask in subtasks if subtask.priority == priority]

    if not author_id is None:
        subtasks = [subtask for subtask in subtasks if subtask.author_id == author_id]

    if not performer_id is None:
        subtasks = [subtask for subtask in subtasks if subtask.performer_id == performer_id]

    return subtasks

@router.get("/allocated", response_model=list[SubtaskSchema])
async def get_allocated_subtasks(project_id: int,
                              service: ServiceDependency,
                              user: UserDependency):
    try:
        tasks = service.get_allocated_subtasks(user.id)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение задач проекта.")

    return tasks

@router.put("/performer", response_model=SubtaskSchema)
async def set_subtask_performer(task_id: int,
                                performer_email: str,
                                service: ServiceDependency,
                                user: UserDependency,
                                user_service: UserServiceDependency):
    try:
        performer = user_service.get_user_by_email(performer_email)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован!")
        
    is_user_owner = service.check_task_ownership(user.id, task_id)

    if not is_user_owner:
        raise HTTPException(status_code=403, detail="Вы не являетесь автором этой задачи.")
    
    subtask = service.set_performer(task_id, performer.id)
    
    return subtask
