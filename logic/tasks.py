from fastapi import APIRouter, Body, Depends, HTTPException, Query, Form
from sqlalchemy.orm import Session

from pydantic import EmailStr
from email_validator import validate_email
from passlib.hash import bcrypt

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserIn

router = APIRouter()

