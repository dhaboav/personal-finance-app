from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlmodel import Session

from src.core import Crud, Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    Database.connect()
    yield
    Database.disconnect()


app = FastAPI(title="Finance Tracker", lifespan=lifespan)
crud = Crud()
SessionDep = Annotated[Session, Depends(Database.get_session)]


@app.get("/health", include_in_schema=False)
def health_check_endpoint():
    """Return the health status of the API

    This endpoint is used for monitoring purposes to verify that the API
    is up and running. It returns a simple JSON response indicating the
    status of the application.
    """
    return JSONResponse(content={"status": "ok"})


@app.post("/category")
def add_category(session: SessionDep, name: str):
    """Add a new category to the database

    Args:
        session: The database session injected by FastAPI.
        name: The name of the new category.

    Returns:
        JSON response indicating whether the category was added successfully.
    """
    if crud.set_category(session, name):
        return JSONResponse(
            content={"status": "success added new category"}, status_code=201
        )
    else:
        return JSONResponse(
            content={"status": "failed added new category"}, status_code=400
        )
