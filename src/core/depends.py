from typing import Annotated

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from src.core.database import Database

templates = Jinja2Templates(directory="templates")

SessionDep = Annotated[Session, Depends(Database.get_session)]
