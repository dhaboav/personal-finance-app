from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from src.core import Crud, Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    Database.connect()
    yield
    Database.disconnect()


app = FastAPI(title="Finance Tracker", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
crud = Crud()
SessionDep = Annotated[Session, Depends(Database.get_session)]


@app.get("/")
def index(request: Request, session: SessionDep):
    categories = crud.get_category(session)
    labels = crud.get_label(session)
    items = crud.get_item(session)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "categories": categories,
            "labels": labels,
            "items": items,
        },
    )


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


@app.post("/label")
def add_label(session: SessionDep, name: str):
    """Add a new label to the database

    Args:
        session: The database session injected by FastAPI.
        name: The name of the new label.

    Returns:
        JSON response indicating whether the label was added successfully.
    """
    if crud.set_label(session, name):
        return JSONResponse(
            content={"status": "success added new label"}, status_code=201
        )
    else:
        return JSONResponse(
            content={"status": "failed added new label"}, status_code=400
        )

@app.post("/items")
def add_item(
    request: Request,
    session: SessionDep,
    date: datetime = Form(...),
    category_id: int = Form(...),
    name: str = Form(...),
    label_id: int = Form(...),
    total: int = Form(...),
):

    if crud.set_item(session, date, category_id, name, label_id, total):
        items = crud.get_item(session)
        return templates.TemplateResponse(
            "partials/item_table.html",
            {
                "request": request,
                "items": items,
            },
        )
