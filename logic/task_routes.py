from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .tokens import get_current_user, UserSchema
from .tasks import TaskRepository, TaskService
from ..database import get_db
from ..schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from .users import UserRepository, UserService

router = APIRouter(prefix="/task", tags=["Tasks"])


def get_task_repository(db: Session = Depends(get_db)):
    return TaskRepository(db)

def get_task_service(user_repository: TaskRepository = Depends(get_task_repository)):
    return TaskService(user_repository)

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
ServiceDependency = Annotated[TaskService, Depends(get_task_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]

@router.post("/", response_model=TaskSchema, status_code=201)
async def add_task(project_id: int,
                   task_data: TaskCreateSchema, 
                   service: ServiceDependency,
                   user: UserDependency):
    try:
        task = service.add_task(project_id, user.id, task_data)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Вам не разрешено добавлять задачу в проект, так как он не принадлежит вам.")
    
    return task

@router.get("/", response_model=TaskSchema)
async def get_task(task_id: int,
                   service: ServiceDependency,
                   user: UserDependency):
    try: 
        task = service.get_task(user.id, task_id)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Задача с таким ID не была найдена.")

    return task

@router.get("/all-tasks", response_model=list[TaskSchema])
async def get_all_tasks(service: ServiceDependency,
                            user: UserDependency,
                            status: int | None = None,
                            priority: int | None = None,
                            author_id: int | None = None,
                            performer_id: int | None = None,):
    try:
        tasks = service.get_tasks(user.id)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение подзадач проекта.")
    
    if not author_id is None:
        tasks = [task for task in tasks if task.author_id == author_id]

    if not performer_id is None:
        tasks = [task for task in tasks if task.performer_id == performer_id]

    if not status is None:
        tasks = [task for task in tasks if task.status == status]

    if not priority is None:
        tasks = [task for task in tasks if task.priority == priority]

    return tasks

@router.get("/all", response_model=list[TaskSchema])
async def get_project_tasks(project_id: int,
                            service: ServiceDependency,
                            user: UserDependency,
                            status: int | None = None,
                            priority: int | None = None,
                            author_id: int | None = None,
                            performer_id: int | None = None,):
    try:
        tasks = service.get_project_tasks(user.id, project_id)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение подзадач проекта.")
    
    if not author_id is None:
        tasks = [task for task in tasks if task.author_id == author_id]

    if not performer_id is None:
        tasks = [task for task in tasks if task.performer_id == performer_id]

    if not status is None:
        tasks = [task for task in tasks if task.status == status]

    if not priority is None:
        tasks = [task for task in tasks if task.priority == priority]

    return tasks

@router.get("/allocated", response_model=list[TaskSchema])
async def get_allocated_tasks(service: ServiceDependency,
                              user: UserDependency):
    try:
        tasks = service.get_allocated_tasks(user.id)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение задач проекта.")

    return tasks


@router.get("/authored", response_model=list[TaskSchema])
async def get_authored_tasks(service: ServiceDependency,
                              user: UserDependency):
    try:
        tasks = service.get_authored_tasks(user.id)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение задач проекта.")

    return tasks


@router.put("/", response_model=TaskSchema)
async def update_task(task_id: int, 
                      task_data: TaskUpdateSchema, 
                      service: ServiceDependency,
                      user: UserDependency):

    try:
        task = service.update_task(user.id, task_id, task_data)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Вам не разрешено изменять задачу, так как она не принадлежит вам.")
        
    return task


@router.delete("/", status_code=204, response_model=None)
async def delete_task(task_id: int, 
                      service: ServiceDependency,
                      user: UserDependency):
    try:  
        task = service.remove_task(user.id, task_id)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена.")


@router.put("/performer", response_model=TaskSchema)
async def set_task_performer(task_id: int,
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
    
    task = service.set_performer(task_id, performer.id)
    
    return task

@router.get("/count-subtasks", response_model=int)
async def count_subtaks(task_id: int,
                        user: UserDependency,
                        service: ServiceDependency):
    return service.count_subtasks(task_id)